# quantum_quest_futuristic.py
import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Quantum Quest — Futuristic",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS / THEME ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, .stApp {
      height: 100%;
      background: radial-gradient(circle at 10% 10%, #071026 0%, #081228 25%, #08121a 100%);
      color: #e6f0ff;
      font-family: 'Inter', sans-serif;
    }
    .panel {
      max-width: 920px;
      margin: 28px auto;
      padding: 20px;
      border-radius: 14px;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      box-shadow: 0 10px 40px rgba(2,6,23,0.7);
      border: 1px solid rgba(255,255,255,0.03);
    }
    .hero-title {
      text-align:center;
      font-size:44px;
      font-weight:800;
      margin: 6px 0 2px 0;
      letter-spacing: 0.6px;
      color: #dff4ff;
      text-shadow: 0 2px 12px rgba(79,139,255,0.12);
    }
    .hero-sub {
      text-align:center;
      color:#9fb3d8;
      margin-bottom:18px;
    }
    .qcard {
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      padding: 18px;
      border-radius: 12px;
      border-left: 4px solid rgba(79,139,255,0.18);
      margin-bottom: 12px;
    }
    .question-text {
      font-size:20px;
      font-weight:600;
      color:#e8f6ff;
      margin-bottom:12px;
    }
    .opt-btn {
      width:100%;
      padding:12px 14px;
      margin:8px 0;
      border-radius:10px;
      border:1px solid rgba(255,255,255,0.04);
      background: linear-gradient(90deg, rgba(21,32,64,0.9), rgba(18,26,48,0.9));
      color:#e6f0ff;
      text-align:left;
      transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .opt-btn:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(7,9,37,0.6);
      border-color: rgba(79,139,255,0.28);
    }
    /* white progress bar */
    .progress-outer {
      background: rgba(255,255,255,0.08);
      border-radius: 10px;
      height: 14px;
      overflow: hidden;
    }
    .progress-inner {
      height: 100%;
      background: #ffffff;
      width: 0%;
      transition: width 0.45s ease;
    }
    .progress-label {
      color: #d3e8ff;
      font-size:13px;
      margin-top:8px;
    }
    /* result hero */
    .result-hero {
      background: linear-gradient(90deg, rgba(79,139,255,0.12), rgba(124,77,255,0.08));
      padding: 12px;
      border-radius: 10px;
      margin-bottom: 12px;
      text-align:center;
    }
    .result-card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 12px;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid rgba(255,255,255,0.03);
    }
    .small {
      color:#9fb3d8;
      font-size:13px;
    }
    .reason-box {
      background: rgba(255,255,255,0.02);
      padding: 10px;
      border-radius: 8px;
      margin-top:8px;
      color:#dbefff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUESTIONS DATA ----------------
# Each option is: (display_text, {category:points}, professional_reason_text)
questions = [
    {
        "question": "When solving a problem, what do you prefer to do?",
        "options": [
            ("Design and construct a physical device", {"Engineering":3}, "Indicates aptitude for practical systems-thinking and applied mechanics."),
            ("Write software to automate it", {"IT":3}, "Shows a proclivity for algorithmic logic and software engineering."),
            ("Design and run experiments to understand it", {"Science":3}, "Reflects curiosity, rigor and scientific methodology."),
            ("Sketch or craft an aesthetic solution", {"Arts":3}, "Suggests strengths in visual thinking and creative expression."),
        ]
    },
    {
        "question": "Which school project excited you most?",
        "options": [
            ("Building a model or prototype", {"Engineering":3}, "Preference for hands-on creation and engineering design."),
            ("Making a website/app", {"IT":3}, "Interest in software, user experience and digital problem solving."),
            ("Carrying out a research or lab report", {"Science":3}, "Affinity for observation, measurement and hypothesis testing."),
            ("Creating a poster, short film or artwork", {"Arts":3}, "Tendency toward storytelling and visual communication."),
        ]
    },
    {
        "question": "Which of these activities would you pick on a free weekend?",
        "options": [
            ("Tinkering with electronics or mechanical parts", {"Engineering":3}, "You enjoy tangible problem solving and practical iteration."),
            ("Experimenting with code or data", {"IT":3}, "You enjoy logical puzzles and scalable solutions in software."),
            ("Reading scientific journals or doing experiments", {"Science":3}, "You are methodical and enjoy evidence-based exploration."),
            ("Working on a creative portfolio (photos, music, art)", {"Arts":3}, "You derive satisfaction from creative expression."),
        ]
    },
    {
        "question": "When evaluating success you focus on:",
        "options": [
            ("Reliable, measurable physical performance", {"Engineering":3}, "You value robustness and engineering efficiency."),
            ("System stability and code quality", {"IT":3}, "You prioritize clean systems and maintainable design."),
            ("Reproducible, validated results", {"Science":3}, "You emphasize rigor and reproducibility."),
            ("Emotional and aesthetic impact", {"Arts":3}, "You value human connection through creativity."),
        ]
    },
    {
        "question": "Which environment energizes you most?",
        "options": [
            ("A workshop with tools and parts", {"Engineering":3}, "Hands-on settings amplify your problem-solving strengths."),
            ("A fast-paced tech studio or startup", {"IT":3}, "Dynamic digital environments bring out your strengths."),
            ("A research lab or observatory", {"Science":3}, "Analytical and investigative contexts suit you well."),
            ("An art studio or creative collective", {"Arts":3}, "Collaborative creative spaces inspire you."),
        ]
    },
    {
        "question": "When leading a small team, your role tends to be:",
        "options": [
            ("Defining technical specs and building", {"Engineering":2, "IT":1}, "You naturally organize technical work and produce solutions."),
            ("Coordinating tasks and timelines", {"IT":1, "Engineering":1, "Science":1}, "You show cross-functional coordination skills."),
            ("Design direction and creative mentoring", {"Arts":2, "Management":1}, "You guide creative quality and vision."),
            ("Setting research goals and validating results", {"Science":2, "Management":1}, "You bring methodical leadership and clarity."),
        ]
    },
    {
        "question": "Pick the tool you'd rather learn first:",
        "options": [
            ("3D CAD / fabrication tools", {"Engineering":3}, "Practical design and manufacturing interest is evident."),
            ("A modern programming framework", {"IT":3}, "Shows preference for applied software development."),
            ("Advanced lab instrumentation", {"Science":3}, "Indicates experimental rigor and interest in measurement."),
            ("Digital art suite or film editing tools", {"Arts":3}, "Indicates desire to create professional visual media."),
        ]
    },
    {
        "question": "Which problem excites you more?",
        "options": [
            ("Improving mechanical efficiency", {"Engineering":3}, "You value optimization in physical systems."),
            ("Scaling a backend architecture", {"IT":3}, "You are oriented towards system architecture and performance."),
            ("Understanding an ecological pattern", {"Science":3}, "You are drawn to system-level scientific questions."),
            ("Changing how people feel through media", {"Arts":3}, "You are motivated by emotional and cultural impact."),
        ]
    },
    {
        "question": "Your ideal deliverable is:",
        "options": [
            ("A tested working prototype", {"Engineering":3}, "Delivering working artifacts appeals to you."),
            ("A deployable software product", {"IT":3}, "You like software that impacts users at scale."),
            ("A peer-reviewed study or paper", {"Science":3}, "You aim for validated contributions to knowledge."),
            ("A curated exhibition or campaign", {"Arts":3}, "You want your work to be publicly experienced."),
        ]
    },
    {
        "question": "When learning, you prefer:",
        "options": [
            ("Hands-on guided projects", {"Engineering":3}, "You learn best through doing and iteration."),
            ("Interactive coding exercises", {"IT":3}, "You learn by building incrementally and debugging."),
            ("Careful experimental protocols", {"Science":3}, "You prefer systematic learning with evidence."),
            ("Workshops and critiques", {"Arts":3}, "You thrive on feedback and iterative refinement."),
        ]
    },
    {
        "question": "Which description fits your thought process?",
        "options": [
            ("Systems-oriented and structured", {"Engineering":3}, "You naturally decompose problems into testable components."),
            ("Abstract logical & algorithmic", {"IT":3}, "You enjoy symbolic reasoning and pattern extraction."),
            ("Hypothesis-driven and meticulous", {"Science":3}, "You favour careful reasoning and validation."),
            ("Associative and expressive", {"Arts":3}, "You link ideas through metaphor and imagery."),
        ]
    },
    {
        "question": "Which impact would you like to have?",
        "options": [
            ("Create reliable infrastructure/objects", {"Engineering":3}, "You aim for enduring practical impact."),
            ("Influence millions through software", {"IT":3}, "You want scalable digital influence."),
            ("Advance human knowledge", {"Science":3}, "You want intellectual contributions and discovery."),
            ("Shift culture via creative work", {"Arts":3}, "You aim to move people emotionally and culturally."),
        ]
    },
    {
        "question": "Pick a small project you’d enjoy:",
        "options": [
            ("Build a microcontroller robot", {"Engineering":3}, "You enjoy embedded systems and control tasks."),
            ("Create a data-driven web dashboard", {"IT":3}, "You like shaping information for users."),
            ("Design and run a small experiment", {"Science":3}, "Experimental design appeals to you."),
            ("Produce a short film or animation", {"Arts":3}, "Storytelling through media energizes you."),
        ]
    },
    {
        "question": "How do you approach ambiguous tasks?",
        "options": [
            ("Prototype to find workable constraints", {"Engineering":3}, "You use practical iteration to reduce uncertainty."),
            ("Build minimal viable features to test ideas", {"IT":3}, "You validate via quick digital experiments."),
            ("Form hypotheses and test them", {"Science":3}, "You reduce ambiguity with controlled inquiry."),
            ("Explore many concepts until one resonates", {"Arts":3}, "You embrace divergent exploration for innovation."),
        ]
    },
    {
        "question": "In ten years you'd most like to be known for:",
        "options": [
            ("Engineering innovations that solve real problems", {"Engineering":3}, "You aim to translate knowledge into useful systems."),
            ("Transformative software or AI systems", {"IT":3}, "You want to shape digital experiences at scale."),
            ("Meaningful scientific discoveries", {"Science":3}, "You want to push the frontier of knowledge."),
            ("Enduring artistic works that influence culture", {"Arts":3}, "You want creative legacy and cultural impact."),
        ]
    }
]

# Categories and metadata to present detailed capabilities
categories = ["Engineering", "IT", "Science", "Arts"]
category_colors = {
    "Engineering": "#FF6B6B",
    "IT": "#796AEE",
    "Science": "#F9A826",
    "Arts": "#4ECDC4"
}
category_emojis = {
    "Engineering": "🔧",
    "IT": "💻",
    "Science": "🔬",
    "Arts": "🎨"
}

capabilities = {
    "Engineering": [
        "System design & prototyping",
        "Applied mechanics & manufacturing understanding",
        "Practical problem-solving & testing",
        "Cross-disciplinary product development"
    ],
    "IT": [
        "Software architecture & development",
        "Data systems and analytics",
        "Automation & scalable engineering",
        "AI/ML model application"
    ],
    "Science": [
        "Experimental design & statistical reasoning",
        "Critical analysis & reproducibility",
        "Domain-specific research expertise",
        "Hypothesis-driven investigation"
    ],
    "Arts": [
        "Visual storytelling & composition",
        "Creative ideation & concept development",
        "User-centered aesthetics & UX sensibility",
        "Multimedia production & direction"
    ]
}

# Professional interpretations for options are in the questions structure (third field)

# ---------------- SESSION STATE ----------------
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}  # q_idx -> selected_option_index
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "reasons_list" not in st.session_state:
    st.session_state.reasons_list = []  # list of (q_text, chosen_text, interpretive_reason)

