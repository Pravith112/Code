# Import necessary libraries
import streamlit as st  # Streamlit for building the web app interface
import pandas as pd  # Pandas for data manipulation, though not heavily used here
import matplotlib.pyplot as plt  # Matplotlib for creating charts in results
import numpy as np  # NumPy for numerical operations, if needed for calculations

# Set page configuration for the Streamlit app
# This defines the title, icon, and layout of the web page
st.set_page_config(
    page_title="Career Interest Quiz",  # Title shown in the browser tab
    page_icon="🚀",  # Icon for the tab
    layout="wide"  # Wide layout for better use of screen space
)

# Custom CSS for styling the app
# This CSS provides a modern, gradient background and styles for cards, buttons, etc.
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  /* Gradient background from blue to purple */
        color: white;  /* Default text color */
    }
    .card {
        background: rgba(255, 255, 255, 0.1);  /* Semi-transparent white background for cards */
        border-radius: 10px;  /* Rounded corners */
        padding: 20px;  /* Padding inside the card */
        margin: 10px 0;  /* Margin around the card */
        backdrop-filter: blur(10px);  /* Blur effect for modern look */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* Shadow for depth */
    }
    .result-card {
        background: rgba(255, 255, 255, 0.2);  /* Slightly more opaque for result cards */
        border-radius: 15px;  /* More rounded for emphasis */
        padding: 25px;  /* More padding for results */
        margin: 15px 0;  /* Larger margin */
        text-align: center;  /* Center-align text in results */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);  /* Deeper shadow */
    }
    .emoji {
        font-size: 2em;  /* Larger emoji size */
    }
    .question {
        font-weight: bold;  /* Bold for questions */
        color: #f0f0f0;  /* Light gray color */
    }
    .option {
        color: #e0e0e0;  /* Slightly darker for options */
    }
    .submit-btn {
        background: #ff6b6b;  /* Red background for submit button */
        color: white;  /* White text */
        border: none;  /* No border */
        padding: 10px 20px;  /* Padding */
        border-radius: 5px;  /* Rounded corners */
        cursor: pointer;  /* Pointer cursor on hover */
        font-size: 1.2em;  /* Larger font */
    }
    .explanation {
        background: rgba(255, 255, 255, 0.05);  /* Very light background for explanations */
        border-radius: 8px;  /* Rounded */
        padding: 15px;  /* Padding */
        margin: 10px 0;  /* Margin */
        color: #e0e0e0;  /* Light color */
    }
    </style>
    """,
    unsafe_allow_html=True  # Allow HTML in markdown for custom styles
)

# Define categories with detailed information
# Each category has an emoji, description, list of careers, and strengths
# This makes the results more informative
categories = {
    "Engineering": {
        "emoji": "🛠️",
        "description": "Engineering involves designing, building, and maintaining structures, machines, and systems. It emphasizes problem-solving, innovation, and technical skills. Engineers work on real-world applications, from bridges to software systems, requiring a blend of creativity and precision.",
        "careers": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Aerospace Engineer", "Biomedical Engineer", "Chemical Engineer"],
        "strengths": "Analytical thinking, creativity in design, hands-on work, attention to detail, problem-solving under pressure."
    },
    "Arts": {
        "emoji": "🎨",
        "description": "Arts focus on creative expression through visual, performing, or literary mediums. It values imagination, emotional depth, and aesthetic appreciation. Artists often explore human emotions and culture, creating works that inspire and provoke thought.",
        "careers": ["Graphic Designer", "Artist", "Musician", "Writer", "Photographer", "Film Director", "Sculptor"],
        "strengths": "Creativity, emotional intelligence, self-expression, originality, ability to evoke emotions."
    },
    "Management": {
        "emoji": "📊",
        "description": "Management involves leading teams, strategizing business operations, and making decisions to achieve goals. It requires organizational skills, leadership, and the ability to motivate others. Managers often handle resources, budgets, and long-term planning.",
        "careers": ["Project Manager", "Business Analyst", "CEO", "Consultant", "Operations Manager", "Entrepreneur", "HR Manager"],
        "strengths": "Leadership, strategic planning, communication, decision-making, adaptability to change."
    },
    "Science": {
        "emoji": "🔬",
        "description": "Science explores natural phenomena through research, experimentation, and analysis. It seeks to understand and explain the world, from microscopic cells to cosmic events. Scientists contribute to advancements in medicine, technology, and environmental protection.",
        "careers": ["Researcher", "Biologist", "Chemist", "Physicist", "Environmental Scientist", "Geologist", "Pharmacist"],
        "strengths": "Curiosity, analytical skills, attention to detail, objectivity, perseverance in research."
    },
    "IT": {
        "emoji": "💻",
        "description": "IT deals with technology, software, and data systems. It involves programming, cybersecurity, and digital solutions. IT professionals build and maintain the digital infrastructure that powers modern life, from apps to networks.",
        "careers": ["Software Developer", "Data Scientist", "Cybersecurity Expert", "Web Developer", "Network Administrator", "AI Engineer", "Database Administrator"],
        "strengths": "Logical thinking, problem-solving, adaptability to tech, coding skills, innovation in digital tools."
    }
}

# Define the list of questions
# Each question has a text, options with points and reasoning
# Points are assigned to categories, reasoning explains the choice
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
