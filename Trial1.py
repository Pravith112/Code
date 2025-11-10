import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="I Love You ❤️", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>I Love You</title>
<style>
  html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: black;
    height: 100%;
    width: 100%;
  }
  canvas {
    display: block;
  }
  #text {
    position: absolute;
    top: 65%;
    width: 100%;
    text-align: center;
    font-family: 'Brush Script MT', cursive;
    font-size: 70px;
    color: #ff4081;
    text-shadow: 0 0 25px #ff66b2, 0 0 50px #ff66b2;
    animation: glow 2s ease-in-out infinite alternate;
  }
  @keyframes glow {
    from { text-shadow: 0 0 15px ##FFFFFF, 0 0 30px ##FFFFFF; }
    to { text-shadow: 0 0 35px ###FFFFFF, 0 0 70px ##FFFFFF; }
  }
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<div id="text">I LOVE YOU!!!</div>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let hearts = [];
let time = 0;

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

function drawHeart(x, y, size, color, alpha=1) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(size, size);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.bezierCurveTo(0, -3, -5, -15, -15, -15);
  ctx.bezierCurveTo(-35, -15, -35, 10, -35, 10);
  ctx.bezierCurveTo(-35, 25, -15, 45, 0, 60);
  ctx.bezierCurveTo(15, 45, 35, 25, 35, 10);
  ctx.bezierCurveTo(35, 10, 35, -15, 15, -15);
  ctx.bezierCurveTo(5, -15, 0, -3, 0, 0);
  ctx.closePath();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = color;
  ctx.shadowBlur = 25;
  ctx.shadowColor = color;
  ctx.fill();
  ctx.restore();
}

class SmallHeart {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = Math.random() * 0.25 + 0.05;
    this.vy = Math.random() * 2 + 1;
    this.vx = (Math.random() - 0.5) * 1;
    this.alpha = 1;
  }
  update() {
    this.y += this.vy;
    this.x += this.vx;
    this.alpha -= 0.003;
  }
  draw() {
    drawHeart(this.x, this.y, this.size, "rgba(255,80,150,1)", this.alpha);
  }
}

function animate() {
  time += 0.03;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Big bouncing heart
  let bounceY = Math.sin(time) * 20;
  drawHeart(canvas.width/2, canvas.height/2 + bounceY, 5, "rgb(255,50,130)");

  // Create small hearts
  if (Math.random() < 0.3) {
    hearts.push(new SmallHeart(Math.random() * canvas.width, -20));
  }

  // Update and draw small hearts
  for (let i = hearts.length - 1; i >= 0; i--) {
    let h = hearts[i];
    h.update();
    h.draw();
    if (h.alpha <= 0 || h.y > canvas.height + 50) {
      hearts.splice(i, 1);
    }
  }

  requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
"""

# Fullscreen in Streamlit
components.html(html_code, height=800, scrolling=False)