# ---------------- HELPERS ----------------
def calculate_scores():
    scores = {c: 0 for c in categories}
    for q_idx, opt_idx in st.session_state.answers.items():
        _, score_map, reason_text = questions[q_idx]["options"][opt_idx]
        for k, v in score_map.items():
            if k in scores:
                scores[k] += v
    return scores

def record_reason(q_idx, opt_idx):
    q_text = questions[q_idx]["question"]
    opt_text, _, reason_text = questions[q_idx]["options"][opt_idx]
    st.session_state.reasons_list.append((q_text, opt_text, reason_text))

# ---------------- UI: Header ----------------
st.markdown("<div class='panel'>", unsafe_allow_html=True)
st.markdown("<div class='hero-title'>🧭 Quantum Quest — Futuristic</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Deep interest-to-career simulation · professional insights delivered after mission analysis</div>", unsafe_allow_html=True)

# ---------------- MAIN FLOW ----------------
if not st.session_state.show_results:
    # Show current question card with smooth transition simulation
    q_idx = st.session_state.q_idx
    q_obj = questions[q_idx]
    st.markdown("<div class='qcard'>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-text'>Q{q_idx+1} / {len(questions)} — {q_obj['question']}</div>", unsafe_allow_html=True)

    # Options as buttons — one column
    # We'll use a container to allow a little "fade" effect using placeholder
    for i, (opt_text, score_map, reason_text) in enumerate(q_obj["options"]):
        btn_key = f"q{q_idx}_opt{i}"
        if st.button(opt_text, key=btn_key):
            # record choice
            st.session_state.answers[q_idx] = i
            record_reason(q_idx, i)
            # Smooth transition: brief placeholder message before moving on
            placeholder = st.empty()
            placeholder.markdown("<div style='padding:8px;color:#bcd6ff;'>Processing choice...</div>", unsafe_allow_html=True)
            time.sleep(0.28)  # short pause for smooth feeling
            placeholder.empty()
            # next question or results
            if q_idx + 1 < len(questions):
                st.session_state.q_idx += 1
            else:
                st.session_state.show_results = True
            # rerun to refresh content
            st.experimental_rerun()

    # custom white progress bar
    progress_pct = int((st.session_state.q_idx / len(questions)) * 100)
    # outer + inner divs
    st.markdown(
        f"""
        <div style='margin-top:12px;'>
            <div class='progress-outer'>
                <div class='progress-inner' style='width:{progress_pct}%;'></div>
            </div>
            <div class='progress-label'>{st.session_state.q_idx} of {len(questions)} completed — {progress_pct}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # show nothing else inside card
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ------------------ RESULTS / ROCKET SEQUENCE ------------------
    # Run a staged analysis: show log entries and progress to feel like a launch
    st.markdown("<div class='result-hero'><h3>🛰️ Initiating Quantum Analysis Pipeline...</h3></div>", unsafe_allow_html=True)
    # quick staged progress (visual)
    p = st.progress(0)
    for stage in range(4):
        # each stage increments
        for i in range(25):
            p.progress((stage*25 + i + 1))
            time.sleep(0.01)
    p.empty()
    st.markdown("<div class='result-hero'><strong>🔭 Analysis complete — presenting your mission debrief</strong></div>", unsafe_allow_html=True)
    st.write("")  # spacing

    # compute scores
    scores = calculate_scores()
    # present top categories
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_possible = 3 * len(questions)  # max per category if all map there
    # Top 3
    top3 = sorted_scores[:3]

    # Top summary card
    top_cat, top_score = top3[0]
    st.markdown(f"""
        <div class='result-card'>
            <h2 style='margin:4px 0 8px 0;'>{category_emojis[top_cat]} Top Domain: <strong>{top_cat}</strong></h2>
            <div class='small'>You demonstrate a strong alignment with <strong>{top_cat}</strong>-oriented roles. Below you will find a structured breakdown of what that alignment means and practical careers & capabilities to consider.</div>
        </div>
    """, unsafe_allow_html=True)

    # Capabilities block
    st.markdown("<div class='result-card'><h3>🛠️ Core Capabilities Indicated</h3>", unsafe_allow_html=True)
    caps = capabilities[top_cat]
    st.write("")  # spacing
    for c in caps:
        st.markdown(f"- {c}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Suggested roles and capability ladder
    st.markdown("<div class='result-card'><h3>🎯 Suggested Career Paths & What You Bring</h3>", unsafe_allow_html=True)
    roles = {
        "Engineering": ["Mechanical Engineer", "Product Design Engineer", "Robotics Engineer", "Embedded Systems Engineer"],
        "IT": ["Software Developer", "Data Engineer", "ML Engineer", "Site Reliability Engineer"],
        "Science": ["Research Scientist", "Lab Technician", "Environmental Researcher", "Clinical Researcher"],
        "Arts": ["Graphic Designer", "Animator/Director", "Creative Director", "Multimedia Producer"]
    }
    for r in roles[top_cat]:
        st.markdown(f"- **{r}** — a role where your strengths can be exercised and grown.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Score visualization (matplotlib for style)
    st.markdown("<div class='result-card'><h3>📊 Quantum Fit Scores</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(list(scores.items()), columns=["Category", "Score"]).set_index("Category")
    fig, ax = plt.subplots(figsize=(6, 3))
    cats = df.index.tolist()
    vals = df['Score'].tolist()
    bar_colors = [category_colors[c] for c in cats]
    bars = ax.barh(cats, vals, color=bar_colors)
    ax.invert_yaxis()
    ax.set_xlabel("Score")
    ax.set_xlim(0, max(vals) + 3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_title("Alignment Scores")
    for i, v in enumerate(vals):
        ax.text(v + 0.2, i, str(v), color='white', va='center', fontweight='600')
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Professional Reason Report (per-question)
    st.markdown("<div class='result-card'><h3>🔎 Reason Report — Why each choice matters</h3><div class='small'>Below is a professional interpretation of every answer you selected. This helps you see how each preference maps to career capabilities.</div>", unsafe_allow_html=True)
    for idx, (q_text, opt_text, reason_text) in enumerate(st.session_state.reasons_list):
        st.markdown(f"<div style='margin-top:8px;'><b>Q{idx+1}:</b> {q_text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='reason-box'><b>Your choice:</b> {opt_text}<br/><b>Interpretation:</b> {reason_text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Final recommendations and next steps
    st.markdown("<div class='result-card'><h3>🧭 Strategic Next Steps</h3>", unsafe_allow_html=True)
    # Give tailored next steps for each top 3
    for rank, (cat, sc) in enumerate(top3, start=1):
        st.markdown(f"**{rank}. {category_emojis[cat]} {cat} (score: {sc})**")
        if cat == "Engineering":
            st.markdown("- Explore hands-on maker projects (Arduino/robotics).")
            st.markdown("- Learn CAD & basic electronics. Consider internships in product or design labs.")
        elif cat == "IT":
            st.markdown("- Build small full-stack projects and learn data structures.")
            st.markdown("- Explore cloud platforms, and get comfortable with Python and version control.")
        elif cat == "Science":
            st.markdown("- Join research labs or science clubs; learn experimental design and statistics.")
            st.markdown("- Take courses that deepen understanding of the scientific method & domain knowledge.")
        elif cat == "Arts":
            st.markdown("- Build a portfolio, practice critique cycles, and collaborate on creative projects.")
            st.markdown("- Learn production pipelines (video, animation, UX tools) and showcase work.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Telemetry / stage log (small)
    st.markdown("<div class='small' style='margin-top:10px;'>Telemetry: Quantum pipeline executed — results are probabilistic and aligned to stated interests.</div>", unsafe_allow_html=True)

    # Celebratory visual & retake
    st.balloons()
    if st.button("🔁 Retake Quantum Quest"):
        # reset
        st.session_state.q_idx = 0
        st.session_state.answers = {}
        st.session_state.reasons_list = []
        st.session_state.show_results = False
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close panel
