# quantum_quest_render.py
import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Quest", page_icon="🧭", layout="centered")

# ---------------- CSS: Futuristic dark + readable option buttons ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp {
  height:100%;
  background: radial-gradient(circle at 10% 10%, #071026 0%, #081228 40%, #08121a 100%);
  color: #e6f0ff;
  font-family: 'Inter', sans-serif;
}

.panel {
  max-width: 920px;
  margin: 28px auto;
  padding: 22px;
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  box-shadow: 0 10px 40px rgba(2,6,23,0.7);
  border: 1px solid rgba(255,255,255,0.03);
}

/* Header */
.hero-title {
  text-align:center;
  font-size:40px;
  font-weight:800;
  color: #e8f7ff;
  margin-bottom:4px;
}
.hero-sub {
  text-align:center;
  color:#9fb3d8;
  margin-bottom:18px;
}

/* Question card */
.qcard {
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid rgba(79,139,255,0.18);
  margin-bottom: 12px;
}
.question-text {
  font-size:18px;
  font-weight:600;
  color:#e8f6ff;
  margin-bottom:12px;
}

/* Option button - DARK background with WHITE text so options are visible */
.opt-btn {
  width:100%;
  padding:12px 14px;
  margin:8px 0;
  border-radius:10px;
  border:1px solid rgba(255,255,255,0.04);
  background: linear-gradient(90deg,#0f2a4a,#13283f);
  color:#ffffff !important;
  text-align:left;
  font-weight:500;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.opt-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(7,9,37,0.6);
  border-color: rgba(79,139,255,0.28);
}

/* White progress bar */
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

/* Results styling */
.result-hero {
  background: linear-gradient(90deg, rgba(79,139,255,0.12), rgba(124,77,255,0.08));
  padding: 12px;
  border-radius: 10px;
  text-align:center;
  margin-bottom:12px;
}
.result-card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid rgba(255,255,255,0.03);
}
.small { color:#9fb3d8; font-size:13px; }
.reason-box { background: rgba(255,255,255,0.02); padding:10px; border-radius:8px; margin-top:8px; color:#dbefff; }
</style>
""", unsafe_allow_html=True)

# ---------------- Questions (15) ----------------
# Each option: (text, {category:points}, professional_reason)
questions = [
    {"question":"When solving a problem, what do you do first?",
     "options":[
         ("Sketch or design a physical solution", {"Engineering":3}, "Shows system design thinking and mechanical intuition."),
         ("Plan a software-based solution", {"IT":3}, "Shows algorithmic and systems-oriented thinking."),
         ("Form a hypothesis and test it", {"Science":3}, "Shows experimental and analytical mindset."),
         ("Create visual or narrative concepts", {"Arts":3}, "Shows creative ideation and visual reasoning.")
     ]},
    {"question":"Which class excited you most in school?",
     "options":[
         ("Physics/Math", {"Engineering":3}, "Strong quantitative and analytical tendencies."),
         ("Computer Science", {"IT":3}, "Affinity for coding and computational logic."),
         ("Biology/Chemistry", {"Science":3}, "Interest in experimental methods and living systems."),
         ("Art/Music", {"Arts":3}, "Natural inclination toward creativity and expression.")
     ]},
    {"question":"On a weekend you prefer to:",
     "options":[
         ("Tinker with gadgets / build models", {"Engineering":3}, "Hands–on practical experimentation appeals to you."),
         ("Work on a coding project", {"IT":3}, "You enjoy iterative software development."),
         ("Read scientific articles / run experiments", {"Science":3}, "You prefer evidence-driven exploration."),
         ("Create art or media", {"Arts":3}, "You find expression through creative work.")
     ]},
    {"question":"Which outcome feels most rewarding?",
     "options":[
         ("A working prototype", {"Engineering":3}, "You value tangible, reliable results."),
         ("A deployed app or tool", {"IT":3}, "You value impactful software solutions."),
         ("A validated research result", {"Science":3}, "You value rigor and validation."),
         ("An emotive artwork", {"Arts":3}, "You value emotional resonance and aesthetics.")
     ]},
    {"question":"What tool would you pick first?",
     "options":[
         ("3D printer / tools", {"Engineering":3}, "Interest in fabrication and physical design."),
         ("Code editor / terminal", {"IT":3}, "Comfort with digital development environments."),
         ("Lab kit / instruments", {"Science":3}, "Inclination for measurement and precision."),
         ("Camera / design suite", {"Arts":3}, "Preference for creative production tools.")
     ]},
    {"question":"When leading a project, you usually:",
     "options":[
         ("Define technical specs & build", {"Engineering":2, "IT":1}, "You prefer technical leadership and execution."),
         ("Coordinate and assign tasks", {"IT":1, "Engineering":1, "Science":1}, "You show organizational and cross-functional skills."),
         ("Guide creative direction", {"Arts":2, "IT":1}, "You focus on vision and aesthetics."),
         ("Design experiments and verify", {"Science":2, "Engineering":1}, "You lead with methodical validation.")
     ]},
    {"question":"Which problem excites you most?",
     "options":[
         ("Improving mechanical efficiency", {"Engineering":3}, "Optimization in physical systems energizes you."),
         ("Scaling software systems", {"IT":3}, "You are drawn to architectural & scaling challenges."),
         ("Uncovering scientific patterns", {"Science":3}, "Systematic discovery motivates you."),
         ("Transforming ideas into visual stories", {"Arts":3}, "Narrative and visual impact inspire you.")
     ]},
    {"question":"Your ideal workplace is:",
     "options":[
         ("Workshop / lab / makerspace", {"Engineering":3}, "Hands-on labs are your natural habitat."),
         ("Tech startup / engineering team", {"IT":3}, "Dynamic software environments suit you."),
         ("Research lab or field site", {"Science":3}, "You flourish in investigative contexts."),
         ("Studio / creative collective", {"Arts":3}, "Creative collaboration fuels you.")
     ]},
    {"question":"You learn best by:",
     "options":[
         ("Building and iterating", {"Engineering":3}, "Learning through doing is effective for you."),
         ("Coding and small projects", {"IT":3}, "Project-based learning clarifies concepts."),
         ("Designing controlled experiments", {"Science":3}, "Systematic, reproducible methods fit you."),
         ("Workshops and critiques", {"Arts":3}, "Feedback-driven creative growth works best.")
     ]},
    {"question":"Which description fits your thinking?",
     "options":[
         ("Structured & systems oriented", {"Engineering":3}, "You decompose problems into components."),
         ("Algorithmic & logical", {"IT":3}, "You excel at pattern extraction and flow."),
         ("Hypothesis-led & meticulous", {"Science":3}, "You value careful validation."),
         ("Associative & expressive", {"Arts":3}, "You connect ideas through metaphor & imagery.")
     ]},
    {"question":"Which impact would you prefer to make?",
     "options":[
         ("Build durable infrastructure/products", {"Engineering":3}, "You aim for practical societal impact."),
         ("Create software used by millions", {"IT":3}, "Scalable digital impact motivates you."),
         ("Advance scientific understanding", {"Science":3}, "Contributing to knowledge drives you."),
         ("Shift culture through creative work", {"Arts":3}, "You pursue cultural influence via creativity.")
     ]},
    {"question":"Pick a mini-project you’d enjoy:",
     "options":[
         ("Assemble a simple robot", {"Engineering":3}, "Embedded systems & mechatronics fascinate you."),
         ("Publish a small web app", {"IT":3}, "Delivering functional software gives satisfaction."),
         ("Run a small experiment & analyze data", {"Science":3}, "Designing tests and interpreting results fits you."),
         ("Produce a short creative film", {"Arts":3}, "Storytelling via media energizes you.")
     ]},
    {"question":"How do you approach vague tasks?",
     "options":[
         ("Prototype to reveal constraints", {"Engineering":3}, "Iterative prototyping reduces uncertainty."),
         ("Create an MVP and iterate", {"IT":3}, "Lean experimentation provides feedback quickly."),
         ("Form hypotheses and test them", {"Science":3}, "Controlled inquiry clarifies ambiguity."),
         ("Explore many concepts to find resonance", {"Arts":3}, "Divergent exploration finds novel directions.")
     ]},
    {"question":"What kind of problems do you enjoy solving?",
     "options":[
         ("Mechanical / design problems", {"Engineering":3}, "You enjoy making tangible, functional solutions."),
         ("Software / data challenges", {"IT":3}, "You enjoy logical problem solving and data structures."),
         ("Scientific / investigative puzzles", {"Science":3}, "You like deep analytical challenges."),
         ("Creative / expressive tasks", {"Arts":3}, "You enjoy crafting emotional experiences.")
     ]},
    {"question":"In ten years, you'd like to be known for:",
     "options":[
         ("Engineering innovations that help people", {"Engineering":3}, "You aim for practical, scalable engineering outcomes."),
         ("Transformative software or platforms", {"IT":3}, "You want to shape digital experiences at scale."),
         ("Scientific discoveries that matter", {"Science":3}, "You aspire to research-driven influence."),
         ("Artistic works that inspire", {"Arts":3}, "You aim to create emotionally impactful art.")
     ]}
]

# categories metadata
categories = ["Engineering", "IT", "Science", "Arts"]
category_colors = {"Engineering":"#FF6B6B", "IT":"#796AEE", "Science":"#F9A826", "Arts":"#4ECDC4"}
category_emojis = {"Engineering":"🔧", "IT":"💻", "Science":"🔬", "Arts":"🎨"}

# ---------------- session state ----------------
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}  # q_idx -> opt_index
if "reasons" not in st.session_state:
    st.session_state.reasons = []  # list of (q_text, opt_text, reason_text)
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# helpers
def calculate_scores():
    scores = {c:0 for c in categories}
    for qidx, opt_idx in st.session_state.answers.items():
        _, score_map, _ = questions[qidx]["options"][opt_idx]
        for k,v in score_map.items():
            if k in scores:
                scores[k] += v
    return scores

def record_reason(qidx, opt_idx):
    q_text = questions[qidx]["question"]
    opt_text, _, reason_text = questions[qidx]["options"][opt_idx]
    st.session_state.reasons.append((q_text, opt_text, reason_text))

# ---------------- UI ----------------
st.markdown("<div class='panel'>", unsafe_allow_html=True)
st.markdown("<div class='hero-title'>🧭 Quantum Quest</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Futuristic career-interest diagnostic — professional insights delivered after analysis</div>", unsafe_allow_html=True)

if not st.session_state.show_result:
    qidx = st.session_state.q_idx
    qobj = questions[qidx]
    st.markdown("<div class='qcard'>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-text'>Q{qidx+1} / {len(questions)} — {qobj['question']}</div>", unsafe_allow_html=True)

    # one-column buttons; styled via CSS class .opt-btn
    for i, (opt_text, _, _) in enumerate(qobj["options"]):
        key = f"q{qidx}_opt{i}"
        # use st.button with HTML wrapper to apply the CSS class
        if st.button(opt_text, key=key):
            # record
            st.session_state.answers[qidx] = i
            record_reason(qidx, i)
            # small transition feel
            placeholder = st.empty()
            placeholder.markdown("<div style='padding:8px;color:#bcd6ff;'>Processing...</div>", unsafe_allow_html=True)
            time.sleep(0.28)
            placeholder.empty()
            if qidx + 1 < len(questions):
                st.session_state.q_idx += 1
            else:
                st.session_state.show_result = True
            st.experimental_rerun()

    # white progress bar
    progress_pct = int((st.session_state.q_idx / len(questions)) * 100)
    st.markdown(f"""
        <div style='margin-top:12px;'>
            <div class='progress-outer'>
                <div class='progress-inner' style='width:{progress_pct}%;'></div>
            </div>
            <div class='progress-label'>{st.session_state.q_idx} of {len(questions)} completed — {progress_pct}%</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close qcard

else:
    # results flow with simple rocket-ish staged progress
    st.markdown("<div class='result-hero'><h3>🛰️ Running Deep Analysis Pipeline...</h3></div>", unsafe_allow_html=True)
    p = st.progress(0)
    for i in range(100):
        p.progress((i+1)/100)
        time.sleep(0.01)
    p.empty()

    scores = calculate_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = sorted_scores[0][0]

    # Top summary
    st.markdown(f"<div class='result-card'><h2 style='margin:6px 0;'>{category_emojis[top]} Top Domain: <strong>{top}</strong></h2><div class='small'>The following report explains what your choices indicate about your capabilities and suggested paths.</div></div>", unsafe_allow_html=True)

    # Capabilities
    capabilities = {
        "Engineering":["System design & prototyping","Applied mechanics understanding","Testing & iteration","Product development skills"],
        "IT":["Software development","Data & systems thinking","Automation & scripting","Cloud & deployment basics"],
        "Science":["Experimental design","Statistical reasoning","Research methodology","Domain-specific knowledge building"],
        "Arts":["Visual storytelling","Creative ideation","UX & aesthetic sensibility","Media production"]
    }
    st.markdown("<div class='result-card'><h3>🔧 Core Capabilities You Demonstrate</h3>", unsafe_allow_html=True)
    for cap in capabilities[top]:
        st.markdown(f"- {cap}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Bar chart of scores
    st.markdown("<div class='result-card'><h3>📊 Alignment Scores</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(list(scores.items()), columns=["Category","Score"]).set_index("Category")
    fig, ax = plt.subplots(figsize=(6,3))
    cats = df.index.tolist()
    vals = df['Score'].tolist()
    bar_colors = [category_colors[c] for c in cats]
    bars = ax.barh(cats, vals, color=bar_colors)
    ax.invert_yaxis()
    ax.set_xlabel("Score")
    ax.set_xlim(0, max(vals)+2 if max(vals)>0 else 5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_title("Category Scores")
    for i, v in enumerate(vals):
        ax.text(v + 0.2, i, str(v), color='white', va='center', fontweight='600')
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Professional Reason Report (all questions with chosen option + reason)
    st.markdown("<div class='result-card'><h3>🔎 Reason Report</h3><div class='small'>Professional interpretation of your selected answers (why each choice maps to a capability)</div>", unsafe_allow_html=True)
    for idx, (q_text, opt_text, reason_text) in enumerate(st.session_state.reasons):
        st.markdown(f"<div style='margin-top:8px;'><b>Q{idx+1}:</b> {q_text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='reason-box'><b>Your choice:</b> {opt_text}<br/><b>Interpretation:</b> {reason_text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Suggested next steps (brief)
    st.markdown("<div class='result-card'><h3>🧭 Suggested Next Steps</h3>", unsafe_allow_html=True)
    if top == "Engineering":
        st.markdown("- Do hands-on maker projects (Arduino, tiny robotics).")
        st.markdown("- Learn CAD basics and electronics.")
    elif top == "IT":
        st.markdown("- Build small apps and learn Python thoroughly.")
        st.markdown("- Explore data structures, Git, and cloud basics.")
    elif top == "Science":
        st.markdown("- Join research labs, learn statistics and experimental design.")
        st.markdown("- Get comfortable with data analysis tools.")
    elif top == "Arts":
        st.markdown("- Create a small portfolio; practice critique cycles.")
        st.markdown("- Learn production tools (video, design, UX).")
    st.markdown("</div>", unsafe_allow_html=True)

    # Retake
    if st.button("🔁 Retake Quantum Quest"):
        st.session_state.q_idx = 0
        st.session_state.answers = {}
        st.session_state.reasons = []
        st.session_state.show_result = False
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close panel
