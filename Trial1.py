import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Career Interest Quiz", page_icon="🚀", layout="wide")

# Custom CSS for gradient background and modern UI
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .result-card {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .emoji {
        font-size: 2em;
    }
    .question {
        font-weight: bold;
        color: #f0f0f0;
    }
    .option {
        color: #e0e0e0;
    }
    .submit-btn {
        background: #ff6b6b;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.2em;
    }
    .explanation {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define categories with emojis and detailed descriptions
categories = {
    "Engineering": {
        "emoji": "🛠️",
        "description": "Engineering involves designing, building, and maintaining structures, machines, and systems. It emphasizes problem-solving, innovation, and technical skills.",
        "careers": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Aerospace Engineer"],
        "strengths": "Analytical thinking, creativity in design, hands-on work."
    },
    "Arts": {
        "emoji": "🎨",
        "description": "Arts focus on creative expression through visual, performing, or literary mediums. It values imagination, emotional depth, and aesthetic appreciation.",
        "careers": ["Graphic Designer", "Artist", "Musician", "Writer"],
        "strengths": "Creativity, emotional intelligence, self-expression."
    },
    "Management": {
        "emoji": "📊",
        "description": "Management involves leading teams, strategizing business operations, and making decisions to achieve goals. It requires organizational skills and leadership.",
        "careers": ["Project Manager", "Business Analyst", "CEO", "Consultant"],
        "strengths": "Leadership, strategic planning, communication."
    },
    "Science": {
        "emoji": "🔬",
        "description": "Science explores natural phenomena through research, experimentation, and analysis. It seeks to understand and explain the world.",
        "careers": ["Researcher", "Biologist", "Chemist", "Physicist"],
        "strengths": "Curiosity, analytical skills, attention to detail."
    },
    "IT": {
        "emoji": "💻",
        "description": "IT deals with technology, software, and data systems. It involves programming, cybersecurity, and digital solutions.",
        "careers": ["Software Developer", "Data Scientist", "Cybersecurity Expert", "Web Developer"],
        "strengths": "Logical thinking, problem-solving, adaptability to tech."
    }
}

# Define questions (same as before, with questions)
questions = [
    {
        "question": "What do you enjoy most in a project?",
        "options": [
            {"text": "Building or fixing things", "points": {"Engineering": 1}, "reasoning": "You chose this because you enjoy hands-on creation → indicating skills in problem-solving and mechanics → suggested careers: Mechanical Engineer, Civil Engineer."},
            {"text": "Expressing creativity through art", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy artistic expression → indicating skills in creativity and design → suggested careers: Graphic Designer, Artist."},
            {"text": "Organizing teams and resources", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy leadership → indicating skills in organization and strategy → suggested careers: Project Manager, Business Analyst."},
            {"text": "Experimenting with ideas", "points": {"Science": 1}, "reasoning": "You chose this because you enjoy discovery → indicating skills in research and analysis → suggested careers: Researcher, Biologist."}
        ]
    },
    {
        "question": "How do you prefer to spend your free time?",
        "options": [
            {"text": "Tinkering with gadgets", "points": {"Engineering": 1, "IT": 1}, "reasoning": "You chose this because you enjoy technical hobbies → indicating skills in innovation and technology → suggested careers: Robotics Engineer, Software Developer."},
            {"text": "Drawing or playing music", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy creative outlets → indicating skills in expression and aesthetics → suggested careers: Musician, Illustrator."},
            {"text": "Planning events or budgets", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy coordination → indicating skills in planning and finance → suggested careers: Event Planner, Financial Manager."},
            {"text": "Reading about science", "points": {"Science": 1}, "reasoning": "You chose this because you enjoy learning → indicating skills in curiosity and knowledge → suggested careers: Scientist, Educator."}
        ]
    },
    {
        "question": "What type of problem excites you?",
        "options": [
            {"text": "Structural or mechanical issues", "points": {"Engineering": 1}, "reasoning": "You chose this because you enjoy practical challenges → indicating skills in engineering and design → suggested careers: Aerospace Engineer, Architect."},
            {"text": "Emotional or aesthetic dilemmas", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy interpretive challenges → indicating skills in empathy and vision → suggested careers: Writer, Photographer."},
            {"text": "Business or logistical puzzles", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy strategic challenges → indicating skills in decision-making and efficiency → suggested careers: Operations Manager, Consultant."},
            {"text": "Scientific or analytical mysteries", "points": {"Science": 1, "IT": 1}, "reasoning": "You chose this because you enjoy intellectual challenges → indicating skills in logic and data → suggested careers: Data Scientist, Chemist."}
        ]
    },
    {
        "question": "Which subject did you excel in school?",
        "options": [
            {"text": "Math or Physics", "points": {"Engineering": 1, "Science": 1}, "reasoning": "You chose this because you enjoy quantitative subjects → indicating skills in calculation and theory → suggested careers: Physicist, Engineer."},
            {"text": "Art or Literature", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy expressive subjects → indicating skills in communication and imagination → suggested careers: Author, Artist."},
            {"text": "Business or Economics", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy practical subjects → indicating skills in economics and strategy → suggested careers: Economist, Entrepreneur."},
            {"text": "Computer Science", "points": {"IT": 1}, "reasoning": "You chose this because you enjoy technical subjects → indicating skills in programming and systems → suggested careers: Programmer, IT Specialist."}
        ]
    },
    {
        "question": "What motivates you at work?",
        "options": [
            {"text": "Creating tangible products", "points": {"Engineering": 1}, "reasoning": "You chose this because you enjoy tangible outcomes → indicating skills in craftsmanship and innovation → suggested careers: Product Designer, Inventor."},
            {"text": "Inspiring others through creativity", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy inspiration → indicating skills in motivation and artistry → suggested careers: Art Teacher, Performer."},
            {"text": "Achieving goals and leading teams", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy achievement → indicating skills in leadership and execution → suggested careers: CEO, Team Leader."},
            {"text": "Discovering new knowledge", "points": {"Science": 1}, "reasoning": "You chose this because you enjoy discovery → indicating skills in exploration and analysis → suggested careers: Researcher, Scientist."}
        ]
    },
    {
        "question": "How do you handle challenges?",
        "options": [
            {"text": "By designing solutions", "points": {"Engineering": 1, "IT": 1}, "reasoning": "You chose this because you enjoy problem-solving → indicating skills in design and technology → suggested careers: Systems Engineer, Developer."},
            {"text": "By expressing emotions", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy emotional processing → indicating skills in expression and therapy → suggested careers: Counselor, Artist."},
            {"text": "By strategizing and delegating", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy strategy → indicating skills in planning and management → suggested careers: Strategist, Manager."},
            {"text": "By researching and testing", "points": {"Science": 1}, "reasoning": "You chose this because you enjoy experimentation → indicating skills in research and testing → suggested careers: Lab Technician, Analyst."}
        ]
    },
    {
        "question": "What kind of environment do you thrive in?",
        "options": [
            {"text": "Workshop or lab", "points": {"Engineering": 1, "Science": 1}, "reasoning": "You chose this because you enjoy hands-on environments → indicating skills in experimentation and building → suggested careers: Engineer, Scientist."},
            {"text": "Studio or stage", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy creative spaces → indicating skills in performance and creation → suggested careers: Actor, Sculptor."},
            {"text": "Office or boardroom", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy professional settings → indicating skills in negotiation and administration → suggested careers: Administrator, Executive."},
            {"text": "Computer or data center", "points": {"IT": 1}, "reasoning": "You chose this because you enjoy digital environments → indicating skills in coding and networking → suggested careers: Cybersecurity Expert, Web Developer."}
        ]
    },
    {
        "question": "What do you value most in a career?",
        "options": [
            {"text": "Innovation and invention", "points": {"Engineering": 1}, "reasoning": "You chose this because you value creation → indicating skills in invention and technology → suggested careers: Innovator, Engineer."},
            {"text": "Self-expression and beauty", "points": {"Arts": 1}, "reasoning": "You chose this because you value expression → indicating skills in aesthetics and communication → suggested careers: Fashion Designer, Poet."},
            {"text": "Success and influence", "points": {"Management": 1}, "reasoning": "You chose this because you value achievement → indicating skills in leadership and influence → suggested careers: Influencer, Manager."},
            {"text": "Knowledge and truth", "points": {"Science": 1}, "reasoning": "You chose this because you value discovery → indicating skills in inquiry and accuracy → suggested careers: Philosopher, Scientist."}
        ]
    },
    {
        "question": "How do you approach learning?",
        "options": [
            {"text": "Through practical application", "points": {"Engineering": 1, "IT": 1}, "reasoning": "You chose this because you enjoy applied learning → indicating skills in implementation and coding → suggested careers: Engineer, Programmer."},
            {"text": "Through creative exploration", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy exploratory learning → indicating skills in creativity and experimentation → suggested careers: Explorer, Artist."},
            {"text": "Through structured courses", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy organized learning → indicating skills in discipline and strategy → suggested careers: Trainer, Manager."},
            {"text": "Through research and analysis", "points": {"Science": 1}, "reasoning": "You chose this because you enjoy analytical learning → indicating skills in research and logic → suggested careers: Analyst, Scientist."}
        ]
    },
    {
        "question": "What type of team role do you prefer?",
        "options": [
            {"text": "Builder or fixer", "points": {"Engineering": 1}, "reasoning": "You chose this because you enjoy constructive roles → indicating skills in construction and repair → suggested careers: Builder, Technician."},
            {"text": "Ideator or performer", "points": {"Arts": 1}, "reasoning": "You chose this because you enjoy expressive roles → indicating skills in ideation and performance → suggested careers: Performer, Creative Director."},
            {"text": "Leader or coordinator", "points": {"Management": 1}, "reasoning": "You chose this because you enjoy directive roles → indicating skills in leadership and coordination → suggested careers: Coordinator, Leader."},
            {"text": "Analyst or researcher", "points": {"Science": 1, "IT": 1}, "reasoning": "You chose this because you enjoy investigative roles → indicating skills in analysis and research → suggested careers: Researcher, Data Analyst."}
        ]
    },
    {
        "question": "What inspires you?",
        "options": [
            {"text": "Technological advancements", "points": {"Engineering": 1, "IT": 1}, "reasoning": "You chose this because you are inspired by tech → indicating skills in innovation and programming → suggested careers: Tech Innovator, Engineer."},
            {"text": "Artistic masterpieces", "points": {"Arts": 1}, "reasoning": "You chose this because you are inspired by art → indicating skills in appreciation and creation → suggested careers: Curator, Artist."},
            {"text": "Successful businesses", "points": {"Management": 1}, "reasoning": "You chose this because you are inspired by success → indicating skills in entrepreneurship and management → suggested careers: Entrepreneur, Manager."},
            {"text": "Scientific breakthroughs", "points": {"Science": 1}, "reasoning": "You chose this because you are inspired by discovery → indicating skills in science and exploration → suggested careers: Scientist, Inventor."}
        ]
    },
    {
        "question": "How do you make decisions?",
        "options": [
            {"text": "Based on logic and design", "points": {"Engineering": 1}, "reasoning": "You chose this because you rely on logic → indicating skills in rational thinking and design → suggested careers: Engineer, Architect."},
            {"text": "Based on intuition and emotion", "points": {"Arts": 1}, "reasoning": "You chose this because you rely on intuition → indicating skills in emotional intelligence and creativity → suggested careers: Therapist, Artist."},
            {"text": "Based on data and strategy", "points": {"Management": 1, "IT": 1}, "reasoning": "You chose this because you rely on data → indicating skills in analysis and strategy → suggested careers: Analyst, Strategist."},
            {"text": "Based on evidence and facts", "points": {"Science": 1}, "reasoning": "You chose this because you rely on evidence → indicating skills in objectivity and research → suggested careers: Scientist, Researcher."}
        ]
    },
    {
        "question": "What do you dream of achieving?",
        "options": [
            {"text": "Inventing something useful", "points": {"Engineering": 1}, "reasoning": "You chose this because you dream of invention → indicating skills in creativity and utility → suggested careers: Inventor, Engineer."},
            {"text": "Creating a masterpiece", "points": {"Arts": 1}, "reasoning": "You chose this because you dream of creation → indicating skills in artistry and expression → suggested careers: Artist, Composer."},
            {"text": "Building a successful company", "points": {"Management": 1}, "reasoning": "You chose this because you dream of success → indicating skills in business and leadership → suggested careers: CEO, Founder."},
            {"text": "Making a scientific discovery", "points": {"Science": 1}, "reasoning": "You chose this because you dream of discovery → indicating skills in exploration and science → suggested careers: Discoverer, Scientist."}
        ]
    },
    {
        "question": "What bores you?",
        "options": [
            {"text": "Repetitive tasks", "points": {"Engineering": 1, "IT": 1}, "reasoning": "You chose this because you dislike routine → indicating skills in innovation and dynamism → suggested careers: Innovator, Developer."},
            {"text": "Strict rules", "points": {"Arts": 1}, "reasoning": "You chose this because you dislike constraints → indicating skills in freedom and creativity → suggested careers: Free Spirit, Artist."},
            {"text": "Unclear goals", "points": {"Management": 1}, "reasoning": "You chose this because you dislike ambiguity → indicating skills in clarity and organization → suggested careers: Organizer, Manager."},
            {"text": "Superficial information", "points": {"Science": 1}, "reasoning": "You chose this because you dislike shallowness → indicating skills in depth and analysis → suggested careers: Deep Thinker, Scientist."}
        ]
    },
    {
        "question": "How do you communicate ideas?",
        "options": [
            {"text": "Through diagrams and models", "points": {"Engineering": 1}, "reasoning": "You chose this because you use visuals → indicating skills in visualization and design → suggested careers: Designer, Engineer."},
            {"text": "Through stories and art", "points": {"Arts": 1}, "reasoning": "You chose this because you use narratives → indicating skills in storytelling and expression → suggested careers: Storyteller, Artist."},
            {"text": "Through presentations and plans", "
