import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Career Aptitude Test", layout="centered")

# ================= GLOBAL CSS =================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Hide Streamlit UI */
header, footer { visibility: hidden; }

/* Fade animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Glass cards */
div.stButton > button {
    width: 100%;
    height: 260px;
    min-height: 260px;
    max-height: 260px;

    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.25);
    background: rgba(255,255,255,0.08);

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

    overflow: hidden;
    animation: fadeIn 0.5s ease;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* Hover + ripple glow */
div.stButton > button:hover {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.6);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 0 28px rgba(0,255,200,0.45);
}

/* Text clamp */
div.stButton > button span {
    display: -webkit-box;
    -webkit-line-clamp: 5;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Progress dots */
.progress {
    text-align: center;
    font-size: 22px;
    letter-spacing: 6px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("<h1 style='text-align:center;'>🎯 Career Aptitude Test</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.85;'>Choose what feels more like you</p>", unsafe_allow_html=True)

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
    ("Nurse","Provides medical care and emotional support.","Healthcare",
     "Software Developer","Builds apps and solves problems using code.","Technology"),

    ("Teacher","Guides students and builds foundations.","Education",
     "Marketing Manager","Promotes brands and products.","Business"),

    ("Mechanical Engineer","Designs machines and systems.","Engineering",
     "Graphic Designer","Creates digital visuals.","Creative"),

    ("Lawyer","Represents people in legal matters.","Law",
     "Data Analyst","Finds insights from data.","Technology"),

    ("Doctor","Diagnoses and treats illnesses.","Healthcare",
     "Research Scientist","Conducts discoveries.","Science"),

    ("Civil Engineer","Builds infrastructure.","Engineering",
     "Interior Designer","Designs beautiful spaces.","Creative"),

    ("Entrepreneur","Builds businesses.","Business",
     "Professor","Teaches and researches.","Education"),

    ("Cybersecurity Analyst","Protects systems.","Technology",
     "Police Officer","Maintains law and order.","Law"),

    ("Biotechnologist","Applies biology to tech.","Science",
     "Pharmacist","Manages medicines.","Healthcare"),

    ("Startup Founder","Creates startups.","Business",
     "UX Designer","Designs user experiences.","Creative"),

    ("Electrical Engineer","Works with power.","Engineering",
     "AI Engineer","Builds intelligent systems.","Technology"),

    ("Judge","Delivers justice.","Law",
     "Social Worker","Helps communities.","Healthcare"),

    ("Economist","Studies economic systems.","Business",
     "Statistician","Analyzes numbers.","Science"),

    ("Film Director","Creates films.","Creative",
     "Architect","Designs buildings.","Engineering"),

    ("School Principal","Leads institutions.","Education",
     "Product Manager","Manages product vision.","Business")
]

total_q = len(questions)

# ================= TEST FLOW =================
if st.session_state.q_no < total_q:
    q = questions[st.session_state.q_no]

    # Progress dots
    dots = ["●" if i <= st.session_state.q_no else "○" for i in range(total_q)]
    st.markdown(f"<div class='progress'>{''.join(dots[:7])}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"**{q[0]}**\n\n{q[1]}", key=f"A{st.session_state.q_no}"):
            st.session_state.scores[q[2]] += 1
            st.session_state.q_no += 1
            st.rerun()

    with col2:
        if st.button(f"**{q[3]}**\n\n{q[4]}", key=f"B{st.session_state.q_no}"):
            st.session_state.scores[q[5]] += 1
            st.session_state.q_no += 1
            st.rerun()

# ================= RESULTS =================
else:
    st.markdown("<h2 style='text-align:center;'>✨ Results ✨</h2>", unsafe_allow_html=True)

    best = max(st.session_state.scores, key=st.session_state.scores.get)
    score = st.session_state.scores[best]
    confidence = int((score / total_q) * 100)

    st.markdown(
        f"<h3 style='text-align:center;'>Best Match: "
        f"<span style='color:#4cffd7'>{best}</span></h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h4 style='text-align:center;'>Confidence Score: {confidence}%</h4>",
        unsafe_allow_html=True
    )

    st.write("### Recommended Careers")
    careers = {
        "Technology": ["Software Developer","AI Engineer","Data Scientist"],
        "Healthcare": ["Doctor","Nurse","Medical Researcher"],
        "Business": ["Entrepreneur","Marketing Manager","Business Analyst"],
        "Creative": ["Designer","Filmmaker","UX Designer"],
        "Engineering": ["Civil","Mechanical","Electrical Engineer"],
        "Law": ["Lawyer","Judge","Public Prosecutor"],
        "Science": ["Scientist","Biotechnologist","Statistician"],
        "Education": ["Teacher","Professor","Researcher"]
    }

    for c in careers[best]:
        st.write("•", c)

    st.write("")
    if st.button("🔄 Take Test Again"):
        st.session_state.q_no = 0
        for k in st.session_state.scores:
            st.session_state.scores[k] = 0
        st.rerun()
