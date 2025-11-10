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
.progress-bar {height:10px; background:#1f4068; border-radius:10px; overflow:hidden;}
.reason {font-size:13px; color:#c9d6e2; margin-top:4px;}
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

# Each question gives scores + reason
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
    {
        "question": "Which activity do you enjoy most?",
        "options": [
            ("Building robots or models", {"Engineering":3}, "You enjoy structured, hands-on projects."),
            ("Making websites or apps", {"IT":3}, "You like logical digital creation."),
            ("Doing lab experiments", {"Science":3}, "You’re fascinated by discovery."),
            ("Painting or filmmaking", {"Arts":3}, "You enjoy creative storytelling.")
        ]
    },
    {
        "question": "Your dream project would be:",
        "options": [
            ("Designing a car or bridge", {"Engineering":3}, "You focus on functionality & precision."),
            ("Developing AI that learns", {"IT":3}, "You love tech that thinks."),
            ("Discovering new medicine", {"Science":3}, "You’re drawn to innovation through research."),
            ("Creating a viral short film", {"Arts":3}, "You aim to evoke emotion through art.")
        ]
    },
    {
        "question": "In a team, you are usually the one who:",
        "options": [
            ("Builds and tests prototypes", {"Engineering":3}, "You’re hands-on and practical."),
            ("Codes or manages data", {"IT":3}, "You handle logical systems."),
            ("Researches and verifies facts", {"Science":3}, "You seek accuracy and evidence."),
            ("Designs the final presentation", {"Arts":3}, "You make things visually appealing.")
        ]
    },
    {
        "question": "Which word best describes you?",
        "options": [
            ("Practical", {"Engineering":3}, "You value working systems."),
            ("Tech-savvy", {"IT":3}, "You’re comfortable with digital tools."),
            ("Curious", {"Science":3}, "You ask why and how."),
            ("Creative", {"Arts":3}, "You love originality and beauty.")
        ]
    },
    {
        "question": "What would you love to learn next?",
        "options": [
            ("How machines work", {"Engineering":3}, "You think in mechanics."),
            ("How to create apps", {"IT":3}, "You love digital creativity."),
            ("How DNA replicates", {"Science":3}, "You’re drawn to life sciences."),
            ("How to edit music/videos", {"Arts":3}, "You express visually or musically.")
        ]
    },
    {
        "question": "Your ideal workspace is:",
        "options": [
            ("A lab or workshop", {"Engineering":3}, "You prefer physical experimentation."),
            ("A tech office or startup hub", {"IT":3}, "You like fast-paced innovation."),
            ("A research lab", {"Science":3}, "You enjoy structured exploration."),
            ("A studio or art room", {"Arts":3}, "You thrive on creative freedom.")
        ]
    },
    {
        "question": "Which tool would excite you most?",
        "options": [
            ("3D printer", {"Engineering":3}, "You love creation and structure."),
            ("Laptop & code editor", {"IT":3}, "You think in syntax and systems."),
            ("Microscope", {"Science":3}, "You’re detail-oriented."),
            ("Camera & sketchbook", {"Arts":3}, "You see beauty in perspective.")
        ]
    },
    {
        "question": "When facing a challenge, you:",
        "options": [
            ("Break it into parts & rebuild", {"Engineering":3}, "You think structurally."),
            ("Debug it logically", {"IT":3}, "You enjoy solving puzzles."),
            ("Hypothesize and test", {"Science":3}, "You use evidence and logic."),
            ("Brainstorm creative alternatives", {"Arts":3}, "You innovate visually.")
        ]
    },
    {
        "question": "You get most satisfaction from:",
        "options": [
            ("Seeing a machine work", {"Engineering":3}, "You love practical results."),
            ("Making software run perfectly", {"IT":3}, "You enjoy debugging success."),
            ("Proving a theory", {"Science":3}, "You value discovery."),
            ("Seeing others inspired by your art", {"Arts":3}, "You thrive on emotional impact.")
        ]
    },
    {
        "question": "Your favourite subjects are:",
        "options": [
            ("Physics / Math", {"Engineering":3}, "You like quantitative reasoning."),
            ("Computer Science", {"IT":3}, "You enjoy logical precision."),
            ("Biology / Chemistry", {"Science":3}, "You love exploring nature."),
            ("Literature / Art", {"Arts":3}, "You express through creativity.")
        ]
    },
    {
        "question": "How do you handle new tech?",
        "options": [
            ("Use it to build stuff", {"Engineering":3}, "You apply tech practically."),
            ("Learn how it works internally", {"IT":3}, "You explore digital logic."),
            ("Test it scientifically", {"Science":3}, "You evaluate evidence."),
            ("Use it creatively", {"Arts":3}, "You see artistic possibilities.")
        ]
    },
    {
        "question": "Which outcome sounds best?",
        "options": [
            ("Inventing a sustainable engine", {"Engineering":3}, "You’re innovative and practical."),
            ("Creating the next big app", {"IT":3}, "You combine logic with design."),
            ("Winning a science fair", {"Science":3}, "You value curiosity and data."),
            ("Exhibiting your artwork", {"Arts":3}, "You live for creative recognition.")
        ]
    },
    {
        "question": "What kind of problems do you like solving?",
        "options": [
            ("Mechanical & design problems", {"Engineering":3}, "You fix how things work."),
            ("Software & data issues", {"IT":3}, "You automate smartly."),
            ("Scientific mysteries", {"Science":3}, "You seek truth."),
            ("Creative challenges", {"Arts":3}, "You communicate ideas visually.")
        ]
    },
    {
        "question": "In 10 years, you see yourself as:",
        "options": [
            ("Building innovations that change lives", {"Engineering":3}, "You shape the physical world."),
            ("Creating digital revolutions", {"IT":3}, "You innovate through code."),
            ("Making scientific breakthroughs", {"Science":3}, "You push knowledge forward."),
            ("Inspiring people through art", {"Arts":3}, "You connect emotion and imagination.")
        ]
    }
]

# ---------------------- SESSION ----------------------
if "index" not in st.session_state:
    st.session_state.index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# ---------------------- FUNCTIONS ----------------------
def calculate_scores():
    scores = {c: 0 for c in categories}
    for ans in st.session_state.answers:
        for c, v in ans.items():
            if c in scores:
                scores[c] += v
    return scores

def reset_quiz():
    st.session_state.index = 0
    st.session_state.answers = []
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
            st.session_state.index += 1
            st.session_state.reason = reason
            if st.session_state.index >= len(questions):
                st.session_state.show_result = True
            st.rerun()
    progress = (st.session_state.index / len(questions)) * 100
    st.progress(progress/100)
    if "reason" in st.session_state:
        st.markdown(f"<p class='reason'>🧠 Reason: {st.session_state.reason}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Rocket sequence
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
    st.info("This analysis is based on your responses to the 15-question interest assessment. Each choice reflected traits tied to specific domains — giving you a snapshot of your inner alignment.")

    if st.button("🔁 Retake Quiz"):
        reset_quiz()
        st.rerun()
