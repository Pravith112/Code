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

# Combined HTML + CSS animation
st.markdown("""
    <style>
    /* --- Matrix Rain Background --- */
    body, html {
        height: 100%;
        background: black;
        overflow: hidden;
        margin: 0;
    }

    canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background: black;
    }

    /* --- Falling Hearts --- */
    @keyframes fallHearts {
      0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
      100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }

    .heart {
      position: fixed;
      top: 0;
      width: 15px;
      height: 15px;
      background: #ff4d6d;
      transform: rotate(-45deg);
      animation: fallHearts linear infinite;
      border-radius: 50% 50% 0 0;
      z-index: 2;
    }

    .heart::before, .heart::after {
      content: "";
      position: absolute;
      width: 15px;
      height: 15px;
      background: #ff4d6d;
      border-radius: 50%;
    }

    .heart::before {
      top: 0;
      left: 7.5px;
    }

    .heart::after {
      top: -7.5px;
      left: 0;
    }

    /* --- Big Center Heart --- */
    @keyframes pulse {
      0% { transform: translate(-50%, -50%) rotate(-45deg) scale(1); }
      50% { transform: translate(-50%, -50%) rotate(-45deg) scale(1.1); }
      100% { transform: translate(-50%, -50%) rotate(-45deg) scale(1); }
    }

    .big-heart {
      position: fixed;
      top: 50%;
      left: 50%;
      width: 160px;
      height: 160px;
      background: #ff1a4d;
      transform: translate(-50%, -50%) rotate(-45deg);
      border-radius: 50% 50% 0 0;
      animation: pulse 2s infinite ease-in-out;
      z-index: 3;
    }

    .big-heart::before, .big-heart::after {
      content: "";
      position: absolute;
      width: 160px;
      height: 160px;
      background: #ff1a4d;
      border-radius: 50%;
    }

    .big-heart::before {
      top: 0;
      left: 80px;
    }

    .big-heart::after {
      top: -80px;
      left: 0;
    }
    </style>

    <!-- Matrix Canvas -->
    <canvas id="matrix"></canvas>

    <!-- Big Heart -->
    <div class="big-heart"></div>

    <!-- Falling Hearts -->
    <script>
    const numHearts = 25;
    for (let i = 0; i < numHearts; i++) {{
        const heart = document.createElement('div');
        heart.classList.add('heart');
        heart.style.left = Math.random() * 100 + '%';
        heart.style.animationDuration = (3 + Math.random() * 5) + 's';
        heart.style.animationDelay = (Math.random() * 3) + 's';
        heart.style.background = ['#ff4d6d', '#ff758f', '#ff92a5'][Math.floor(Math.random()*3)];
        document.body.appendChild(heart);
    }}

    /* --- Matrix Effect --- */
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');

    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    const letters = '01💖';
    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const drops = [];
    for (let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {{
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff00';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {{
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }}
    }}

    setInterval(draw, 35);
    </script>
""", unsafe_allow_html=True)
