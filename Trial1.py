import streamlit as st
import random

st.set_page_config(page_title="I Love You ❤️", page_icon="❤️", layout="centered")

# Clean UI (no Streamlit chrome)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    body {
        background-color: black;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Generate small hearts HTML separately (so Streamlit doesn't render it as text)
small_hearts_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(3, 7)
    delay = random.uniform(0, 3)
    size = random.randint(8, 16)
    color = random.choice(["#ff4d6d", "#ff758f", "#ff92a5", "#ffb3c1"])
    small_hearts_html += f'''
      <div class="small-heart" style="
        left:{left}%;
        width:{size}px;
        height:{size}px;
        background-color:{color};
        animation-duration:{duration}s;
        animation-delay:{delay}s;
      "></div>
    '''

# Combine everything into one HTML block
html_code = f"""
<style>
/* --- ANIMATIONS --- */

@keyframes softPulse {{
  0%   {{ transform: scale(1); }}
  25%  {{ transform: scale(1.05); }}
  50%  {{ transform: scale(1.12); }}
  75%  {{ transform: scale(1.05); }}
  100% {{ transform: scale(1); }}
}}

@keyframes heartGlow {{
  0%,100% {{ filter: drop-shadow(0 0 25px rgba(255, 0, 100, 0.8)); }}
  50%     {{ filter: drop-shadow(0 0 60px rgba(255, 100, 180, 1)); }}
}}

@keyframes fall {{
  0% {{
    transform: translateY(-10vh) translateX(0);
    opacity: 1;
  }}
  100% {{
    transform: translateY(110vh) translateX(10px);
    opacity: 0;
  }}
}}

/* --- ELEMENTS --- */

.container {{
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}}

.main-heart {{
  position: absolute;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-45deg);
  width: 150px;
  height: 150px;
  background-color: #ff2b5e;
  border-radius: 50% 50% 0 0;
  animation: softPulse 2s infinite ease-in-out, heartGlow 3s infinite ease-in-out;
}}

.main-heart::before,
.main-heart::after {{
  content: "";
  position: absolute;
  width: 150px;
  height: 150px;
  background-color: #ff2b5e;
  border-radius: 50%;
}}

.main-heart::before {{
  top: 0;
  left: 75px;
}}

.main-heart::after {{
  top: -75px;
  left: 0;
}}

h1 {{
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
}}

@keyframes glowText {{
  from {{ text-shadow: 0 0 10px #ff3366, 0 0 20px #ff6699; }}
  to   {{ text-shadow: 0 0 20px #ff99cc, 0 0 40px #ff3366; }}
}}

.small-heart {{
  position: absolute;
  transform: rotate(-45deg);
  border-radius: 50% 50% 0 0;
  animation: fall linear infinite;
}}

.small-heart::before,
.small-heart::after {{
  content: "";
  position: absolute;
  border-radius: 50%;
}}

.small-heart::before {{
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 100%;
  background-color: inherit;
}}

.small-heart::after {{
  top: -50%;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: inherit;
}}
</style>

<div class="container">
  {small_hearts_html}
  <div class="main-heart"></div>
  <h1>I Love You!! 💖</h1>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
