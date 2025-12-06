import streamlit as st
import pandas as pd
import random
import time
from streamlit.components.v1 import html

# Custom CSS for futuristic theme, animations, and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #6C63FF 0%, #121237 100%);
        background-attachment: fixed;
        color: #ffffff;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    .noise {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48ZmlsdGVyIGlkPSJub2lzZSI+PGZlVHVyYnVsZW5jZSBiYXNlRnJlcXVlbmN5PSIwLjkiIG51bU9IjQiIHN0aXRjaFRpbGVzPSJzdGl0Y2giLz48L2ZpbHRlcj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsdGVyPSJ1cmwoI25vaXNlKSIgb3BhY2l0eT0iMC4xIi8+PC9zdmc+');
        pointer-events: none;
        z-index: -1;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.5s ease-in-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .neon-glow {
        box-shadow: 0 0 10px #6C63FF, 0 0 20px #6C63FF, 0 0 30px #6C63FF;
        transition: 0.3s ease;
    }
    
    .neon-glow:hover {
        box-shadow: 0 0 15px #6C63FF, 0 0 30px #6C63FF, 0 0 45px #6C63FF;
        transform: scale(1.05);
    }
    
    .progress-bar {
        width: 100%;
        height: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #6C63FF, #121237);
        border-radius: 5px;
        transition: width 0.5s ease;
    }
    
    .count-up {
        font-size: 2em;
        font-weight: 700;
        color: #6C63FF;
        animation: countUp 2s ease-in-out;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.5); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .btn-option {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 10px 20px;
        margin: 5px;
        color: #ffffff;
        cursor: pointer;
        transition: 0.3s ease;
        width: 100%;
    }
    
    .btn-option:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6C63FF, #121237);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: 600;
        transition: 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #6C63FF;
    }
    
    .title {
        text-align: center;
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 20px;
        color: #ffffff;
        text-shadow: 0 0 10px #6C63FF;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 40px;
        color: #cccccc;
    }
    
    .result-card {
        margin: 20px 0;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .chart-container {
        margin: 20px 0;
    }
</style>
<div class="noise"></div>
""", unsafe_allow_html=True)

# Sample questions data
# Each question has section, question text, options with text and scores (dict of trait: points)
questions = [
    # Logical Reasoning
    {
        "section": "Logical Reasoning",
        "question": "If all cats are mammals and some mammals are pets, which of the following must be true?",
        "options": [
            {"text": "All cats are pets", "scores": {"Analytical": 1}},
            {"text": "Some cats are pets", "scores": {"Analytical": 3, "Practical": 2}},
            {"text": "No cats are pets", "scores": {"Analytical": 2}},
            {"text": "All pets are cats", "scores": {"Analytical": 1}}
        ]
    },
    {
        "section": "Logical Reasoning",
        "question": "What comes next in the sequence: 2, 4, 8, 16, ...?",
        "options": [
            {"text": "18", "scores": {"Analytical": 1}},
            {"text": "24", "scores": {"Analytical": 2}},
            {"text": "32", "scores": {"Analytical": 4, "Practical": 1}},
            {"text": "20", "scores": {"Analytical": 1}}
        ]
    },
    # Quantitative Aptitude
    {
        "section": "Quantitative Aptitude",
        "question": "What is 15% of 200?",
        "options": [
            {"text": "20", "scores": {"Analytical": 2}},
            {"text": "25", "scores": {"Analytical": 1}},
            {"text": "30", "scores": {"Analytical": 4, "Practical": 2}},
            {"text": "35", "scores": {"Analytical": 1}}
        ]
    },
    {
        "section": "Quantitative Aptitude",
        "question": "Solve for x: 2x + 3 = 7",
        "options": [
            {"text": "x = 1", "scores": {"Analytical": 1}},
            {"text": "x = 2", "scores": {"Analytical": 4, "Practical": 1}},
            {"text": "x = 3", "scores": {"Analytical": 1}},
            {"text": "x = 4", "scores": {"Analytical": 2}}
        ]
    },
    # Verbal Ability
    {
        "section": "Verbal Ability",
        "question": "Choose the synonym of 'Eloquent':",
        "options": [
            {"text": "Silent", "scores": {"Creative": 1}},
            {"text": "Articulate", "scores": {"Creative": 4, "Leader": 2}},
            {"text": "Clumsy", "scores": {"Creative": 1}},
            {"text": "Dull", "scores": {"Creative": 2}}
        ]
    },
    {
        "section": "Verbal Ability",
        "question": "Complete the analogy: Book is to Library as Painting is to:",
        "options": [
            {"text": "Museum", "scores": {"Creative": 4, "Analytical": 1}},
            {"text": "Gallery", "scores": {"Creative": 3}},
            {"text": "Frame", "scores": {"Creative": 1}},
            {"text": "Artist", "scores": {"Creative": 2}}
        ]
    },
    # Personality / Thinking Style
    {
        "section": "Personality / Thinking Style",
        "question": "When faced with a problem, I prefer to:",
        "options": [
            {"text": "Analyze data and facts", "scores": {"Analytical": 4}},
            {"text": "Brainstorm creative ideas", "scores": {"Creative": 4}},
            {"text": "Consult others and decide", "scores": {"Leader": 4}},
            {"text": "Try practical solutions", "scores": {"Practical": 4}}
        ]
    },
    {
        "section": "Personality / Thinking Style",
        "question": "In a team, I am most likely to:",
        "options": [
            {"text": "Lead the group", "scores": {"Leader": 4}},
            {"text": "Come up with innovative ideas", "scores": {"Creative": 4}},
            {"text": "Handle the details", "scores": {"Practical": 4}},
            {"text": "Research and analyze", "scores": {"Analytical": 4}}
        ]
    }
]

# Personality categories
personality_categories = {
    "Analytical": "Analytical Thinker",
    "Creative": "Creative Solver",
    "Leader": "Leader / Decision Maker",
    "Practical": "Practical Executor"
}

# Career suggestions based on personality
career_suggestions = {
    "Analytical Thinker": ["Data Analyst", "Research Scientist", "Engineer"],
    "Creative Solver": ["Designer", "Marketer", "Entrepreneur"],
    "Leader / Decision Maker": ["Manager", "Politician", "Consultant"],
    "Practical Executor": ["Technician", "Project Coordinator", "Tradesperson"]
}

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"Logical Reasoning": 0, "Quantitative Aptitude": 0, "Verbal Ability": 0, "Personality / Thinking Style": 0}
if 'traits' not in st.session_state:
    st.session_state.traits = {"Analytical": 0, "Creative": 0, "Leader": 0, "Practical": 0}
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False

# Function to calculate personality type
def get_personality_type(traits):
    max_trait = max(traits, key=traits.get)
    return personality_categories[max_trait]

# Function to generate detailed result text
def generate_result_text(scores, traits, personality_type):
    total_aptitude = sum(scores.values())
    strengths = []
    weaknesses = []
    advice = []
    
    # Strengths and weaknesses based on scores
    for section, score in scores.items():
        if score >= 6:  # Assuming max 8 per section (2 questions * 4)
            strengths.append(f"Strong in {section}")
        else:
            weaknesses.append(f"Needs improvement in {section}")
            advice.append(f"Practice more {section.lower()} questions to build skills.")
    
    # Personality-based
    if personality_type == "Analytical Thinker":
        strengths.append("Excellent at logical analysis and problem-solving.")
        advice.append("Incorporate creativity to balance analytical thinking.")
    elif personality_type == "Creative Solver":
        strengths.append("Innovative and idea-driven.")
        advice.append("Focus on practical implementation of ideas.")
    elif personality_type == "Leader / Decision Maker":
        strengths.append("Strong leadership and decision-making skills.")
        advice.append("Develop analytical skills for better-informed decisions.")
    elif personality_type == "Practical Executor":
        strengths.append("Hands-on and efficient in execution.")
        advice.append("Enhance creative thinking for innovative solutions.")
    
    careers = ", ".join(career_suggestions[personality_type])
    
    text = f"""
    **Total Aptitude Score:** {total_aptitude}/32  
    **Personality Type:** {personality_type}  
    
    **Section Breakdown:**  
    - Logical Reasoning: {scores['Logical Reasoning']}/8  
    - Quantitative Aptitude: {scores['Quantitative Aptitude']}/8  
    - Verbal Ability: {scores['Verbal Ability']}/8  
    - Personality / Thinking Style: {scores['Personality / Thinking Style']}/8  
    
    **Strengths:**  
    {chr(10).join(strengths)}  
    
    **Weaknesses:**  
    {chr(10).join(weaknesses)}  
    
    **Suggested Career Directions:**  
    Based on your {personality_type.lower()} profile, consider careers such as: {careers}.  
    
    **Improvement Advice:**  
    {chr(10).join(advice)}  
    Tailored to your choices, focus on balancing your skills for holistic development.
    """
    return text

# Main app logic
def main():
    st.markdown('<h1 class="title">Aptitude Test</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your strengths and potential career paths</p>', unsafe_allow_html=True)
    
    if not st.session_state.test_completed:
        # Test in progress
        total_questions = len(questions)
        progress = st.session_state.current_question / total_questions
        
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress*100}%"></div></div>', unsafe_allow_html=True)
        
        if st.session_state.current_question < total_questions:
            q = questions[st.session_state.current_question]
            st.markdown(f'<div class="glass-card slide-up"><h3>{q["section"]}</h3><p>{q["question"]}</p></div>', unsafe_allow_html=True)
            
            cols = st.columns(2)
            for i, option in enumerate(q["options"]):
                with cols[i % 2]:
                    if st.button(option["text"], key=f"option_{i}", help="Click to select"):
                        # Update scores
                        section = q["section"]
                        st.session_state.scores[section] += max(option["scores"].values())  # Simple: add max score for section
                        for trait, points in option["scores"].items():
                            st.session_state.traits[trait] += points
                        st.session_state.answers.append(option["text"])
                        st.session_state.current_question += 1
                        st.rerun()
        else:
            # Test completed
            st.session_state.test_completed = True
            # Save to CSV
            df = pd.DataFrame({
                "Answers": st.session_state.answers,
                "Scores": [st.session_state.scores],
                "Traits": [st.session_state.traits]
            })
            df.to_csv("test_results.csv", mode='a', header=False, index=False)
            st.rerun()
    else:
        # Results page
        personality_type = get_personality_type(st.session_state.traits)
        result_text = generate_result_text(st.session_state.scores, st.session_state.traits, personality_type)
        
        st.markdown('<div class="glass-card"><h2>Results</h2></div>', unsafe_allow_html=True)
        
        # Animated score
        total_score = sum(st.session_state.scores.values())
        st.markdown(f'<div class="count-up">Total Score: {total_score}</div>', unsafe_allow_html=True)
        
        # Charts
        import plotly.express as px
        fig = px.bar(x=list(st.session_state.scores.keys()), y=list(st.session_state.scores.values()), title="Section Scores")
        st.plotly_chart(fig, use_container_width=True)
        
        fig2 = px.pie(names=list(st.session_state.traits.keys()), values=list(st.session_state.traits.values()), title="Personality Traits")
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(f'<div class="result-card">{result_text}</div>', unsafe_allow_html=True)
        
        # Optional confetti
        if st.button("Celebrate! 🎉"):
            html("""
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
            <script>
                confetti();
            </script>
            """, height=0)
        
        if st.button("Retake Test"):
            st.session_state.current_question = 0
            st.session_state.scores = {"Logical Reasoning": 0, "Quantitative Aptitude": 0, "Verbal Ability": 0, "Personality / Thinking Style": 0}
            st.session_state.traits = {"Analytical": 0, "Creative": 0, "Leader": 0, "Practical": 0}
            st.session_state.answers = []
            st.session_state.test_completed = False
            st.rerun()

if __name__ == "__main__":
    main()
