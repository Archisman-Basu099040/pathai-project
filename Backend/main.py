import os
import random
import pandas as pd
import random
from typing import TypedDict, Literal
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(title="PathAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    mentors_df = pd.read_csv("mentors.csv")
except FileNotFoundError:
    mentors_df = pd.DataFrame({
        "mentor_name": ["Ms. Rao (Math)", "Mr. Iqbal (Science)", "Ms. Devi (English)", "Mr. Thomas (Math)"],
        "subject": ["math", "science", "english", "math"],
        "status": ["free", "free", "free", "busy"],
    })

# Tracks the last mentor index handed out per subject so assignments rotate
# fairly instead of always returning the same mentor first.
mentor_rotation_state: dict[str, int] = {}
# Tracks recently assigned mentors per subject so we can avoid an immediate repeat.
recent_mentor_state: dict[str, list] = {}

class StudentState(TypedDict):
    name: str
    grade: str
    language: str
    subject: str
    topic: str
    query: str
    level: str
    reasoning: str
    explanation: str
    quiz: str
    assigned_mentor: str

class StudentIntakeRequest(BaseModel):
    name: str
    grade: str
    language: str
    subject: str
    topic: str
    query: str

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=GROQ_API_KEY)

ROUTER_SYSTEM_PROMPT = """You are an adaptive-learning triage router for a rural K-12 tutoring agent. 
Based on the student's grade and their own description of what's confusing about the topic, classify them into EXACTLY ONE learning path:
- foundational: missing prerequisite basics, needs concept rebuilt from ground up.
- grade_level: has basics but stuck on specific concept at current grade level.
- advanced: mastered grade-level material, asking about edge cases or extensions.
Respond with ONLY one word: foundational, grade_level, or advanced."""

def router_node(state: StudentState) -> StudentState:
    messages = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=f"Grade: {state['grade']}\nSubject: {state['subject']}\nTopic: {state['topic']}\nStudent's words: {state['query']}")
    ]
    level = llm.invoke(messages).content.strip().lower()
    if level not in ("foundational", "grade_level", "advanced"):
        level = "grade_level"
    return {**state, "level": level, "reasoning": f"Classified as '{level}' based on description."}

def route_decision(state: StudentState) -> Literal["foundational", "grade_level", "advanced"]:
    return state["level"]

def _explain(state: StudentState, style_instruction: str) -> str:
    prompt = f"""You are a patient, encouraging tutor writing for a grade {state['grade']} student learning {state['subject']} in {state['language']}.
Topic: {state['topic']}. The student said: "{state['query']}".
{style_instruction}
Write the explanation in {state['language']}. Keep it under 150 words, use a simple real-world example, and end with one encouraging sentence."""
    return llm.invoke([HumanMessage(content=prompt)]).content

def foundational_node(state: StudentState) -> StudentState:
    return {**state, "explanation": _explain(state, "Rebuild the concept from first principles. Do not assume prior knowledge.")}

def grade_level_node(state: StudentState) -> StudentState:
    return {**state, "explanation": _explain(state, "Assume prerequisites are known. Focus tightly on the specific point of confusion.")}

def advanced_node(state: StudentState) -> StudentState:
    return {**state, "explanation": _explain(state, "Assume mastery. Extend with a real-world application or deep insight beyond the syllabus.")}

def _grade_in_range(grade_range: str, grade_value: str) -> bool:
    try:
        lo, hi = str(grade_range).split("-")
        return int(lo) <= int(grade_value) <= int(hi)
    except (ValueError, AttributeError):
        return True

def mentor_availability_node(state: StudentState) -> StudentState:
    global mentors_df, mentor_rotation_state, recent_mentor_state

    if state["level"] != "foundational":
        return {**state, "assigned_mentor": "Not needed — self-serve explanation sufficient"}

    subject = state["subject"].lower()
    grade = state["grade"]
    language = state["language"]

    candidates = mentors_df[(mentors_df["subject"] == subject) & (mentors_df["status"] == "free")]
    if candidates.empty:
        # Fall back to any mentor for the subject rather than leaving the student stranded.
        candidates = mentors_df[mentors_df["subject"] == subject]
    if candidates.empty:
        return {**state, "assigned_mentor": "No mentor currently available for this subject"}

    # Prefer mentors whose grade range covers the student's grade.
    grade_matched = candidates[candidates["grade_range"].apply(lambda gr: _grade_in_range(gr, grade))]
    pool = grade_matched if not grade_matched.empty else candidates

    # Among those, prefer mentors who speak the student's preferred language.
    if "languages" in pool.columns:
        language_matched = pool[pool["languages"].str.contains(language, case=False, na=False)]
        if not language_matched.empty:
            pool = language_matched

    mentor_names = pool["mentor_name"].tolist()

    # Avoid immediately repeating a mentor this subject just used, when alternatives exist.
    recently_used = recent_mentor_state.get(subject, [])
    fresh_names = [name for name in mentor_names if name not in recently_used] or mentor_names

    # Rotate fairly through the pool instead of always picking the first match,
    # with a touch of randomness so simultaneous students don't get identical assignments.
    idx = (mentor_rotation_state.get(subject, -1) + 1) % len(fresh_names)
    mentor_rotation_state[subject] = idx
    mentor = fresh_names[idx] if random.random() > 0.15 else random.choice(fresh_names)

    recently_used = (recently_used + [mentor])[-2:]  # remember up to the last 2 mentors used
    recent_mentor_state[subject] = recently_used

    return {**state, "assigned_mentor": mentor}

def quiz_node(state: StudentState) -> StudentState:
    prompt = f"""Write exactly 2 short quiz questions (with answers) in {state['language']} to check whether a grade {state['grade']} student understands "{state['topic']}" in {state['subject']}, matched to a {state['level'].replace('_', ' ')} difficulty. Keep it concise."""
    return {**state, "quiz": llm.invoke([HumanMessage(content=prompt)]).content}

builder = StateGraph(StudentState)
builder.add_node("router", router_node)
builder.add_node("foundational", foundational_node)
builder.add_node("grade_level", grade_level_node)
builder.add_node("advanced", advanced_node)
builder.add_node("mentor_check", mentor_availability_node)
builder.add_node("quiz", quiz_node)

builder.set_entry_point("router")
builder.add_conditional_edges("router", route_decision, {
    "foundational": "foundational",
    "grade_level": "grade_level",
    "advanced": "advanced",
})
for path in ("foundational", "grade_level", "advanced"):
    builder.add_edge(path, "mentor_check")
builder.add_edge("mentor_check", "quiz")
builder.add_edge("quiz", END)

graph = builder.compile()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "PathAI Adaptive Learning Engine"}

@app.post("/api/intake")
def process_student_intake(request: StudentIntakeRequest):
    try:
        initial_state: StudentState = {
            "name": request.name,
            "grade": request.grade,
            "language": request.language,
            "subject": request.subject.lower(),
            "topic": request.topic,
            "query": request.query,
            "level": "",
            "reasoning": "",
            "explanation": "",
            "quiz": "",
            "assigned_mentor": "",
        }
        return graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))