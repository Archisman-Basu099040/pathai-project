import pandas as pd

print("🌱 Seeding PathAI Enterprise Database System...")

# ==========================================
# TABLE 1: MENTOR REGISTRY (mentors.csv)
# ==========================================
mentors_data = [
    # Mathematics Mentors
    {"mentor_id": "MNT-101", "mentor_name": "Dr. Ananya Sharma", "subject": "math", "grade_range": "6-12", "languages": "English, Hindi", "specialization": "Algebra & Calculus", "experience_years": 12, "rating": 4.9, "total_sessions": 1450, "status": "free", "bio": "Former university lecturer specializing in visual mathematics and anxiety-free algebra."},
    {"mentor_id": "MNT-102", "mentor_name": "Mr. Rohan Chatterjee", "subject": "math", "grade_range": "5-10", "languages": "English, Bengali", "specialization": "Vedic Math & Geometry", "experience_years": 8, "rating": 4.8, "total_sessions": 980, "status": "free", "bio": "Passionate about making geometry and arithmetic intuitive through real-world puzzles."},
    {"mentor_id": "MNT-103", "mentor_name": "Ms. Priya Rao", "subject": "math", "grade_range": "5-8", "languages": "English, Hindi", "specialization": "Fractions & Number Systems", "experience_years": 6, "rating": 4.9, "total_sessions": 670, "status": "free", "bio": "Patience-first mentor focused on building rock-solid foundations for middle school math."},
    {"mentor_id": "MNT-104", "mentor_name": "Mr. David Thomas", "subject": "math", "grade_range": "9-12", "languages": "English", "specialization": "Trigonometry & Calculus", "experience_years": 15, "rating": 5.0, "total_sessions": 2100, "status": "busy", "bio": "Expert competitive exam coach helping high schoolers master advanced theorems."},
    {"mentor_id": "MNT-105", "mentor_name": "Ms. Sneha Mukherjee", "subject": "math", "grade_range": "6-10", "languages": "English, Bengali, Hindi", "specialization": "Statistics & Probability", "experience_years": 7, "rating": 4.7, "total_sessions": 540, "status": "free", "bio": "Data scientist turned educator who teaches probability through games and experiments."},
    
    # Science Mentors
    {"mentor_id": "MNT-201", "mentor_name": "Dr. Tariq Iqbal", "subject": "science", "grade_range": "6-12", "languages": "English, Hindi", "specialization": "Physics & Quantum Mechanics", "experience_years": 14, "rating": 4.9, "total_sessions": 1890, "status": "free", "bio": "Physics PhD dedicated to explaining the laws of the universe with simple household demos."},
    {"mentor_id": "MNT-202", "mentor_name": "Ms. Debosmita Sen", "subject": "science", "grade_range": "5-10", "languages": "English, Bengali", "specialization": "Biology & Botany", "experience_years": 9, "rating": 4.9, "total_sessions": 1120, "status": "free", "bio": "Botanist and educator who turns cell biology and ecosystems into fascinating stories."},
    {"mentor_id": "MNT-203", "mentor_name": "Mr. Vikram Verma", "subject": "science", "grade_range": "8-12", "languages": "English, Hindi", "specialization": "Organic & Inorganic Chemistry", "experience_years": 11, "rating": 4.8, "total_sessions": 1340, "status": "free", "bio": "Demystifying chemical equations and atomic structures with interactive visualizations."},
    {"mentor_id": "MNT-204", "mentor_name": "Ms. Sarah Jenkins", "subject": "science", "grade_range": "5-9", "languages": "English", "specialization": "Earth Science & Astronomy", "experience_years": 5, "rating": 4.8, "total_sessions": 420, "status": "busy", "bio": "Space enthusiast bringing the wonders of the solar system and geology to young learners."},
    {"mentor_id": "MNT-205", "mentor_name": "Mr. Arindam Ghosh", "subject": "science", "grade_range": "7-12", "languages": "English, Bengali, Hindi", "specialization": "Genetics & Human Anatomy", "experience_years": 10, "rating": 5.0, "total_sessions": 1600, "status": "free", "bio": "Medical researcher simplifying complex biological systems and genetics for aspiring doctors."},

    # English Mentors
    {"mentor_id": "MNT-301", "mentor_name": "Ms. Sunita Devi", "subject": "english", "grade_range": "5-12", "languages": "English, Hindi", "specialization": "Grammar & Creative Writing", "experience_years": 16, "rating": 5.0, "total_sessions": 2400, "status": "free", "bio": "Published author and veteran teacher specializing in essay structure and vocabulary building."},
    {"mentor_id": "MNT-302", "mentor_name": "Mr. Alok Banerjee", "subject": "english", "grade_range": "6-10", "languages": "English, Bengali", "specialization": "Literature & Comprehension", "experience_years": 8, "rating": 4.8, "total_sessions": 890, "status": "free", "bio": "Making classic literature and poetry accessible and exciting through modern analogies."},
    {"mentor_id": "MNT-303", "mentor_name": "Ms. Elena Rostova", "subject": "english", "grade_range": "5-11", "languages": "English", "specialization": "Phonics & Public Speaking", "experience_years": 7, "rating": 4.9, "total_sessions": 750, "status": "free", "bio": "Speech coach focused on confidence building, clear diction, and persuasive writing."},
    {"mentor_id": "MNT-304", "mentor_name": "Mr. Kabir Mehta", "subject": "english", "grade_range": "8-12", "languages": "English, Hindi", "specialization": "Advanced Rhetoric & Debating", "experience_years": 9, "rating": 4.7, "total_sessions": 680, "status": "busy", "bio": "National debate champion teaching students how to formulate logical, winning arguments."},
    {"mentor_id": "MNT-305", "mentor_name": "Ms. Poulomi Dutta", "subject": "english", "grade_range": "5-9", "languages": "English, Bengali, Hindi", "specialization": "Reading Comprehension & Syntax", "experience_years": 6, "rating": 4.9, "total_sessions": 610, "status": "free", "bio": "Helping bilingual students master complex English syntax and critical reading skills."}
]

