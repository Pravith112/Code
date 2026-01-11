import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Career Aptitude Test", layout="centered")

# ================= CARD BUTTON CSS =================
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 220px;
    border-radius: 18px;
    border: 1px solid #444;
    background-color: transparent;
    color: white;
    font-size: 18px;
    padding: 20px;
    white-space: normal;
}

div.stButton > button:hover {
    border: 2px solid #4CAF50;
    background-color: #1e1e1e;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🎯 Career Aptitude Test")
st.write("Select the career option that appeals to you more.")

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
    {"A": ("Nurse", "Provides medical care and supports patients.", "Healthcare"),
     "B": ("Software Developer", "Builds apps, websites, and software.", "Technology")},

    {"A": ("Teacher", "Educates students and builds knowledge.", "Education"),
     "B": ("Marketing Manager", "Promotes brands and strategies.", "Business")},

    {"A": ("Mechanical Engineer", "Designs machines and systems.", "Engineering"),
     "B": ("Graphic Designer", "Creates visual designs.", "Creative")},

    {"A": ("Lawyer", "Represents clients in legal matters.", "Law"),
     "B": ("Data Analyst", "Finds insights from data.", "Technology")},

    {"A": ("Doctor", "Diagnoses and treats patients.", "Healthcare"),
     "B": ("Research Scientist", "Conducts scientific research.", "Science")},

    {"A": ("Civil Engineer", "Builds infrastructure.", "Engineering"),
     "B": ("Interior Designer", "Designs indoor spaces.", "Creative")},

    {"A": ("Entrepreneur", "Builds and runs businesses.", "Business"),
     "B": ("Professor", "Teaches and researches.", "Education")},

    {"A": ("Cybersecurity Analyst", "Protects digital systems.", "Technology"),
     "B": ("Police Officer", "Maintains law and order.", "Law")},

    {"A": ("Biotechnologist", "Applies biology to technology.", "Science"),
     "B": ("Pharmacist", "Prepares and dispenses medicines.", "Healthcare")},

    {"A": ("Startup Founder", "Creates innovative companies.", "Business"),
     "B": ("UX Designer", "Designs user experiences.", "Creative")},

    {"A": ("Electrical Engineer", "Works with power systems.", "Engineering"),
     "B": ("AI Engineer", "Builds intelligent systems.", "Technology")},

    {"A": ("Judge", "Delivers court judgments.", "Law"),
     "B": ("Social Worker", "Helps communities.", "Healthcare")},

    {"A": ("Economist", "Studies economic systems.", "Business"),
     "B": ("Statistician", "Analyzes numerical data.", "Science")},

    {"A": ("Film Director", "Creates movies and stories.", "Creative"),
     "B": ("Architect", "Designs buildings.", "Engineering")},

    {"A": ("School Principal", "Leads an institution.", "Education"),
     "B": ("Product Manager", "Manages product strategy.", "Business")}
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
    st.subheader("🎉 Test Completed!")

    best_match = max(st.session_state.scores, key=st.session_state.scores.get)

    st.markdown(f"### 🔍 Best Career Match: **{best_match}**")

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

    for career in recommendations[best_match]:
        st.write("•", career)

    st.divider()

    if st.button("🔄 Take Test Again"):
        st.session_state.q_no = 0
        for key in st.session_state.scores:
            st.session_state.scores[key] = 0
        st.rerun()
