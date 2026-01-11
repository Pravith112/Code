import streamlit as st
import time
# ------------------ SESSION STATE INIT ------------------
if "q_no" not in st.session_state:
    st.session_state.q_no = 0

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Technology":0, "Healthcare":0, "Business":0, "Creative":0,
        "Engineering":0, "Law":0, "Science":0, "Education":0
    }

st.set_page_config(page_title="Career Aptitude Test", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Center content */
.block-container {
    max-width: 900px;
    padding-top: 60px;
}

/* Hide Streamlit default elements */
header, footer {
visibility: hidden;
}

/* Glass card buttons */
div.stButton > button {
    width: 100%;
    height: 260px;
    min-height: 260px;
    max-height: 260px;

    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.25);
    background: rgba(255, 255, 255, 0.10);

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    color: white;
    font-size: 18px;
    padding: 22px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    white-space: normal;
    overflow: hidden;

    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.25s ease;
}

/* Hover + ripple illusion */
div.stButton > button:hover {
    transform: scale(1.03);
    background: rgba(255,255,255,0.18);
}

/* Text clamp */
div.stButton > button p,
div.stButton > button span {
    display: -webkit-box;
    -webkit-line-clamp: 5;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

* Hover effect (liquid glow) */
div.stButton > button:hover {
background: rgba(255, 255, 255, 0.18);
border: 1px solid rgba(255,255,255,0.6);
transform: translateY(-4px) scale(1.02);
box-shadow: 0 0 25px rgba(0,255,200,0.45);
}

/* Progress dots */
.progress {
    text-align: center;
    font-size: 20px;
    margin-bottom: 20px;
}

.fade {
    animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"<h1 style='text-align:center;'>🎯 Career Aptitude Test</h1>",
unsafe_allow_html=True
)
st.markdown(
"<p style='text-align:center; opacity:0.85;'>Click the career that feels more like you</p>",
unsafe_allow_html=True
)

st.write("")

# ------------------ QUESTIONS DATA ------------------
# 🔥 EDIT DESCRIPTIONS HERE ONLY 🔥
questions = [
    {
        "A": ("Software Engineer", "Designs and builds applications, websites, and intelligent systems using programming."),
        "B": ("Doctor", "Diagnoses illnesses, treats patients, and improves human health through medical science.")
    },
    {
        "A": ("Architect", "Plans and designs buildings focusing on aesthetics, safety, and functionality."),
        "B": ("Civil Engineer", "Constructs and manages infrastructure like roads, bridges, and buildings.")
    },
    {
        "A": ("Psychologist", "Studies human behavior and helps people manage emotions and mental health."),
        "B": ("HR Manager", "Manages employee relations, recruitment, and workplace culture.")
    },
    {
        "A": ("Journalist", "Researches, writes, and reports news for newspapers, TV, and digital media."),
        "B": ("Content Creator", "Creates engaging digital content for social media and online platforms.")
    },
    {
        "A": ("Entrepreneur", "Builds and manages startups by taking financial and strategic risks."),
        "B": ("Corporate Manager", "Oversees teams and operations within established organizations.")
    },
    {
        "A": ("Lawyer", "Represents clients legally and interprets laws and regulations."),
        "B": ("Judge", "Presides over court cases and ensures justice is delivered fairly.")
    },
    {
        "A": ("Graphic Designer", "Creates visual designs for branding, ads, and digital products."),
        "B": ("UI/UX Designer", "Designs user-friendly interfaces and experiences for apps and websites.")
    },
    {
        "A": ("Teacher", "Educates and mentors students to build knowledge and values."),
        "B": ("Professor", "Teaches advanced subjects and conducts academic research.")
    },
    {
        "A": ("Scientist", "Conducts experiments and research to discover new knowledge."),
        "B": ("Research Analyst", "Analyzes data to support business and policy decisions.")
    },
    {
        "A": ("Marketing Manager", "Develops strategies to promote products and brands."),
        "B": ("Sales Executive", "Directly sells products and builds customer relationships.")
    },
    {
        "A": ("Data Scientist", "Analyzes complex data to extract insights and predictions."),
        "B": ("Statistician", "Applies mathematical techniques to interpret numerical data.")
    },
    {
        "A": ("IAS Officer", "Implements government policies and manages administration."),
        "B": ("Politician", "Represents people and participates in law-making.")
    },
    {
        "A": ("Film Director", "Leads film production and storytelling."),
        "B": ("Actor", "Performs roles in films, theatre, or television.")
    },
    {
        "A": ("Mechanical Engineer", "Designs machines and mechanical systems."),
        "B": ("Automobile Engineer", "Specializes in vehicle design and manufacturing.")
    },
    {
        "A": ("Defense Officer", "Protects the nation through armed services."),
        "B": ("Police Officer", "Maintains law, order, and public safety.")
    },
]

# ------------------ SESSION STATE ------------------
if "q" not in st.session_state:
    st.session_state.q = 0
    st.session_state.score = 0

total = len(questions)

# ------------------ PROGRESS DOTS ------------------
dots = "".join("● " if i <= st.session_state.q else "○ " for i in range(total))
st.markdown(f"<div class='progress'>{dots}</div>", unsafe_allow_html=True)

# ------------------ MAIN LOGIC ------------------
if st.session_state.q_no < len(questions):
    q = questions[st.session_state.q_no]

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"**{q['A'][0]}**\n\n{q['A'][1]}", key=f"A{st.session_state.q_no}"):
            # You can hardcode the category if your tuple doesn't have it
            st.session_state.scores["Technology"] += 1  # Replace with actual category
            st.session_state.q_no += 1
            st.rerun()

    with col2:
        if st.button(f"**{q['B'][0]}**\n\n{q['B'][1]}", key=f"B{st.session_state.q_no}"):
            st.session_state.scores["Healthcare"] += 1  # Replace with actual category
            st.session_state.q_no += 1
            st.rerun()


# ------------------ RESULTS ------------------
# ------------------ RESULTS ------------------
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
        # ✅ Fix: indent this for-loop properly (inside the button block)
        for key in st.session_state.scores:
            st.session_state.scores[key] = 0
        st.rerun()



