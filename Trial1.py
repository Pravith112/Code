import streamlit as st

st.set_page_config(page_title="Matrix Love 💚❤️", page_icon="💚", layout="wide")

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
body {
  margin: 0;
  overflow: hidden;
  background: black;
}
</style>
""", unsafe_allow_html=True)

# Actual animation content
st.markdown("""
<div id="container"></div>

<style>
/* --- Base page setup --- */
body, html {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background: black;
  height: 100%;
  width: 100%;
}

/* --- Matrix Canvas --- */
#matrixCanvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: black;
  z-index: 0;
}

/* --- Big Heart --- */
.big-heart {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 150px;
  height: 150px;
  background: #ff1a4d;
  transform: translate(-50%, -50%) rotate(-45deg);
  animation: pulse 2s ease-in-out infinite;
  z-index: 3;
}

.big-heart::before,
.big-heart::after {
  content: '';
  position: absolute;
  width: 150px;
  height: 150px;
  background: #ff1a4d;
  border-radius: 50%;
}

.big-heart::before {
  top: 0;
  left: 75px;
}

.big-heart::after {
  top: -75px;
  left: 0;
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) rotate(-45deg) scale(1); }
  50% { transform: translate(-50%, -50%) rotate(-45deg) scale(1.15); }
}

/* --- Falling Hearts --- */
@keyframes fall {
  0% {
    transform: translateY(-10vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(110vh) rotate(360deg);
    opacity: 0;
  }
}

.falling-heart {
  position: fixed;
  top: -20px;
  width: 15px;
  height: 15px;
  background-color: #ff4d6d;
  transform: rotate(-45deg);
  border-radius: 50% 50% 0 0;
  z-index: 2;
  animation: fall linear infinite;
}

.falling-heart::before,
.falling-heart::after {
  content: "";
  position: absolute;
  width: 15px;
  height: 15px;
  background-color: inherit;
  border-radius: 50%;
}

.falling-heart::before {
  top: 0;
  left: 7.5px;
}

.falling-heart::after {
  top: -7.5px;
  left: 0;
}
</style>

<script>
const container = document.getElementById("container");

// --- Create matrix canvas ---
const canvas = document.createElement("canvas");
canvas.id = "matrixCanvas";
container.appendChild(canvas);
const ctx = canvas.getContext("2d");

// --- Create big heart ---
const bigHeart = document.createElement("div");
bigHeart.classList.add("big-heart");
container.appendChild(bigHeart);

// --- Create falling hearts ---
for (let i = 0; i < 25; i++) {
  const h = document.createElement("div");
  h.classList.add("falling-heart");
  h.style.left = Math.random() * 100 + "%";
  h.style.animationDuration = (4 + Math.random() * 5) + "s";
  h.style.animationDelay = Math.random() * 3 + "s";
  const colors = ["#ff4d6d", "#ff758f", "#ff92a5"];
  h.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  container.appendChild(h);
}

// --- Matrix effect ---
canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters = "01💖";
const fontSize = 16;
const columns = canvas.width / fontSize;
const drops = [];
for (let x = 0; x < columns; x++) drops[x] = 1;

function draw() {
  ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#00ff00";
  ctx.font = fontSize + "px monospace";

  for (let i = 0; i < drops.length; i++) {
    const text = letters.charAt(Math.floor(Math.random() * letters.length));
    ctx.fillText(text, i * fontSize, drops[i] * fontSize);

    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
      drops[i] = 0;
    drops[i]++;
  }
}
setInterval(draw, 35);
</script>
""", unsafe_allow_html=True)
