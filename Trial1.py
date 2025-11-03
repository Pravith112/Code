"""
Streamlit Career Interest Quiz - 15 questions

Run:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

This app asks 15 questions, accumulates points across 5 career categories:
Engineering, Arts, Management, Science, IT

After submitting, it shows:
- Top recommended career category
- Dynamic per-answer explanations ("You chose this because... -> indicating skills/interests -> suggested careers.")
- Full score breakdown with a chart
- Stylish UI with gradient background, cards, and emojis
"""

from typing import Dict, List
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Career Compass — 15Q Quiz", page_icon="🧭", layout="wide")

# ----------------------------
# Styling (gradient background, card styles)
# ----------------------------
st.markdown(
    """
    <style>
    :root{
      --card-bg: rgba(255,255,255,0.06);
      --glass: rgba(255,255,255,0.04);
      --accent: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
      --card-radius: 14px;
    }
    html, body, [data-testid="stAppViewContainer"] > .main {
      height: 100%;
    }
    body {
      background: radial-gradient(1200px 600px at 10% 10%, rgba(97,42,255,0.14), transparent 10%),
                  radial-gradient(1000px 500px at 90% 90%, rgba(37,117,252,0.10), transparent 10%),
                  linear-gradient(180deg, #0f172a 0%, #071022 100%);
      color: #e6eef8;
      font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .title {
      background: linear-gradient(90deg,#ffe259,#ffa751);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      font-weight:800;
    }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: var(--card-radius);
      padding: 18px;
      box-shadow: 0 6px 26px rgba(2,6,23,0.6);
      border: 1px solid rgba(255,255,255,0.03);
    }
    .result-card {
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 10px 40px rgba(2,6,23,0.7);
      border: 1px solid rgba(255,255,255,0.04);
    }
    .big-num {
      font-size: 34px;
      font-weight: 800;
    }
    .small {
      color: #c8d3e8;
      font-size: 13px;
    }
    .emoji {
      font-size: 26px;
      margin-right:8px;
    }
    .badge {
      display:inline-block;
      padding:6px 10px;
      border-radius:999px;
      background: linear-gradient(90deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.03);
      color:#e9f0ff;
      font-weight:600;
    }
    .muted { color: #9fb0d8; }
    .explain {
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 10px;
      border: 1px solid rgba(255,255,255,0.02);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Data: categories, emojis, suggested careers
# ----------------------------
CATEGORIES = ["Engineering", "Arts", "Management", "Science", "IT"]
EMOJI = {
    "Engineering": "🔧",
    "Arts": "🎨",
    "Management": "🧭",
    "Science": "🔬",
    "IT": "💻",
}
SUGGESTED_CAREERS = {
    "Engineering": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Product Engineer"],
    "Arts": ["Graphic Designer", "Illustrator", "Animator", "UX/UI Designer"],
    "Management": ["Project Manager", "Product Manager", "Operations Manager", "Business Analyst"],
    "Science": ["Research Scientist", "Lab Technician", "Data Scientist", "Environmental Scientist"],
    "IT": ["Software Developer", "Systems Admin", "DevOps Engineer", "Data Engineer"],
}

# ----------------------------
# Questions and options
# For each option we set:
# - label: text to show
# - scores: dict add scores to categories
# - explain: short explanation template (we will expand dynamically)
# ----------------------------
QUESTIONS = [
    {
        "q": "1) When you face a new problem, what do you enjoy most?",
        "opts": [
            {"label": "Designing practical solutions and prototypes", "scores": {"Engineering": 2, "IT": 1}, "explain": "You prefer building and iterating tangible solutions."},
            {"label": "Sketching or imagining creative concepts", "scores": {"Arts": 2}, "explain": "You like creative expression and visual thinking."},
            {"label": "Organizing steps, people and resources to solve it", "scores": {"Management": 2}, "explain": "You naturally plan, coordinate, and lead."},
            {"label": "Reading scientific papers and testing hypotheses", "scores": {"Science": 2}, "explain": "You enjoy rigorous investigation and experimentation."},
        ],
    },
    {
        "q": "2) Which activity sounds most like fun to you on a free weekend?",
        "opts": [
            {"label": "Tinkering with gadgets or building things", "scores": {"Engineering": 2, "IT": 1}, "explain": "Hands-on construction and technology excite you."},
            {"label": "Painting, playing music or crafting", "scores": {"Arts": 2}, "explain": "Artistic creation brings you joy."},
            {"label": "Organizing events or leading a volunteer team", "scores": {"Management": 2}, "explain": "You enjoy coordinating people and activities."},
        ],
    },
    {
        "q": "3) What school subject did you enjoy most?",
        "opts": [
            {"label": "Math and physics", "scores": {"Engineering": 2, "Science": 1}, "explain": "You enjoy quantitative problem solving."},
            {"label": "Literature, art, or music", "scores": {"Arts": 2}, "explain": "You connect with language and aesthetics."},
            {"label": "Computer science or coding", "scores": {"IT": 2, "Engineering": 1}, "explain": "You like logical systems and automation."},
            {"label": "Biology and chemistry", "scores": {"Science": 2}, "explain": "You are drawn to living systems and experiments."},
        ],
    },
    {
        "q": "4) How do you prefer to work?",
        "opts": [
            {"label": "On long technical projects that require precision", "scores": {"Engineering": 2, "Science": 1}, "explain": "You value depth and meticulous work."},
            {"label": "On creative short-term projects with fast feedback", "scores": {"Arts": 2}, "explain": "You like variety and expressive output."},
            {"label": "Leading a team and coordinating deliveries", "scores": {"Management": 2}, "explain": "You prefer leadership and alignment."},
            {"label": "Building software or scripts that automate tasks", "scores": {"IT": 2}, "explain": "You enjoy solving problems with code."},
        ],
    },
    {
        "q": "5) Which tool would you most enjoy learning deeply?",
        "opts": [
            {"label": "CAD and prototyping tools", "scores": {"Engineering": 2}, "explain": "You like designing and prototyping physical things."},
            {"label": "Digital painting or 3D art software", "scores": {"Arts": 2}, "explain": "You want to develop creative technical skills."},
            {"label": "Project management platforms and people skills", "scores": {"Management": 2}, "explain": "You want to organize teams and projects."},
            {"label": "Databases, cloud platforms or programming languages", "scores": {"IT": 2, "Science": 1}, "explain": "You are interested in systems and data."},
        ],
    },
    {
        "q": "6) In a team, what role do you naturally take?",
        "opts": [
            {"label": "The technical problem-solver", "scores": {"Engineering": 2, "IT": 1}, "explain": "You jump to fix technical challenges."},
            {"label": "The creative idea person", "scores": {"Arts": 2}, "explain": "You bring fresh, creative perspectives."},
            {"label": "The organizer who delegates and tracks progress", "scores": {"Management": 2}, "explain": "You keep things moving and aligned."},
            {"label": "The researcher who collects evidence and tests", "scores": {"Science": 2}, "explain": "You validate ideas through testing."},
        ],
    },
    {
        "q": "7) Which of these outcomes would feel most rewarding?",
        "opts": [
            {"label": "A durable product or structure that works reliably", "scores": {"Engineering": 2}, "explain": "You value robustness and function."},
            {"label": "An emotional, beautiful piece that moves people", "scores": {"Arts": 2}, "explain": "You value expression and audience impact."},
            {"label": "A smoothly run team that met its goals", "scores": {"Management": 2}, "explain": "You value coordination and results."},
            {"label": "A discovery or finding that advances knowledge", "scores": {"Science": 2}, "explain": "You value insight and evidence."},
        ],
    },
    {
        "q": "8) When learning, you prefer:",
        "opts": [
            {"label": "Step-by-step practical tutorials", "scores": {"IT": 2, "Engineering": 1}, "explain": "You like hands-on guided learning."},
            {"label": "Open-ended creative assignments", "scores": {"Arts": 2}, "explain": "You learn by exploring and expressing."},
            {"label": "Case studies and leadership scenarios", "scores": {"Management": 2}, "explain": "You learn by seeing systems and decisions."},
            {"label": "Research papers and experiments", "scores": {"Science": 2}, "explain": "You favor methodical and evidence-driven study."},
        ],
    },
    {
        "q": "9) Which environment sounds best?",
        "opts": [
            {"label": "A lab or field site running experiments", "scores": {"Science": 2}, "explain": "You like investigative, empirical settings."},
            {"label": "A studio or creative workshop", "scores": {"Arts": 2}, "explain": "You thrive in expressive and flexible spaces."},
            {"label": "A product development floor with machines and tools", "scores": {"Engineering": 2}, "explain": "You enjoy making and improving products."},
            {"label": "A fast-paced office with servers and code", "scores": {"IT": 2}, "explain": "You prefer tech-driven environments."},
        ],
    },
    {
        "q": "10) Which task would you volunteer for?",
        "opts": [
            {"label": "Fixing a malfunctioning system", "scores": {"Engineering": 2, "IT": 1}, "explain": "You enjoy troubleshooting and repair."},
            {"label": "Creating promotional visuals or a brand", "scores": {"Arts": 2}, "explain": "You enjoy crafting a visual message."},
            {"label": "Leading a cross-team initiative", "scores": {"Management": 2}, "explain": "You enjoy rallying people around goals."},
            {"label": "Designing an experiment to test an idea", "scores": {"Science": 2}, "explain": "You prefer planned inquiry and measurement."},
        ],
    },
    {
        "q": "11) What kind of feedback motivates you most?",
        "opts": [
            {"label": "Technical correctness and performance metrics", "scores": {"Engineering": 2, "Science": 1}, "explain": "You value measurable excellence."},
            {"label": "Emotional reactions and audience responses", "scores": {"Arts": 2}, "explain": "You are driven by human connection."},
            {"label": "Team success and stakeholder praise", "scores": {"Management": 2}, "explain": "You value collaborative achievement."},
            {"label": "Functional reliability and uptime", "scores": {"IT": 2}, "explain": "You are motivated by system stability."},
        ],
    },
    {
        "q": "12) When reading about careers, you get most excited by:",
        "opts": [
            {"label": "Stories of invention and large-scale infrastructure", "scores": {"Engineering": 2}, "explain": "You enjoy creating things that scale."},
            {"label": "Profiles of artists and creators who moved people", "scores": {"Arts": 2}, "explain": "Human expression inspires you."},
            {"label": "Leaders who turned teams into high-performance units", "scores": {"Management": 2}, "explain": "Leadership journeys interest you."},
            {"label": "Researchers who discovered new phenomena", "scores": {"Science": 2}, "explain": "Discovery and new knowledge compel you."},
            {"label": "Engineers who built impactful software systems", "scores": {"IT": 2}, "explain": "Systems and software innovation excite you."},
        ],
    },
    {
        "q": "13) Which word describes you best?",
        "opts": [
            {"label": "Analytical", "scores": {"Engineering": 2, "Science": 1}, "explain": "You think logically and break problems down."},
            {"label": "Expressive", "scores": {"Arts": 2}, "explain": "You communicate with style and feeling."},
            {"label": "Organized", "scores": {"Management": 2}, "explain": "You bring clarity and structure."},
            {"label": "Curious", "scores": {"Science": 2, "IT": 1}, "explain": "You want to learn how things work."},
        ],
    },
    {
        "q": "14) What's your tolerance for ambiguity in projects?",
        "opts": [
            {"label": "Low — I like clear specs and constraints", "scores": {"Engineering": 2, "Management": 1}, "explain": "You prefer well-defined problems."},
            {"label": "High — I thrive with open briefs", "scores": {"Arts": 2}, "explain": "You enjoy shaping vague briefs into ideas."},
            {"label": "Moderate — I set milestones and adapt", "scores": {"Management": 2}, "explain": "You balance structure with flexibility."},
            {"label": "I enjoy exploring unknowns to find answers", "scores": {"Science": 2}, "explain": "You embrace open-ended inquiry."},
        ],
    },
    {
        "q": "15) How do you imagine your ideal career in 10 years?",
        "opts": [
            {"label": "Leading technical projects or building products", "scores": {"Engineering": 2, "Management": 1}, "explain": "You want to shape technical outcomes and possibly lead teams."},
            {"label": "Being a recognized creative professional", "scores": {"Arts": 2}, "explain": "You aspire to be known for your creative work."},
            {"label": "Running teams or businesses", "scores": {"Management": 2}, "explain": "You see yourself steering organizations."},
            {"label": "Advancing knowledge or solving scientific challenges", "scores": {"Science": 2}, "explain": "You want to contribute to discovery."},
            {"label": "Building complex software systems and products", "scores": {"IT": 2}, "explain": "You foresee a career in technology and systems."},
        ],
    },
]

# ----------------------------
# Helpers
# ----------------------------
def init_state():
    # Ensure every question key exists in session_state
    for i in range(len(QUESTIONS)):
        key = f"q{i+1}"
        if key not in st.session_state:
            st.session_state[key] = None
    if "results" not in st.session_state:
        st.session_state["results"] = None


def compute_scores(answers: Dict[str, int]) -> Dict[str, int]:
    totals = {c: 0 for c in CATEGORIES}
    for q_idx, opt_idx in answers.items():
        if opt_idx is None:
            continue
        question = QUESTIONS[q_idx]
        option = question["opts"][opt_idx]
        for cat, pts in option["scores"].items():
            totals[cat] = totals.get(cat, 0) + pts
    return totals


def build_dynamic_explanation(q_idx: int, opt_idx: int) -> str:
    q = QUESTIONS[q_idx]
    opt = q["opts"][opt_idx]
    # Which categories got points from this option
    cats = [cat for cat, pts in opt["scores"].items() if pts > 0]
    cats_str = ", ".join([f"{EMOJI.get(c,'')} {c}" for c in cats])
    suggested = []
    for c in cats:
        suggested.extend(SUGGESTED_CAREERS.get(c, [])[:3])
    # Deduplicate suggested careers while preserving order
    seen = set()
    suggested_unique = [s for s in suggested if not (s in seen or seen.add(s))]
    suggested_str = ", ".join(suggested_unique[:5])
    explanation = (
        f"You chose: \"{opt['label']}\" — {opt.get('explain','')}\n\n"
        f"→ This maps to: {cats_str}.\n"
        f"→ What it indicates: interest/skills in {', '.join(cats)}.\n"
        f"→ Suggested career directions: {suggested_str}."
    )
    return explanation


def format_score_cards(totals: Dict[str, int], top_cats: List[str]):
    # Return list of dict for display
    cards = []
    max_score = max(totals.values()) if totals else 0
    for cat in CATEGORIES:
        score = totals.get(cat, 0)
        highlight = cat in top_cats
        pct = int((score / max_score * 100) if max_score > 0 else 0)
        cards.append(
            {
                "category": cat,
                "emoji": EMOJI.get(cat, ""),
                "score": score,
                "pct": pct,
                "suggested": SUGGESTED_CAREERS.get(cat, [])[:3],
                "highlight": highlight,
            }
        )
    return cards


# ----------------------------
# App layout
# ----------------------------
init_state()

with st.container():
    st.markdown('<div style="display:flex;align-items:center;gap:14px">', unsafe_allow_html=True)
    st.markdown('<div style="flex:1">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">Career Compass — 15-question Interest Quiz 🧭</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:right;"><span class="badge">Quick • Visual • Personalized</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="small">Answer 15 short questions — honest first answers give the best hint about careers that fit your interests and strengths.</p>', unsafe_allow_html=True)

st.write("")  # spacer

# Display question cards in a two-column layout for readability
cols = st.columns(2)
for i, q in enumerate(QUESTIONS):
    col = cols[i % 2]
    key = f"q{i+1}"
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<strong style='font-size:16px'>Q{i+1}.</strong> <span style='margin-left:8px'>{q['q']}</span>", unsafe_allow_html=True)
        # Build options labels
        option_labels = [opt["label"] for opt in q["opts"]]
        # Use radio buttons with a clear key
        selected = st.radio("", option_labels, index=st.session_state[key] if st.session_state[key] is not None else 0, key=key, label_visibility="collapsed")
        # save index
        st.session_state[key] = option_labels.index(selected)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")  # small gap

st.write("")  # spacer

# Submit area
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<strong>Ready?</strong> Click Submit when you've answered all questions to see your personalized results.", unsafe_allow_html=True)
all_answered = all(st.session_state[f"q{i+1}"] is not None for i in range(len(QUESTIONS)))
if not all_answered:
    st.warning("Please answer every question before submitting. (Scroll up to finish any unanswered questions.)")
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Submit • Show Results", use_container_width=True):
        if not all_answered:
            st.warning("You must answer all questions before submitting.")
        else:
            # gather answers mapping q_idx -> opt_idx
            answers = {i: st.session_state[f"q{i+1}"] for i in range(len(QUESTIONS))}
            totals = compute_scores(answers)
            # Determine top recommended category/cats
            max_score = max(totals.values())
            top_cats = [cat for cat, s in totals.items() if s == max_score]
            # Build per-question explanations
            per_q_explanations = []
            for q_idx, opt_idx in answers.items():
                expl = build_dynamic_explanation(q_idx, opt_idx)
                per_q_explanations.append({"q": QUESTIONS[q_idx]["q"], "explanation": expl})
            # Save in session_state
            st.session_state["results"] = {
                "totals": totals,
                "top": top_cats,
                "per_q": per_q_explanations,
            }
            st.experimental_rerun()
with col2:
    st.write("")  # intentionally blank to align button

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Show results if available
# ----------------------------
if st.session_state.get("results"):
    results = st.session_state["results"]
    totals = results["totals"]
    top_cats = results["top"]

    st.write("")  # spacer
    # Header result card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center">', unsafe_allow_html=True)
    left, right = st.columns([3, 1])
    with left:
        if len(top_cats) == 1:
            primary = top_cats[0]
            st.markdown(f"<div style='display:flex;align-items:center;gap:12px'><div class='emoji'>{EMOJI.get(primary)}</div><div><div class='big-num'>{primary}</div><div class='muted'>Top recommended career area for you</div></div></div>", unsafe_allow_html=True)
            st.markdown(f"<p class='small'>Why: Your answers collectively show a stronger tilt toward <strong>{primary}</strong>. Here are some roles you might explore: <strong>{', '.join(SUGGESTED_CAREERS.get(primary, [])[:4])}</strong>.</p>", unsafe_allow_html=True)
        else:
            # tie
            tops = ", ".join([f"{EMOJI.get(c,'')}{c}" for c in top_cats])
            st.markdown(f"<div style='display:flex;flex-direction:column;gap:6px'><div class='big-num'>Multiple strong fits</div><div class='muted'>You have a tie between: {tops}</div></div>", unsafe_allow_html=True)
            # show combined suggestions
            combined = []
            for c in top_cats:
                combined.extend(SUGGESTED_CAREERS.get(c, [])[:3])
            seen = set()
            combined_unique = [s for s in combined if not (s in seen or seen.add(s))]
            st.markdown(f"<p class='small'>Explore careers like: <strong>{', '.join(combined_unique[:6])}</strong>.</p>", unsafe_allow_html=True)

    with right:
        # Show overall numeric summary
        total_points = sum(totals.values())
        st.markdown(f"<div style='text-align:right'><div class='badge'>Total points: {total_points}</div></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # spacer

    # Score cards grid
    cards = format_score_cards(totals, top_cats)
    card_cols = st.columns(5)
    for i, card in enumerate(cards):
        col = card_cols[i % 5]
        with col:
            highlight_style = "border: 2px solid rgba(255,255,255,0.08);" if card["highlight"] else ""
            st.markdown(f"<div class='card' style='text-align:center; {highlight_style}'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:20px;font-weight:700'>{card['emoji']} {card['category']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:28px;font-weight:800;margin-top:6px'>{card['score']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='small'>Top roles: {', '.join(card['suggested'])}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # spacer

    # Bar chart for breakdown
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<strong>Full score breakdown</strong>", unsafe_allow_html=True)
    df = pd.DataFrame({"Category": list(totals.keys()), "Points": list(totals.values())})
    df = df.sort_values("Points", ascending=False)
    st.bar_chart(data=df.set_index("Category"))
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # spacer

    # Per-question explanations (collapsible)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<strong>Why each answer matters</strong>", unsafe_allow_html=True)
    for i, pq in enumerate(results["per_q"]):
        with st.expander(f"Q{i+1}: {QUESTIONS[i]['q']}", expanded=False):
            st.markdown(f"<div class='explain'>{pq['explanation']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # spacer

    # Next steps and suggestions
    st.markdown(
        """
        <div class="card">
        <strong>Next steps</strong>
        <ul class="small">
          <li>Explore the suggested roles above — try informational interviews or short courses.</li>
          <li>If you had a tie, consider projects that combine those areas (e.g., UX engineering = Engineering + Arts).</li>
          <li>Use this quiz as a directional guide — not a definitive label. Your experience and values matter too.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # spacer

    # Allow reset
    if st.button("Reset answers & retake quiz"):
        for i in range(len(QUESTIONS)):
            st.session_state[f"q{i+1}"] = None
        st.session_state["results"] = None
        st.experimental_rerun()
