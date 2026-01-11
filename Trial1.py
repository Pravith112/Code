import streamlit as st

st.set_page_config(page_title="Career Aptitude Test", layout="centered")

st.title("🎯 Career Aptitude Test")
st.write("Choose the career that appeals to you more.")

# Initialize session state
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

questions = [
    {
        "A": ("Nurse", "Provides medical care and supports patients.", "Healthcare"),
        "B": ("Software Developer", "Builds apps, websites, and software.", "Technology")
    },
    {
        "A": ("Teacher", "Educates students and builds knowledge.", "Education"),
        "B": ("Marketing Manager", "Promotes brands and strategies.", "Business")
    },
    {
        "A": ("Mechanical Engineer", "Designs machines and systems.", "Engineering"),
        "B": ("Graphic Designer", "Creates visual designs.", "Creative")
    },
    {
        "A": ("Lawyer", "Represents clients in legal matters.", "Law"),
        "B": ("Data Analyst", "Finds insights from data.", "Technology")
    },
    {
        "A": ("Doctor", "Diagnoses and treats patients.", "Healthcare"),
        "B": ("Research Scientist", "Conducts scientific research.", "Science")
    },
    {
        "A": ("Civil Engineer", "Builds infrastructure.", "Engineering"),
        "B": ("Interior Designer", "Designs indoor spaces.", "Creative")
    },
    {
        "A": ("Entrepreneur", "Builds and runs businesses.", "Business"),
        "B": ("Professor", "Teaches and researches.", "Education")
    },
    {
        "A": ("Cybersecurity Analyst", "Protects digital systems.", "Technology"),
        "B": ("Police Officer", "Maintains law and order.", "Law")
    },
    {
        "A": ("Biotechnologist", "Applies biology to technology.", "Science"),
        "B": ("Pharmacist", "Prepares and dispenses medicines.", "Healthcare")
    },
    {
        "A": ("Startup Founder", "Creates innovative companies.", "Business"),
        "B": ("UX Designer", "Designs user experiences.", "Creative")
    },
    {
        "A": ("Electrical Engineer", "Works with power systems.", "Engineering"),
        "B": ("AI Engineer", "Builds intelligent systems.", "Technology")
    },
    {
        "A": ("Judge", "Delivers court judgments.", "Law"),
        "B": ("Social Worker", "Helps communities.", "Healthcare")
    },
    {
        "A": ("Economist", "Studies economic systems.", "Business"),
        "B": ("Statistician", "Analyzes numerical data.", "Science")
    },
    {
        "A": ("Film Director", "Creates movies and stories.", "Creative"),
        "B": ("Architect", "Designs buildings.", "Engineering")
    },
    {
        "A": ("School Principal", "Leads an institution.", "Education"),
        "B": ("Product Manager", "Manages product strategy.", "Business")
    }
]

# ================= QUESTIONS =================
if st.session_state.q_no < len(questions):
    q = questions[st.session_state.q_no]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="padding:25px; border-radius:15px; border:1px solid #444; text-align:center;">
            <h3>{q['A'][0]}</h3>
            <p>{q['A'][1]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"Choose {q['A'][0]}"):
            st.session_state.scores[q["A"][2]] += 1
            st.session_state.q_no += 1
            st.rerun()

    with col2:
        st.markdown(
            f"""
            <div style="padding:25px; border-radius:15px; border:1px solid #444; text-align:center;">
            <h3>{q['B'][0]}</h3>
            <p>{q['B'][1]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"Choose {q['B'][0]}"):
            st.session_state.scores[q["B"][2]] += 1
            st.session_state.q_no += 1
            st.rerun()

# ================= RESULTS =================
else:
    st.subheader("🎉 Test Completed!")

    top_career = max(st.session_state.scores, key=st.session_state.scores.get)

    st.markdown(f"### 🔍 Best Career Match: **{top_career}**")

    suggestions = {
        "Technology": ["Software Developer", "AI Engineer", "Data Scientist"],
        "Healthcare": ["Doctor", "Nurse", "Medical Researcher"],
        "Business": ["Entrepreneur", "Business Analyst", "Marketing Manager"],
        "Creative": ["Designer", "Filmmaker", "UX Designer"],
        "Engineering": ["Civil", "Mechanical", "Electrical Engineer"],
        "Law": ["Lawyer", "Judge", "Public Prosecutor"],
        "Science": ["Scientist", "Biotechnologist", "Statistician"],
        "Education": ["Teacher", "Professor", "Academic Researcher"]
    }

    for c in suggestions[top_career]:
        st.write("•", c)

    st.divider()

    # 🔁 Restart Button
    if st.button("🔄 Take Test Again"):
        st.session_state.q_no = 0
        for key in st.session_state.scores:
            st.session_state.scores[key] = 0
        st.rerun()
