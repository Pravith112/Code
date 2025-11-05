import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE SETTINGS ------------------
st.set_page_config(page_title="Quantum Quest", page_icon="🧭", layout="centered")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #333;
    font-family: 'Poppins', sans-serif;
}
.main-title {
    text-align: center;
    font-size: 48px;
    color: white;
    font-weight: 800;
    margin-top: 20px;
}
.quiz-card {
    background: white;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    padding: 30px;
    max-width: 700px;
    margin: 40px auto;
    text-align: center;
}
.question {
    font-size: 22px;
    font-weight: 600;
    color: #222;
    margin-bottom: 25px;
}
.option-button {
    width: 100%;
    background: linear-gradient(90deg, #7F7FD5, #86A8E7, #91EAE4);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.3s ease;
}
.option-button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #764ba2, #667eea);
}
.progress-container {
    background-color: #f0f0f0;
    border-radius: 10px;
    height: 20px;
    margin-top: 20px;
}
.progress-bar {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    height: 20px;
    border-radius: 10px;
    transition: width 0.5s ease;
}
.result-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin: 25px auto;
    max-width: 700px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ------------------ QUESTIONS ------------------
questions = [
    {"question": "When faced with a problem, I prefer to:", 
     "options": [
         {"text": "Build something practical", "scores": {"Engineering": 3}},
         {"text": "Analyze data and find insights", "scores": {"Science": 3}},
         {"text": "Create art or design", "scores": {"Arts": 3}},
         {"text": "Lead a team to fix it", "scores": {"Management": 3}}
     ]},
    {"question": "I enjoy spending time:", 
     "options": [
         {"text": "Experimenting or coding", "scores": {"IT": 3}},
         {"text": "Sketching or playing instruments", "scores": {"Arts": 3}},
         {"text": "Planning events", "scores": {"Management": 3}},
         {"text": "Researching ideas", "scores": {"Science": 3}}
     ]},
    # Add up to 15 questions for your test here...
]

categories = ["Engineering", "Science", "Arts", "Management", "IT"]
colors = {
    "Engineering": "#ff6b6b",
    "Science": "#f9a826",
    "Arts": "#4ecdc4",
    "Management": "#45b7d1",
    "IT": "#796aee"
}
emojis = {
    "Engineering": "⚙️",
    "Science": "🔬",
    "Arts": "🎨",
    "Management": "📊",
    "IT": "💻"
}

# ------------------ SESSION STATE ------------------
if 'q_no' not in st.session_state:
    st.session_state.q_no = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# ------------------ SCORE CALCULATION ------------------
def calculate_scores():
    scores = {cat:0 for cat in categories}
    for ans in st.session_state.answers:
        for cat, score in ans.items():
            scores[cat] += score
    return scores

# ------------------ SHOW RESULTS ------------------
def show_results():
    st.markdown("<h1 class='main-title'>✨ Quantum Quest Results ✨</h1>", unsafe_allow_html=True)
    scores = calculate_scores()
    df = pd.DataFrame(list(scores.items()), columns=["Category", "Score"])
    top_category = max(scores, key=scores.get)

    st.markdown(f"""
    <div class='result-card'>
        <h2>{emojis[top_category]} Top Field: {top_category}</h2>
        <p>You show great potential in <b>{top_category}</b> related careers!</p>
    </div>
    """, unsafe_allow_html=True)

    st.bar_chart(df.set_index("Category"))
    st.balloons()
    if st.button("🔄 Retake Test"):
        st.session_state.q_no = 0
        st.session_state.answers = []
        st.session_state.show_result = False
        st.rerun()

# ------------------ MAIN QUIZ ------------------
st.markdown("<h1 class='main-title'>🧭 Quantum Quest</h1>", unsafe_allow_html=True)

if not st.session_state.show_result:
    q = questions[st.session_state.q_no]
    st.markdown("<div class='quiz-card'>", unsafe_allow_html=True)
    st.markdown(f"<p class='question'>{q['question']}</p>", unsafe_allow_html=True)
    
    for i, opt in enumerate(q['options']):
        if st.button(opt['text'], key=f"{st.session_state.q_no}_{i}", use_container_width=True):
            st.session_state.answers.append(opt['scores'])
            if st.session_state.q_no + 1 < len(questions):
                st.session_state.q_no += 1
            else:
                st.session_state.show_result = True
            st.rerun()

    # Progress bar
    progress = (st.session_state.q_no + 1) / len(questions)
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar' style='width:{progress*100}%'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
else:
    show_results()
