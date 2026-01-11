import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Career Aptitude Test", layout="centered")

# ================= GLOBAL CSS =================
st.markdown("""
<style>

/* Full page gradient background */
.stApp {
background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
color: white;
}

/* Hide Streamlit default elements */
header, footer {
visibility: hidden;
}

/* Glassmorphism card buttons */
div.stButton > button {
width: 100%;
height: 260px; /* FIXED HEIGHT */
min-height: 260px;
max-height: 260px;

border-radius: 20px;
border: 1px solid rgba(255,255,255,0.25);
background: rgba(255, 255, 255, 0.08);

backdrop-filter: blur(18px);
-webkit-backdrop-filter: blur(18px);

color: white;
font-size: 18px;
padding: 22px;

display: flex; /* FLEX FIX */
flex-direction: column;
justify-content: center; /* CENTER CONTENT */
align-items: center;
text-align: center;

white-space: normal;
overflow: hidden; /* PREVENT RESIZE */
transition: all 0.3s ease;
box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* Clamp text so it never stretches box */
div.stButton > button p,
div.stButton > button span {
display: -webkit-box;
-webkit-line-clamp: 5; /* MAX LINES */
-webkit-box-orient: vertical;
overflow: hidden;
}

/* Hover effect (liquid glow) */
div.stButton > button:hover {
background: rgba(255, 255, 255, 0.18);
border: 1px solid rgba(255,255,255,0.6);
transform: translateY(-4px) scale(1.02);
box-shadow: 0 0 25px rgba(0,255,200,0.45);
}

/* Restart button style */
button[kind="secondary"] {
background: rgba(255,255,255,0.15) !important;
border-radius: 14px !important;
border: 1px solid rgba(255,255,255,0.3) !important;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown(
"<h1 style='text-align:center;'>🎯 Career Aptitude Test</h1>",
unsafe_allow_html=True
)
st.markdown(
"<p style='text-align:center; opacity:0.85;'>Click the career that feels more like you</p>",
unsafe_allow_html=True
)

st.write("")

# ================= SESSION STATE =================
if "q_no" not in st.session_state:
st.session_state.q_no = 0
st.session_state.scores = {
"Technology": 0,
"Healthcare": 0,
"Business": 0,
"Creative": 0,
"Engineering": 0,
"Law": 0,
"Science": 0,
"Education": 0
}

# ================= QUESTIONS =================
questions = [
{"A": ("Nurse", "Provides medical care and emotional support to patients.", "Healthcare"),
"B": ("Software Developer", "Builds applications and solves problems using code.", "Technology")},

{"A": ("Teacher", "Guides students and builds strong foundations.", "Education"),
"B": ("Marketing Manager", "Creates strategies to promote brands and products.", "Business")},

{"A": ("Mechanical Engineer", "Designs machines and mechanical systems.", "Engineering"),
"B": ("Graphic Designer", "Creates visual content and digital art.", "Creative")},

{"A": ("Lawyer", "Represents people and interprets the law.", "Law"),
"B": ("Data Analyst", "Finds insights and trends from data.", "Technology")},

{"A": ("Doctor", "Diagnoses and treats illnesses.", "Healthcare"),
"B": ("Research Scientist", "Conducts experiments and discoveries.", "Science")},

{"A": ("Civil Engineer", "Builds roads, bridges, and infrastructure.", "Engineering"),
"B": ("Interior Designer", "Designs beautiful and functional spaces.", "Creative")},

{"A": ("Entrepreneur", "Builds and scales businesses.", "Business"),
"B": ("Professor", "Teaches and conducts academic research.", "Education")},

{"A": ("Cybersecurity Analyst", "Protects systems from digital threats.", "Technology"),
"B": ("Police Officer", "Maintains public safety and law.", "Law")},

{"A": ("Biotechnologist", "Applies biology to innovation.", "Science"),
"B": ("Pharmacist", "Prepares and manages medicines.", "Healthcare")},

{"A": ("Startup Founder", "Creates innovative companies.", "Business"),
"B": ("UX Designer", "Designs smooth digital experiences.", "Creative")},

{"A": ("Electrical Engineer", "Works with power and electronics.", "Engineering"),
"B": ("AI Engineer", "Builds intelligent systems.", "Technology")},

{"A": ("Judge", "Delivers justice in court.", "Law"),
"B": ("Social Worker", "Supports communities and individuals.", "Healthcare")},

{"A": ("Economist", "Studies economic systems and policies.", "Business"),
"B": ("Statistician", "Analyzes numerical data.", "Science")},

{"A": ("Film Director", "Creates visual stories and films.", "Creative"),
"B": ("Architect", "Designs buildings and spaces.", "Engineering")},

{"A": ("School Principal", "Leads educational institutions.", "Education"),
"B": ("Product Manager", "Oversees product vision and growth.", "Business")}
]

# ================= TEST FLOW =================
if st.session_state.q_no < len(questions):
q = questions[st.session_state.q_no]

col1, col2 = st.columns(2)

with col1:
if st.button(
f"**{q['A'][0]}**\n\n{q['A'][1]}",
key=f"A{st.session_state.q_no}"
):
st.session_state.scores[q["A"][2]] += 1
st.session_state.q_no += 1
st.rerun()

with col2:
if st.button(
f"**{q['B'][0]}**\n\n{q['B'][1]}",
key=f"B{st.session_state.q_no}"
):
st.session_state.scores[q["B"][2]] += 1
st.session_state.q_no += 1
st.rerun()

# ================= RESULTS =================
else:
st.markdown("<h2 style='text-align:center;'>✨ Test Completed ✨</h2>", unsafe_allow_html=True)

best_match = max(st.session_state.scores, key=st.session_state.scores.get)

st.markdown(
f"<h3 style='text-align:center;'>Your Best Career Match: <span style='color:#4cffd7;'>{best_match}</span></h3>",
unsafe_allow_html=True
)

recommendations = {
"Technology": ["Software Developer", "AI Engineer", "Data Scientist"],
"Healthcare": ["Doctor", "Nurse", "Medical Researcher"],
"Business": ["Entrepreneur", "Business Analyst", "Marketing Manager"],
"Creative": ["Designer", "Filmmaker", "UX Designer"],
"Engineering": ["Civil Engineer", "Mechanical Engineer", "Electrical Engineer"],
"Law": ["Lawyer", "Judge", "Public Prosecutor"],
"Science": ["Research Scientist", "Biotechnologist", "Statistician"],
"Education": ["Teacher", "Professor", "Academic Researcher"]
}

st.write("")
for career in recommendations[best_match]:
st.markdown(f"• {career}")

st.write("")
if st.button("🔄 Take Test Again"):
st.session_state.q_no = 0
for key in st.session_state.scores:
st.session_state.scores[key] = 0
st.rerun()

