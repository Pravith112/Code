import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Career Interest Quiz",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    .quiz-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
    }
    
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
    }
    
    .category-score {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        background: #f0f0f0;
        margin-bottom: 1rem;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .question-box {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .option-button {
        width: 100%;
        margin: 0.5rem 0;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        background: white;
        text-align: left;
        transition: all 0.3s ease;
    }
    
    .option-button:hover {
        border-color: #667eea;
        background: #f0f4ff;
    }
    
    .submit-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        margin-top: 2rem;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'scores' not in st.session_state:
    st.session_state.scores = {
        'Engineering': 0,
        'Arts': 0,
        'Management': 0,
        'Science': 0,
        'IT': 0
    }

# Career category colors
category_colors = {
    'Engineering': '#FF6B6B',
    'Arts': '#4ECDC4',
    'Management': '#45B7D1',
    'Science': '#F9A826',
    'IT': '#796AEE'
}

# Career category emojis
category_emojis = {
    'Engineering': '🔧',
    'Arts': '🎨',
    'Management': '📊',
    'Science': '🔬',
    'IT': '💻'
}

# Career suggestions
career_suggestions = {
    'Engineering': [
        "Mechanical Engineer", "Civil Engineer", "Electrical Engineer",
        "Aerospace Engineer", "Biomedical Engineer", "Environmental Engineer"
    ],
    'Arts': [
        "Graphic Designer", "Musician", "Writer", "Photographer",
        "Art Director", "Animator", "Architect"
    ],
    'Management': [
        "Project Manager", "Business Analyst", "HR Manager",
        "Marketing Manager", "Operations Manager", "Product Manager"
    ],
    'Science': [
        "Biologist", "Chemist", "Physicist", "Research Scientist",
        "Medical Researcher", "Environmental Scientist"
    ],
    'IT': [
        "Software Developer", "Data Scientist", "Network Administrator",
        "Cybersecurity Analyst", "Systems Analyst", "AI/ML Engineer"
    ]
}

# Quiz questions and options
questions = [
    {
        "question": "When working on a project, I prefer to:",
        "options": [
            {"text": "Design and build physical solutions", "scores": {"Engineering": 3, "IT": 1}},
            {"text": "Create visual or artistic elements", "scores": {"Arts": 3, "Management": 1}},
            {"text": "Organize and manage the team", "scores": {"Management": 3, "Engineering": 1}},
            {"text": "Research and analyze data", "scores": {"Science": 3, "IT": 1}}
        ]
    },
    {
        "question": "My favorite subjects in school were:",
        "options": [
            {"text": "Math and Physics", "scores": {"Engineering": 3, "Science": 2}},
            {"text": "Art and Music", "scores": {"Arts": 3, "Management": 1}},
            {"text": "Business and Economics", "scores": {"Management": 3, "IT": 1}},
            {"text": "Biology and Chemistry", "scores": {"Science": 3, "Engineering": 1}}
        ]
    },
    {
        "question": "In my free time, I enjoy:",
        "options": [
            {"text": "Building or fixing things", "scores": {"Engineering": 3, "IT": 1}},
            {"text": "Drawing, painting, or creating art", "scores": {"Arts": 3}},
            {"text": "Planning events or organizing things", "scores": {"Management": 3}},
            {"text": "Reading scientific articles or experiments", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I'm most comfortable working with:",
        "options": [
            {"text": "Tools and machinery", "scores": {"Engineering": 3}},
            {"text": "Creative software and design tools", "scores": {"Arts": 2, "IT": 2}},
            {"text": "Spreadsheets and organizational tools", "scores": {"Management": 3}},
            {"text": "Laboratory equipment", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "My problem-solving approach is:",
        "options": [
            {"text": "Practical and hands-on", "scores": {"Engineering": 3}},
            {"text": "Creative and innovative", "scores": {"Arts": 3, "Management": 1}},
            {"text": "Strategic and organized", "scores": {"Management": 3}},
            {"text": "Analytical and research-based", "scores": {"Science": 3, "IT": 1}}
        ]
    },
    {
        "question": "I value work that:",
        "options": [
            {"text": "Creates tangible results", "scores": {"Engineering": 3}},
            {"text": "Expresses creativity and emotion", "scores": {"Arts": 3}},
            {"text": "Involves leadership and decision-making", "scores": {"Management": 3}},
            {"text": "Advances knowledge and discovery", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "When faced with a challenge, I:",
        "options": [
            {"text": "Build a prototype or model", "scores": {"Engineering": 3, "IT": 1}},
            {"text": "Brainstorm creative solutions", "scores": {"Arts": 3}},
            {"text": "Develop a step-by-step plan", "scores": {"Management": 3}},
            {"text": "Research and gather data", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I'm most interested in careers that:",
        "options": [
            {"text": "Design and build infrastructure", "scores": {"Engineering": 3}},
            {"text": "Create artistic content", "scores": {"Arts": 3}},
            {"text": "Manage people and projects", "scores": {"Management": 3}},
            {"text": "Explore scientific phenomena", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "My ideal work environment is:",
        "options": [
            {"text": "Construction site or workshop", "scores": {"Engineering": 3}},
            {"text": "Studio or creative space", "scores": {"Arts": 3}},
            {"text": "Office with meeting rooms", "scores": {"Management": 3}},
            {"text": "Laboratory or research facility", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I enjoy working with:",
        "options": [
            {"text": "Machines and mechanical systems", "scores": {"Engineering": 3}},
            {"text": "Colors, shapes, and designs", "scores": {"Arts": 3}},
            {"text": "Teams and organizations", "scores": {"Management": 3}},
            {"text": "Data and experiments", "scores": {"Science": 3, "IT": 1}}
        ]
    },
    {
        "question": "My strength is:",
        "options": [
            {"text": "Technical problem-solving", "scores": {"Engineering": 3, "IT": 2}},
            {"text": "Creative thinking", "scores": {"Arts": 3}},
            {"text": "Organization and planning", "scores": {"Management": 3}},
            {"text": "Analytical thinking", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I get excited about:",
        "options": [
            {"text": "New technologies and inventions", "scores": {"Engineering": 2, "IT": 2, "Science": 1}},
            {"text": "Art exhibitions and creative works", "scores": {"Arts": 3}},
            {"text": "Business strategies and market trends", "scores": {"Management": 3}},
            {"text": "Scientific discoveries", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I prefer tasks that:",
        "options": [
            {"text": "Involve hands-on building", "scores": {"Engineering": 3}},
            {"text": "Allow creative expression", "scores": {"Arts": 3}},
            {"text": "Involve coordination and management", "scores": {"Management": 3}},
            {"text": "Require detailed analysis", "scores": {"Science": 3, "IT": 1}}
        ]
    },
    {
        "question": "My ideal project would:",
        "options": [
            {"text": "Solve a practical engineering problem", "scores": {"Engineering": 3}},
            {"text": "Create something beautiful or artistic", "scores": {"Arts": 3}},
            {"text": "Improve organizational efficiency", "scores": {"Management": 3}},
            {"text": "Answer a scientific question", "scores": {"Science": 3}}
        ]
    },
    {
        "question": "I'm most proud of my ability to:",
        "options": [
            {"text": "Build or fix complex systems", "scores": {"Engineering": 3, "IT": 1}},
            {"text": "Create original artwork or designs", "scores": {"Arts": 3}},
            {"text": "Lead and organize effectively", "scores": {"Management": 3}},
            {"text": "Understand complex concepts", "scores": {"Science": 3}}
        ]
    }
]

def calculate_scores():
    """Calculate scores based on answers"""
    scores = {category: 0 for category in category_colors.keys()}
    
    for question_index, answer_index in st.session_state.answers.items():
        option = questions[question_index]['options'][answer_index]
        for category, points in option['scores'].items():
            scores[category] += points
    
    return scores

def display_results():
    """Display quiz results"""
    scores = calculate_scores()
    max_score = max(scores.values())
    top_categories = [cat for cat, score in scores.items() if score == max_score]
    
    st.markdown("""
    <div class="header">
        <h1>🎯 Your Career Interest Results</h1>
        <p>Based on your answers, here's your career profile analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top recommendation
    st.markdown(f"""
    <div class="result-card" style="border-left-color: {category_colors[top_categories[0]]};">
        <h2>🌟 Top Recommendation: {category_emojis[top_categories[0]]} {top_categories[0]}</h2>
        <p>Your answers show strong alignment with {top_categories[0].lower()} careers. 
        You demonstrated skills and interests that are valuable in this field.</p>
        <h3>Suggested Career Paths:</h3>
        <ul>
    """, unsafe_allow_html=True)
    
    for career in career_suggestions[top_categories[0]][:4]:
        st.markdown(f"<li>{career}</li>", unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Score breakdown
    st.markdown("""
    <div class="result-card">
        <h2>📊 Your Score Breakdown</h2>
        <p>Here's how you scored across different career categories:</p>
    """, unsafe_allow_html=True)
    
    for category, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        percentage = (score / 45) * 100  # Max possible score is 45 (3*15 questions)
        st.markdown(f"""
        <div class="category-score">
            {category_emojis[category]} {category}: {score} points
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%; background: {category_colors[category]};"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Answer analysis
    st.markdown("""
    <div class="result-card">
        <h2>🔍 Answer Analysis</h2>
        <p>Here's what your choices reveal about your skills and interests:</p>
    """, unsafe_allow_html=True)
    
    for i, (q_index, a_index) in enumerate(st.session_state.answers.items()):
        question = questions[q_index]
        option = question['options'][a_index]
        
        reasons = []
        for cat in option['scores']:
            if option['scores'][cat] > 0:
                reasons.append(f"{cat.lower()} skills")
        
        st.markdown(f"""
        <div class="question-box">
            <h4>Q{i+1}: {question['question']}</h4>
            <p><strong>Your choice:</strong> {option['text']}</p>
            <p><strong>This suggests:</strong> You have strengths in {', '.join(reasons)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Take Quiz Again", use_container_width=True):
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.show_results = False
        st.session_state.scores = {category: 0 for category in category_colors.keys()}
        st.rerun()

def main():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    if st.session_state.show_results:
        display_results()
    else:
        # Display header
        st.markdown("""
        <div class="header">
            <h1>🎯 Career Interest Quiz</h1>
            <p>Discover your ideal career path with this 15-question assessment</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 10px 20px; border-radius: 20px; color: white; 
                        display: inline-block; margin-top: 1rem;">
                Question {}/15
            </div>
        </div>
        """.format(st.session_state.current_question + 1), unsafe_allow_html=True)
        
        # Display current question
        current_q = questions[st.session_state.current_question]
        
        st.markdown(f"""
        <div class="question-box">
            <h2>{current_q['question']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display options
        cols = st.columns(2)
        for i, option in enumerate(current_q['options']):
            col = cols[i % 2]
            if col.button(option['text'], key=f"option_{i}", use_container_width=True, 
                         type="primary" if st.session_state.answers.get(st.session_state.current_question) == i else "secondary"):
                st.session_state.answers[st.session_state.current_question] = i
                if st.session_state.current_question < len(questions) - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.show_results = True
                st.rerun()
        
        # Progress bar
        progress = (st.session_state.current_question + 1) / len(questions)
        st.progress(progress)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        with col3:
            if st.session_state.current_question == len(questions) - 1 and st.session_state.current_question in st.session_state.answers:
                if st.button("Submit →", type="primary", use_container_width=True):
                    st.session_state.show_results = True
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
