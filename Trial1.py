# quantum_quest_final_v2.py
import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="Quantum Quest 🚀", page_icon="🚀", layout="centered")

# ---------------------- CSS ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at 20% 30%, #0d1b2a 0%, #1b263b 60%, #0d1b2a 100%);
    color: #f5f6fa;
}
.title {text-align:center; font-size:42px; font-weight:700; color:#aee3ff;}
.subtitle {text-align:center; color:#9cb2c7; margin-bottom:30px;}
.card {background:rgba(255,255,255,0.05); padding:20px; border-radius:16px; box-shadow:0 0 10px rgba(0,0,0,0.4);}
.opt {background:#16213e; color:white; border:none; padding:10px; border-radius:10px; width:100%; text-align:left;}
.opt:hover {background:#1a1a2e;}
.reason-block {background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-top:10px;}
.progress-bar {height:10px; background:#1f4068; border-radius:10px; overflow:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------- Data ----------------------
categories = ["Engineering", "IT", "Science", "Arts"]
descriptions = {
    "Engineering": "You have a logical, structured and practical mindset. Engineering involves applying science to real-world solutions — from machines to modern infrastructure.",
    "IT": "You enjoy working with technology, coding, and systems. IT careers demand problem-solving, creativity in software, and analytical logic.",
    "Science": "You are driven by curiosity and observation. Science involves experimenting, analyzing, and discovering how the world works.",
    "Arts": "You are expressive and imaginative. Artistic fields thrive on storytelling, design, and creativity that connect emotions with visuals or sounds."
}
strengths = {
    "Engineering": ["Analytical problem solving", "Design & testing", "Team-based innovation"],
    "IT": ["Logical thinking", "Coding skills", "System optimization"],
    "Science": ["Observation", "Critical research", "Precision"],
    "Arts": ["Creativity", "Aesthetic sense", "Storytelling"]
}
roles = {
    "Engineering": ["Mechanical Engineer", "Civil Engineer", "Aerospace Designer"],
    "IT": ["Software Developer", "Cybersecurity Expert", "AI Engineer"],
    "Science": ["Physicist", "Biologist", "Environmental Scientist"],
    "Arts": ["Graphic Designer", "Animator", "Film Maker"]
}

# ---------------------- Questions ----------------------
questions = [
    {
        "question": "When solving a problem, what’s your approach?",
        "options": [
            ("Build or fix something physically", {"Engineering":3}, "You like tangible solutions — core to engineering."),
            ("Write code or automate it", {"IT":3}, "You think in algorithms and automation."),
            ("Research deeply to understand causes", {"Science":3}, "You’re curious and investigative."),
            ("Sketch, visualize or design it", {"Arts":3}, "You express ideas creatively.")
        ]
    },
    # --- Same structure for all 15 questions (keep yours) ---
]

# ---------------------- SESSION ----------------------
if "index" not in st.session_state:
    st.session_state.index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []  # Stores dict of category scores
if "details" not in st.session_state:
    st.session_state.details = []  # Stores (question, chosen_option, reason)
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# ---------------------- FUNCTIONS ----------------------
def calculate_scores():
    scores = {c: 0 for c in categories}
    for ans in st.session_state.answers:
        for c, v in ans.items():
            scores[c] += v
    return scores

def reset_quiz():
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.details = []
    st.session_state.show_result = False

# ---------------------- MAIN ----------------------
st.markdown("<h1 class='title'>🧭 Quantum Quest</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Discover your true career domain through rocket-powered personality simulation 🚀</p>", unsafe_allow_html=True)

if not st.session_state.show_result:
    q = questions[st.session_state.index]
    st.markdown(f"<div class='card'><h3>Q{st.session_state.index+1}: {q['question']}</h3>", unsafe_allow_html=True)
    
    for i, (text, score, reason) in enumerate(q["options"]):
        if st.button(text, key=f"opt{i}"):
            st.session_state.answers.append(score)
            st.session_state.details.append((q["question"], text, reason))
            st.session_state.index += 1
            if st.session_state.index >= len(questions):
                st.session_state.show_result = True
            st.rerun()
    
    progress = (st.session_state.index / len(questions)) * 100
    st.progress(progress/100)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Rocket animation
    st.subheader("🚀 Launching your personalized Quantum Report...")
    p = st.progress(0)
    for i in range(100):
        p.progress((i+1)/100)
        time.sleep(0.02)
    st.balloons()
    st.success("Analysis Complete ✅")

    scores = calculate_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_scores[0][0]

    st.markdown(f"## 🌟 Your Top Career Domain: **{top_category}**")
    st.write(descriptions[top_category])
    st.write(f"**Key Strengths:** {', '.join(strengths[top_category])}")
    st.write(f"**Possible Career Roles:** {', '.join(roles[top_category])}")
    st.write("### 📊 Category Scores:")
    st.bar_chart(pd.DataFrame.from_dict(scores, orient='index', columns=['Score']))

    # --------- Personalized Reason Summary ---------
    st.markdown("## 🧠 Personalized Insights Based on Your Answers")
    for idx, (ques, opt, reason) in enumerate(st.session_state.details, 1):
        st.markdown(f"<div class='reason-block'><b>Q{idx}:</b> {ques}<br>🎯 <i>Your choice:</i> {opt}<br>💡 <i>Insight:</i> {reason}</div>", unsafe_allow_html=True)

    st.info("This analysis is based on your responses to the 15-question interest assessment. Each choice reflected traits tied to specific domains — giving you a snapshot of your inner alignment.")

    if st.button("🔁 Retake Quiz"):
        reset_quiz()
        st.rerun()
