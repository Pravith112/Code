import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="🎯 Career Interest Quiz",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 {
    color: #fff;
    text-align: center;
}
.question-box {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    margin: 15px 0;
    border-radius: 20px;
    border-left: 6px solid #667eea;
}
.option-button {
    width: 100%;
    margin: 5px 0;
    padding: 12px;
    border-radius: 12px;
    border: 2px solid #e9ecef;
    background: white;
    text-align: left;
    transition: all 0.3s ease;
}
.option-button:hover {
    border-color: #764ba2;
    background: #f0f4ff;
}
.submit-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 15px;
    border-radius: 12px;
    font-weight: 600;
    width: 100%;
}
.result-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
.progress-container {
    width: 100%;
    background: #f0f0f0;
    border-radius: 10px;
    margin-bottom: 15px;
}
.progress-fill {
    height: 20px;
    border-radius: 10px;
    background: #667eea;
    transition: width 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# ------------------- QUESTIONS -------------------
questions = [
    {
        "question": "When working on a project, I prefer to:",
        "options": [
            {"text": "Design and build physical solutions", "scores": {"Engineering": 3, "IT":1}},
            {"text": "Create visual or artistic elements", "scores": {"Arts":3, "Management":1}},
            {"text": "Organize and manage the team", "scores": {"Management":3, "Engineering":1}},
            {"text": "Research and analyze data", "scores": {"Science":3, "IT":1}}
        ]
    },
    {
        "question": "My favorite subjects in school were:",
        "options": [
            {"text": "Math and Physics", "scores": {"Engineering":3, "Science":2}},
            {"text": "Art and Music", "scores": {"Arts":3, "Management":1}},
            {"text": "Business and Economics", "scores": {"Management":3, "IT":1}},
            {"text": "Biology and Chemistry", "scores": {"Science":3, "Engineering":1}}
        ]
    },
    {
        "question": "In my free time, I enjoy:",
        "options": [
            {"text": "Building or fixing things", "scores": {"Engineering":3, "IT":1}},
            {"text": "Drawing, painting, or creating art", "scores": {"Arts":3}},
            {"text": "Planning events or organizing things", "scores": {"Management":3}},
            {"text": "Reading scientific articles or experiments", "scores": {"Science":3}}
        ]
    },
    # ... repeat till 15 questions like your original file
]

# Category colors and emojis
category_colors = {
    'Engineering':'#FF6B6B',
    'Arts':'#4ECDC4',
    'Management':'#45B7D1',
    'Science':'#F9A826',
    'IT':'#796AEE'
}
category_emojis = {
    'Engineering':'🔧',
    'Arts':'🎨',
    'Management':'📊',
    'Science':'🔬',
    'IT':'💻'
}
career_suggestions = {
    'Engineering':["Mechanical Engineer", "Civil Engineer", "Electrical Engineer","Aerospace Engineer"],
    'Arts':["Graphic Designer", "Musician", "Writer", "Photographer"],
    'Management':["Project Manager","Business Analyst","HR Manager","Marketing Manager"],
    'Science':["Biologist","Chemist","Physicist","Research Scientist"],
    'IT':["Software Developer","Data Scientist","Network Admin","Cybersecurity Analyst"]
}

# ------------------- SESSION STATE -------------------
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# ------------------- FUNCTIONS -------------------
def calculate_scores():
    scores = {cat:0 for cat in category_colors.keys()}
    for q_index, a_index in st.session_state.answers.items():
        option = questions[q_index]['options'][a_index]
        for cat, pts in option['scores'].items():
            scores[cat]+=pts
    return scores

def display_results():
    scores = calculate_scores()
    top_score = max(scores.values())
    top_categories = [cat for cat,score in scores.items() if score==top_score]
    
    st.markdown("<h1>🎯 Your Career Interest Results</h1>", unsafe_allow_html=True)
    
    # Top recommendation
    st.markdown(f"""
    <div class='result-card' style='border-left:5px solid {category_colors[top_categories[0]]}'>
    <h2>🌟 Top Recommendation: {category_emojis[top_categories[0]]} {top_categories[0]}</h2>
    <p>Suggested Careers:</p>
    <ul>
    """, unsafe_allow_html=True)
    for career in career_suggestions[top_categories[0]]:
        st.markdown(f"<li>{career}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Score bar chart
    df = pd.DataFrame(list(scores.items()), columns=['Category','Score'])
    st.bar_chart(df.set_index('Category'))

    # Replay
    if st.button("🔄 Retake Quiz"):
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.show_results = False
        st.rerun()
    
    st.balloons()

# ------------------- MAIN -------------------
st.markdown("<div class='question-box'>", unsafe_allow_html=True)

if st.session_state.show_results:
    display_results()
else:
    q = questions[st.session_state.current_question]
    st.markdown(f"<h2>Q{st.session_state.current_question+1}: {q['question']}</h2>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i,opt in enumerate(q['options']):
        col = cols[i%2]
        if col.button(opt['text'], key=f"opt_{i}"):
            st.session_state.answers[st.session_state.current_question] = i
            if st.session_state.current_question < len(questions)-1:
                st.session_state.current_question+=1
            else:
                st.session_state.show_results = True
            st.rerun()
    
    # Progress
    progress = (st.session_state.current_question+1)/len(questions)
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-fill' style='width:{progress*100}%'></div>
    </div>
    """, unsafe_allow_html=True)
