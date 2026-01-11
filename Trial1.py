import streamlit as st

st.set_page_config(page_title="Career Aptitude Test", layout="centered")

st.title("🎯 Career Aptitude Test")
st.write("Choose the option that interests you more in each question.")

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

# Questions list
questions = [
    {
        "A": ("Nurse", "Provides medical care, supports patients, and assists doctors.", "Healthcare"),
        "B": ("Software Developer", "Builds applications, websites, and software systems.", "Technology")
    },
    {
        "A": ("Teacher", "Educates students and helps them build knowledge.", "Education"),
        "B": ("Marketing Manager", "Promotes products and builds brand strategies.", "Business")
    },
    {
        "A": ("Mechanical Engineer", "Designs and builds machines and mechanical systems.", "Engineering"),
        "B": ("Graphic Designer", "Creates visual designs for branding and media.", "Creative")
    },
    {
        "A": ("Lawyer", "Represents clients and interprets laws.", "Law"),
        "B": ("Data Analyst", "Analyzes data to find patterns and insights.", "Technology")
    },
    {
        "A": ("Doctor", "Diagnoses illnesses and treats patients.", "Healthcare"),
        "B": ("Research Scientist", "Conducts experiments and scientific studies.", "Science")
    },
    {
        "A": ("Civil Engineer", "Designs infrastructure like roads and buildings.", "Engineering"),
        "B": ("Interior Designer", "Designs functional and aesthetic indoor spaces.", "Creative")
    },
    {
        "A": ("Entrepreneur", "Starts and manages business ventures.", "Business"),
        "B": ("Professor", "Teaches and conducts academic research.", "Education")
    },
    {
        "A": ("Cybersecurity Analyst", "Protects systems from cyber threats.", "Technology"),
        "B": ("Police Officer", "Maintains law and order and ensures public safety.", "Law")
    },
    {
        "A": ("Biotechnologist", "Uses biology to develop medical and industrial products.", "Science"),
        "B": ("Pharmacist", "Prepares and dispenses medicines.", "Healthcare")
    },
    {
        "A": ("Startup Founder", "Builds innovative products and companies.", "Business"),
        "B": ("UX Designer", "Designs user-friendly digital experiences.", "Creative")
    },
    {
        "A": ("Electrical Engineer", "Works on power systems and electronics.", "Engineering"),
        "B": ("AI Engineer", "Develops artificial intelligence systems.", "Technology")
    },
    {
        "A": ("Judge", "Presides over court cases and delivers judgments.", "Law"),
        "B": ("Social Worker", "Supports individuals and communities.", "Healthcare")
    },
    {
        "A": ("Economist", "Studies economic systems and policies.", "Business"),
        "B": ("Statistician", "Analyzes numerical data for insights.", "Science")
    },
    {
        "A": ("Film Director", "Creates and directs movies and visual stories.", "Creative"),
        "B": ("Architect", "Designs buildings and structures.", "Engineering")
    },
    {
        "A": ("School Principal", "Manages and leads educational institutions.", "Education"),
        "B": ("Product Manager", "Oversees product development and strategy.", "Business")
    }
]

# Display questions
if st.session_state.q_no < len(questions):
    q = questions[st.session_state.q_no]
    st.subheader(f"Question {st.session_state.q_no + 1}")

    option = st.radio(
        "Which career appeals to you more?",
        (
            f"A: {q['A'][0]} – {q['A'][1]}",
            f"B: {q['B'][0]} – {q['B'][1]}"
        )
    )

    if st.button("Next"):
        if option.startswith("A"):
            st.session_state.scores[q["A"][2]] += 1
        else:
            st.session_state.scores[q["B"][2]] += 1

        st.session_state.q_no += 1
        st.experimental_rerun()

# Results
else:
    st.subheader("🎉 Test Completed!")
    top_career = max(st.session_state.scores, key=st.session_state.scores.get)

    st.markdown(f"### 🔍 Your Best Career Match: **{top_career}**")

    career_suggestions = {
        "Technology": ["Software Developer", "AI Engineer", "Data Scientist"],
        "Healthcare": ["Doctor", "Nurse", "Medical Researcher"],
        "Business": ["Entrepreneur", "Marketing Manager", "Business Analyst"],
        "Creative": ["Graphic Designer", "Film Maker", "UX Designer"],
        "Engineering": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer"],
        "Law": ["Lawyer", "Judge", "Public Prosecutor"],
        "Science": ["Research Scientist", "Biotechnologist", "Statistician"],
        "Education": ["Teacher", "Professor", "Academic Researcher"]
    }

    st.write("**Recommended Careers:**")
    for career in career_suggestions[top_career]:
        st.write("•", career)

    st.success("This result is based on your interests and preferences.")
