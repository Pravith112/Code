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

# Custom CSS for enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        color: #000000;
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
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 3rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .result-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border-left: 6px solid;
        border: 1px solid #e0e0e0;
    }
    
    .category-score {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #000000;
    }
    
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 25px;
        border-radius: 12px;
        background: #f5f5f5;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 12px;
        transition: width 0.8s ease;
        position: relative;
        overflow: hidden;
    }
    
    .progress-text {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.9rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .question-box {
        background: #f8f9fa;
        border-radius: 18px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .option-button {
        width: 100%;
        margin: 0.8rem 0;
        padding: 1.2rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        background: #ffffff;
        text-align: left;
        transition: all 0.3s ease;
        font-weight: 500;
        color: #000000;
    }
    
    .option-button:hover {
        border-color: #667eea;
        background: #f0f4ff;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    .option-button:active {
        transform: translateY(0);
    }
    
    .submit-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 15px;
        font-weight: 600;
        margin-top: 2rem;
        width: 100%;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .submit-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.3rem;
        font-size: 0.9rem;
    }
    
    .career-item {
        background: #f8f9fa;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .career-item:hover {
        transform: translateX(5px);
        background: #f0f2f5;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #fff9e6 0%, #fff0f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffd700;
    }
    
    .radar-chart-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
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

def create_radar_chart(scores):
    """Create a radar chart visualization"""
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Normalize values for better visualization
    max_val = max(values) if max(values) > 0 else 1
    normalized_values = [v/max_val * 100 for v in values]
    
    # Create radar chart using matplotlib
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    normalized_values += normalized_values[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Plot the radar chart with corrected color specification
    ax.fill(angles, normalized_values, color='#667eea', alpha=0.3)
    ax.plot(angles, normalized_values, color='#667eea', linewidth=2)
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Customize the chart
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def display_results():
    """Display quiz results with enhanced visuals"""
    scores = calculate_scores()
    max_score = max(scores.values()) if max(scores.values()) > 0 else 1
    top_categories = [cat for cat, score in scores.items() if score == max_score]
    
    st.markdown("""
    <div class="header">
        <h1 style="color: #000000; margin-bottom: 1rem;">🎯 Your Career Interest Results</h1>
        <p style="color: #666666; font-size: 1.2rem;">Based on your answers, here's your comprehensive career profile analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top recommendation with better styling
    st.markdown(f"""
    <div class="result-card" style="border-left-color: {category_colors[top_categories[0]]};">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-right: 1rem;">{category_emojis[top_categories[0]]}</div>
            <div>
                <h2 style="color: #000000; margin: 0;">🌟 Top Recommendation</h2>
                <h3 style="color: {category_colors[top_categories[0]]}; margin: 0.5rem 0;">{top_categories[0]}</h3>
            </div>
        </div>
        <p style="color: #000000; font-size: 1.1rem; line-height: 1.6;">
            Your
