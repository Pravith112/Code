import streamlit as st

st.set_page_config(page_title="Career Interest Quiz", page_icon="🎯", layout="wide")

# Gradient background using markdown
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(120deg, #89f7fe, #66a6ff);
        color: #000000;
    }
    .card {
        background-color: #ffffffcc;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🎯 Career Interest Quiz")
st.subheader("Discover the fields that match your interests and skills!")

# Initialize scores and explanations
score = {"Engineering":0, "Arts":0, "Management":0, "Science":0, "IT":0}
explanations = []

# Questions and mapping
questions = [
    {"q":"Do you enjoy solving numbers and logical problems?", "options":{"Yes":"Engineering", "No":"Arts"}, "reason":{"Yes":"You enjoy analytical thinking.","No":"You prefer creative work."}},
    {"q":"Do you like leading a team or organizing events?", "options":{"Yes":"Management", "No":"Arts"}, "reason":{"Yes":"You are a natural leader.","No":"You enjoy individual/creative tasks."}},
    {"q":"Do you enjoy creative activities like drawing or designing?", "options":{"Yes":"Arts", "No":"Engineering"}, "reason":{"Yes":"You have strong creative skills.","No":"You lean towards technical/logical work."}},
    {"q":"Do you enjoy programming or working with computers?", "options":{"Yes":"IT", "No":"Management"}, "reason":{"Yes":"You have interest in technology.","No":"You prefer people/organizational work."}},
    {"q":"Do you like experimenting and discovering new things?", "options":{"Yes":"Science", "No":"Arts"}, "reason":{"Yes":"You have curiosity and scientific mindset.","No":"You prefer creative/arts approach."}},
    {"q":"Do you prefer working with machines or gadgets?", "options":{"Yes":"Engineering", "No":"Arts"}, "reason":{"Yes":"Hands-on technical work suits you.","No":"Creative/soft skills are your strength."}},
    {"q":"Do you enjoy writing, blogging, or creating content?", "options":{"Yes":"Arts", "No":"Science"}, "reason":{"Yes":"You have strong communication/creative skills.","No":"You lean towards analytical/scientific work."}},
    {"q":"Do you like solving real-world problems practically?", "options":{"Yes":"Engineering", "No":"IT"}, "reason":{"Yes":"Practical problem solving is your strength.","No":"You prefer theoretical/IT work."}},
    {"q":"Do you enjoy data analysis or research?", "options":{"Yes":"Science", "No":"Management"}, "reason":{"Yes":"You have investigative and analytical skills.","No":"You enjoy organizational/people skills."}},
    {"q":"Do you like managing projects and schedules?", "options":{"Yes":"Management", "No":"Arts"}, "reason":{"Yes":"You have leadership and planning skills.","No":"You prefer creative tasks."}},
    {"q":"Do you enjoy learning about software and apps?", "options":{"Yes":"IT", "No":"Science"}, "reason":{"Yes":"Tech-savvy and IT inclined.","No":"You enjoy lab/science work."}},
    {"q":"Do you enjoy drawing, painting, or crafts?", "options":{"Yes":"Arts", "No":"Engineering"}, "reason":{"Yes":"Strong artistic talent.","No":"You prefer technical/logical work."}},
    {"q":"Do you like understanding how things work technically?", "options":{"Yes":"Engineering", "No":"Arts"}, "reason":{"Yes":"Engineering and technical work fits you.","No":"Creative/artistic skills are stronger."}},
    {"q":"Do you enjoy planning strategies and solving organizational problems?", "options":{"Yes":"Management", "No":"IT"}, "reason":{"Yes":"Leadership and strategy are your strengths.","No":"You enjoy technology-based tasks."}},
    {"q":"Do you like scientific experiments and lab work?", "options":{"Yes":"Science", "No":"Arts"}, "reason":{"Yes":"Curious and analytical mindset suits science.","No":"Creative/artistic skills dominate."}}
]

# User answers
answers = []
st.write("Answer the following questions:")

for i, q in enumerate(questions):
    st.markdown(f"<div class='card'><b>Q{i+1}: {q['q']}</b></div>", unsafe_allow_html=True)
    ans = st.radio("Choose an option:", list(q["options"].keys()), key=f"q{i}")
    answers.append(ans)

# Show results
if st.button("Submit"):
    feedback = []
    for i, ans in enumerate(answers):
        category = questions[i]["options"][ans]
        score[category] += 1
        feedback.append(f"**Q{i+1}: {questions[i]['q']}**\n- Your choice: {ans}\n- Reason: {questions[i]['reason'][ans]} ✅")

    recommended = max(score, key=score.get)

    st.markdown(f"<h2 style='color:#ff5733'>🎉 Based on your interests, you should explore: {recommended} careers!</h2>", unsafe_allow_html=True)
    
    st.subheader("💡 Detailed Analysis by Question:")
    for f in feedback:
        st.markdown(f"<div class='card'>{f}</div>", unsafe_allow_html=True)
    
    st.subheader("📊 Your Score by Career Category:")
    for cat, val in score.items():
        st.progress(val/15)  # visual bar
        st.write(f"{cat}: {val} points")
