import streamlit as st

st.set_page_config(page_title="I Love You ❤️", page_icon="❤️", layout="centered")

# Hide Streamlit’s default UI for clean look
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    body {
        background-color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Heart + glowing animation in HTML + CSS
st.markdown("""
    <style>
    @keyframes heartbeat {
      0% {transform: scale(1);}
      14% {transform: scale(1.3);}
      28% {transform: scale(1);}
      42% {transform: scale(1.3);}
      70% {transform: scale(1);}
    }

    @keyframes glow {
      0%, 100% { box-shadow: 0 0 40px 20px rgba(255, 0, 0, 0.3); }
      50% { box-shadow: 0 0 70px 35px rgba(255, 80, 150, 0.6); }
    }

    .heart {
      position: relative;
      width: 150px;
      height: 135px;
      margin: 100px auto;
      background-color: red;
      transform: rotate(-45deg);
      animation: heartbeat 1.5s infinite ease-in-out, glow 2s infinite ease-in-out;
    }

    .heart::before, .heart::after {
      content: "";
      position: absolute;
      width: 150px;
      height: 135px;
      background-color: red;
      border-radius: 50%;
    }

    .heart::before {
      top: -75px;
      left: 0;
    }

    .heart::after {
      left: 75px;
      top: 0;
    }

    h1 {
      color: white;
      text-align: center;
      font-family: "Comic Sans MS", cursive, sans-serif;
      font-size: 3em;
      text-shadow: 0 0 20px #ff99cc, 0 0 40px #ff3366;
      animation: glowText 2s ease-in-out infinite alternate;
    }

    @keyframes glowText {
      from { text-shadow: 0 0 10px #ff3366, 0 0 20px #ff6699; }
      to { text-shadow: 0 0 20px #ff99cc, 0 0 40px #ff3366; }
    }
    </style>

    <div class="heart"></div>
    <h1>I Love You!! 💖</h1>
""", unsafe_allow_html=True)
