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
    
    # Plot the radar chart
    ax.fill(angles, normalized_values, color='rgba(102, 126, 234, 0.3)', alpha=0.7)
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
            Your answers show strong alignment with <strong>{top_categories[0].lower()}</strong> careers. 
            You demonstrated exceptional skills and interests that are highly valuable in this field.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Radar chart visualization
    st.markdown("""
    <div class="radar-chart-container">
        <h3 style="color: #000000; text-align: center; margin-bottom: 1rem;">📈 Your Career Interest Profile</h3>
    """, unsafe_allow_html=True)
    
    radar_fig = create_radar_chart(scores)
    st.pyplot(radar_fig)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Score breakdown with enhanced progress bars
    st.markdown("""
    <div class="result-card">
        <h2 style="color: #000000; margin-bottom: 1.5rem;">📊 Detailed Score Breakdown</h2>
        <p style="color: #666666; margin-bottom: 2rem;">Here's how you scored across different career categories:</p>
    """, unsafe_allow_html=True)
    
    for category, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        percentage = (score / 45) * 100  # Max possible score is 45 (3*15 questions)
        
        st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; font-weight: 600; color: #000000;">
                    {category_emojis[category]} {category}
                </span>
                <span style="font-size: 1.1rem; font-weight: 600; color: {category_colors[category]};">{score} points</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {percentage}%; background: {category_colors[category]};">
                    <span class="progress-text">{percentage:.1f}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Suggested careers with better styling
    st.markdown(f"""
    <div class="result-card">
        <h2 style="color: #000000; margin-bottom: 1.5rem;">💼 Suggested Career Paths for {top_categories[0]}</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
    """, unsafe_allow_html=True)
    
    for career in career_suggestions[top_categories[0]][:6]:
        st.markdown(f"""
        <div class="career-item" style="border-left-color: {category_colors[top_categories[0]]};">
            <div style="font-weight: 600; color: #000000; margin-bottom: 0.3rem;">{career}</div>
            <div style="font-size: 0.9rem; color: #666666;">Great match for your skills and interests</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Answer analysis with enhanced styling
    st.markdown("""
    <div class="result-card">
        <h2 style="color: #000000; margin-bottom: 1.5rem;">🔍 Detailed Answer Analysis</h2>
        <p style="color: #666666; margin-bottom: 2rem;">Here's what your choices reveal about your skills and interests:</p>
    """, unsafe_allow_html=True)
    
    for i, (q_index, a_index) in enumerate(st.session_state.answers.items()):
        question = questions[q_index]
        option = question['options'][a_index]
        
        reasons = []
        skill_emojis = []
        for cat, points in option['scores'].items():
            if points > 0:
                reasons.append(f"{cat.lower()} skills")
                skill_emojis.append(category_emojis[cat])
        
        st.markdown(f"""
        <div class="question-box">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background: {category_colors['Engineering']}; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: 600; margin-right: 1rem;">
                    {i+1}
                </div>
                <h4 style="color: #000000; margin: 0;">{question['question']}</h4>
            </div>
            <div style="background: #ffffff; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <div style="color: #000000; font-weight: 600; margin-bottom: 0.5rem;">Your choice:</div>
                <div style="color: #667eea; font-weight: 500;">{option['text']}</div>
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                <div style="color: #000000; font-weight: 600; margin-bottom: 0.5rem;">This suggests:</div>
                <div style="color: #000000;">
                    You have strengths in {', '.join(reasons)} 
                    <span style="font-size: 1.2rem; margin-left: 0.5rem;">{' '.join(skill_emojis)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset button with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Take Quiz Again", use_container_width=True, type="primary"):
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
        # Display header with enhanced styling
        st.markdown("""
        <div class="header">
            <h1 style="color: #000000; margin-bottom: 1rem; font-size: 2.5rem;">🎯 Career Interest Quiz</h1>
            <p style="color: #666666; font-size: 1.3rem; margin-bottom: 2rem;">Discover your ideal career path with this comprehensive 15-question assessment</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 15px 30px; border-radius: 25px; color: white; 
                        display: inline-block; margin-top: 1rem; font-size: 1.2rem; font-weight: 600;">
                Question {}/15
            </div>
        </div>
        """.format(st.session_state.current_question + 1), unsafe_allow_html=True)
        
        # Display current question with enhanced styling
        current_q = questions[st.session_state.current_question]
        
        st.markdown(f"""
        <div class="question-box">
            <h2 style="color: #000000; margin-bottom: 1rem; font-size: 1.8rem;">{current_q['question']}</h2>
            <div style="color: #666666; font-size: 1.1rem;">Select the option that best describes you:</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display options with enhanced styling
        for i, option in enumerate(current_q['options']):
            is_selected = st.session_state.answers.get(st.session_state.current_question) == i
            button_style = """
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-color: #667eea !important;
            """ if is_selected else ""
            
            if st.button(
                option['text'], 
                key=f"option_{i}", 
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.answers[st.session_state.current_question] = i
                if st.session_state.current_question < len(questions) - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.show_results = True
                st.rerun()
        
        # Enhanced progress bar
        progress = (st.session_state.current_question + 1) / len(questions)
        st.markdown(f"""
        <div style="margin: 2rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #000000; font-weight: 500;">Progress</span>
                <span style="color: #667eea; font-weight: 600;">{int(progress * 100)}% Complete</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
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
                if st.button("Submit Results →", type="primary", use_container_width=True):
                    st.session_state.show_results = True
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