df_mentors = pd.DataFrame(mentors_data)
df_mentors.to_csv("mentors.csv", index=False)
print(f"✅ Created mentors.csv ({len(df_mentors)} profiles | Columns: {len(df_mentors.columns)})")

# ==========================================
# TABLE 2: CURRICULUM MAP (curriculum_map.csv)
# ==========================================
curriculum_data = [
    {"topic_id": "TOP-M1", "subject": "math", "grade_level": 6, "topic_name": "Fractions & Decimals", "difficulty_tier": "foundational", "prerequisite": "Basic Division", "learning_objective": "Understand numerator/denominator relationships and decimal placement."},
    {"topic_id": "TOP-M2", "subject": "math", "grade_level": 8, "topic_name": "Linear Equations", "difficulty_tier": "intermediate", "prerequisite": "Algebraic Expressions", "learning_objective": "Solve for single variables using inverse operations."},
    {"topic_id": "TOP-M3", "subject": "math", "grade_level": 10, "topic_name": "Quadratic Equations", "difficulty_tier": "advanced", "prerequisite": "Linear Equations", "learning_objective": "Apply the quadratic formula and understand parabolic roots."},
    {"topic_id": "TOP-S1", "subject": "science", "grade_level": 6, "topic_name": "Photosynthesis", "difficulty_tier": "foundational", "prerequisite": "Plant Cell Basics", "learning_objective": "Explain how light energy converts carbon dioxide and water into glucose."},
    {"topic_id": "TOP-S2", "subject": "science", "grade_level": 8, "topic_name": "Newton's Laws of Motion", "difficulty_tier": "intermediate", "prerequisite": "Speed and Velocity", "learning_objective": "Analyze inertia, acceleration (F=ma), and action-reaction forces."},
    {"topic_id": "TOP-S3", "subject": "science", "grade_level": 10, "topic_name": "Atomic Structure & Valency", "difficulty_tier": "advanced", "prerequisite": "Periodic Table Basics", "learning_objective": "Calculate electron configurations and predict chemical bonding."},
    {"topic_id": "TOP-E1", "subject": "english", "grade_level": 6, "topic_name": "Parts of Speech", "difficulty_tier": "foundational", "prerequisite": "Basic Sentence Structure", "learning_objective": "Identify nouns, verbs, adjectives, adverbs, and conjunctions in context."},
    {"topic_id": "TOP-E2", "subject": "english", "grade_level": 8, "topic_name": "Active vs. Passive Voice", "difficulty_tier": "intermediate", "prerequisite": "Verb Tenses", "learning_objective": "Transform sentence structures to emphasize subject or action."},
    {"topic_id": "TOP-E3", "subject": "english", "grade_level": 10, "topic_name": "Critical Essay Structuring", "difficulty_tier": "advanced", "prerequisite": "Paragraph Transitions", "learning_objective": "Construct thesis statements, evidence body paragraphs, and syntheses."}
]

df_curriculum = pd.DataFrame(curriculum_data)
df_curriculum.to_csv("curriculum_map.csv", index=False)
print(f"✅ Created curriculum_map.csv ({len(df_curriculum)} syllabus topics)")

# ==========================================
# TABLE 3: QUESTION BANK (question_bank.csv)
# ==========================================
questions_data = [
    {"question_id": "Q-1001", "subject": "math", "topic_name": "Fractions & Decimals", "difficulty": "foundational", "question_text": "If you eat 3 slices of an 8-slice pizza, what fraction is left?", "correct_answer": "5/8", "hint": "Subtract the eaten slices from the total number of slices."},
    {"question_id": "Q-1002", "subject": "math", "topic_name": "Linear Equations", "difficulty": "intermediate", "question_text": "Solve for x: 3x + 7 = 22", "correct_answer": "x = 5", "hint": "Subtract 7 from both sides first, then divide by 3."},
    {"question_id": "Q-2001", "subject": "science", "topic_name": "Photosynthesis", "difficulty": "foundational", "question_text": "What green pigment in leaves absorbs sunlight for photosynthesis?", "correct_answer": "Chlorophyll", "hint": "It starts with 'Chlo-' and gives plants their green color."},
    {"question_id": "Q-2002", "subject": "science", "topic_name": "Newton's Laws of Motion", "difficulty": "intermediate", "question_text": "Which of Newton's laws is known as the Law of Inertia?", "correct_answer": "First Law", "hint": "An object at rest stays at rest unless acted upon by an unbalanced force."},
    {"question_id": "Q-3001", "subject": "english", "topic_name": "Active vs. Passive Voice", "difficulty": "intermediate", "question_text": "Change to passive voice: 'The chef cooked a delicious meal.'", "correct_answer": "A delicious meal was cooked by the chef.", "hint": "Make the object ('a delicious meal') the subject of the new sentence."}
]

df_questions = pd.DataFrame(questions_data)
df_questions.to_csv("question_bank.csv", index=False)
print(f"✅ Created question_bank.csv ({len(df_questions)} diagnostic questions)")

print("\n🏆 DATABASE UPGRADE COMPLETE! Your backend now contains a relational data schema.")