import streamlit as st

st.set_page_config(page_title="I Love You ❤️", page_icon="❤️", layout="centered")

# Clean UI
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    body {
        background-color: black;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Full HTML + CSS magic
st.markdown("""
    <style>
    /* --- KEYFRAMES --- */

    /* Smooth heartbeat pulse */
    @keyframes softPulse {
      0%   { transform: scale(1); }
      25%  { transform: scale(1.05); }
      50%  { transform: scale(1.12); }
      75%  { transform: scale(1.05); }
      100% { transform: scale(1); }
    }

    /* Glow animation for main heart */
    @keyframes heartGlow {
      0%,100% { filter: drop-shadow(0 0 25px rgba(255, 0, 100, 0.8)); }
      50%     { filter: drop-shadow(0 0 60px rgba(255, 100, 180, 1)); }
    }

    /* Falling hearts */
    @keyframes fall {
      0% {
        transform: translateY(-10vh) translateX(0);
        opacity: 1;
      }
      100% {
        transform: translateY(110vh) translateX(10px);
        opacity: 0;
      }
    }

    /* --- ELEMENT STYLES --- */

    .container {
      position: relative;
      height: 100vh;
      width: 100%;
      overflow: hidden;
    }

    /* Big heart */
    .main-heart {
      position: absolute;
      top: 45%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-45deg);
      width: 150px;
      height: 150px;
      background-color: #ff2b5e;
      border-radius: 50% 50% 0 0;
      animation: softPulse 2s infinite ease-in-out, heartGlow 3s infinite ease-in-out;
    }

    .main-heart::before,
    .main-heart::after {
      content: "";
      position: absolute;
      width: 150px;
      height: 150px;
      background-color: #ff2b5e;
      border-radius: 50%;
    }

    .main-heart::before {
      top: 0;
      left: 75px;
    }

    .main-heart::after {
      top: -75px;
      left: 0;
    }

    /* I Love You text */
    h1 {
      position: absolute;
      top: 75%;
      left: 50%;
      transform: translateX(-50%);
      color: white;
      text-align: center;
      font-family: "Comic Sans MS", cursive, sans-serif;
      font-size: 3em;
      text-shadow: 0 0 20px #ff99cc, 0 0 40px #ff3366;
      animation: glowText 2s ease-in-out infinite alternate;
    }

    @keyframes glowText {
      from { text-shadow: 0 0 10px #ff3366, 0 0 20px #ff6699; }
      to   { text-shadow: 0 0 20px #ff99cc, 0 0 40px #ff3366; }
    }

    /* Small falling hearts */
    .small-heart {
      position: absolute;
      width: 15px;
      height: 15px;
      background-color: #ff4d6d;
      transform: rotate(-45deg);
      animation: fall linear infinite;
      border-radius: 50% 50% 0 0;
    }

    .small-heart::before,
    .small-heart::after {
      content: "";
      position: absolute;
      width: 15px;
      height: 15px;
      background-color: #ff4d6d;
      border-radius: 50%;
    }

    .small-heart::before {
      top: 0;
      left: 7.5px;
    }

    .small-heart::after {
      top: -7.5px;
      left: 0;
    }
    </style>

    

