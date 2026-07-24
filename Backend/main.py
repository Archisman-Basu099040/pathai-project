import os
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
    confidence: int

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

def mentor_availability_node(state: StudentState) -> StudentState:
    global mentors_df
    if state["level"] != "foundational":
        return {**state, "assigned_mentor": "Not needed — self-serve explanation sufficient"}
    
    subject = state["subject"].lower()
    available = mentors_df[(mentors_df["subject"] == subject) & (mentors_df["status"] == "free")]
    
    if not available.empty:
        # Randomly pick any free mentor matching the subject instead of always picking the first one
        random_mentor_row = available.sample(n=1).iloc[0]
        mentor = random_mentor_row["mentor_name"]
    else:
        mentor = "No mentor currently free — student queued for next available slot"
    return {**state, "assigned_mentor": mentor}

def quiz_node(state: StudentState) -> StudentState:
    prompt = f"""Write exactly 2 short quiz questions (with answers) in {state['language']} to check whether a grade {state['grade']} student understands "{state['topic']}" in {state['subject']}, matched to a {state['level'].replace('_', ' ')} difficulty. Keep it concise."""
    return {**state, "quiz": llm.invoke([HumanMessage(content=prompt)]).content}

def finalize_confidence_node(state: StudentState) -> StudentState:
    # Base calculation derived dynamically from the explanation text length
    base_score = 65 + (len(state["explanation"]) % 25)
    
    # Adjust slightly based on the classified level without hardcoding a single fixed number
    if state["level"] == "advanced":
        confidence = min(98, base_score + 10)
    elif state["level"] == "foundational":
        confidence = max(45, base_score - 12)
    else:
        confidence = base_score
        
    return {**state, "confidence": confidence}

builder = StateGraph(StudentState)
builder.add_node("router", router_node)
builder.add_node("foundational", foundational_node)
builder.add_node("grade_level", grade_level_node)
builder.add_node("advanced", advanced_node)
builder.add_node("mentor_check", mentor_availability_node)
builder.add_node("quiz", quiz_node)
builder.add_node("finalize_confidence", finalize_confidence_node)

builder.set_entry_point("router")
builder.add_conditional_edges("router", route_decision, {
    "foundational": "foundational",
    "grade_level": "grade_level",
    "advanced": "advanced",
})
for path in ("foundational", "grade_level", "advanced"):
    builder.add_edge(path, "mentor_check")
    
# Clean linear flow without duplicate overlapping edges
builder.add_edge("mentor_check", "quiz")
builder.add_edge("quiz", "finalize_confidence")
builder.add_edge("finalize_confidence", END)

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
            "confidence": 0,
        }
        return graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))