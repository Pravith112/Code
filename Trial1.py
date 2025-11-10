# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Legendary Hearts + Matrix", layout="wide", initial_sidebar_state="collapsed")

html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Legendary Hearts + Matrix</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    html, body, #canvasWrap { height: 100%; margin: 0; background: black; overflow: hidden; }
    #canvasWrap { position: fixed; inset: 0; }
    canvas { display: block; }
    /* optional small credit text */
    #credit {
      position: fixed;
      right: 12px;
      bottom: 8px;
      color: rgba(255,255,255,0.6);
      font-family: Inter, system-ui, Arial;
      font-size: 12px;
      user-select: none;
      z-index: 10;
      pointer-events: none;
      text-shadow: 0 1px 3px rgba(0,0,0,0.6);
    }
  </style>
</head>
<body>
  <div id="canvasWrap"></div>
  <div id="credit">Legendary hearts + matrix</div>

  <script>
  (function () {
    // Canvas setup
    const wrap = document.getElementById('canvasWrap');
    const canvas = document.createElement('canvas');
    wrap.appendChild(canvas);
    const ctx = canvas.getContext('2d', { alpha: true });

    // DPI / retina handling
    let DPR = Math.max(1, window.devicePixelRatio || 1);

    function resize() {
      DPR = Math.max(1, window.devicePixelRatio || 1);
      canvas.width = Math.floor(window.innerWidth * DPR);
      canvas.height = Math.floor(window.innerHeight * DPR);
      canvas.style.width = window.innerWidth + 'px';
      canvas.style.height = window.innerHeight + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      // recompute dependent params
      columns = Math.floor(window.innerWidth / columnSize);
      initMatrixDrops();
    }
    window.addEventListener('resize', resize, { passive: true });

    // ---- Matrix background ----
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリギジヂビピウゥクスツヌフムユュルグズヅブプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポ0123456789ABCDEFGHIJKLMNOPQRSTUVWXZY';
    const columnSize = 18; // px per column
    let columns = Math.floor(window.innerWidth / columnSize);
    let drops = []; // y position for each column
    let fontSize = 14;
    const trailAlpha = 0.075; // how strong the fade trail is

    function initMatrixDrops() {
      columns = Math.max(3, Math.floor(window.innerWidth / columnSize));
      drops = new Array(columns).fill(0).map(() => Math.random() * -50);
    }

    // ---- Hearts ----
    // Heart utility: draw a heart path centered at (x,y) with given size
    function drawHeartPath(ctx, x, y, size) {
      // parametric heart scaled
      const s = size / 20;
      ctx.beginPath();
      ctx.moveTo(x, y - 4 * s);
      ctx.bezierCurveTo(x + 12 * s, y - 28 * s, x + 44 * s, y - 8 * s, x, y + 28 * s);
      ctx.bezierCurveTo(x - 44 * s, y - 8 * s, x - 12 * s, y - 28 * s, x, y - 4 * s);
      ctx.closePath();
    }

    // Big soft bouncing heart
    const bigHeart = {
      x: () => window.innerWidth * 0.5,
      baseY: () => window.innerHeight * 0.36,
      size: () => Math.min(window.innerWidth, window.innerHeight) * 0.22, // responsive
      t: 0
    };

    // Small falling hearts (particles)
    class SmallHeart {
      constructor(x, y, size, vx, vy, rotation, spin, life, hue) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.vx = vx;
        this.vy = vy;
        this.rotation = rotation;
        this.spin = spin;
        this.life = life; // total lifetime in frames
        this.age = 0;
        this.hue = hue || 340; // pinkish default
        this.alpha = 1;
      }
      update() {
        this.vy += 0.06; // gravity
        this.x += this.vx;
        this.y += this.vy;
        this.rotation += this.spin;
        this.age++;
        this.alpha = Math.max(0, 1 - this.age / this.life);
      }
      draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.alpha;
        const s = this.size;
        ctx.beginPath();
        // simple heart via two arcs + triangle
        ctx.moveTo(0, -s/2);
        ctx.bezierCurveTo(s/2, -s*0.9, s*1.1, -s*0.05, 0, s);
        ctx.bezierCurveTo(-s*1.1, -s*0.05, -s/2, -s*0.9, 0, -s/2);
        ctx.closePath();
        // fill with gradient for depth
        const g = ctx.createLinearGradient(-s, -s, s, s);
        g.addColorStop(0, `hsla(${this.hue},95%,60%,1)`);
        g.addColorStop(1, `hsla(${this.hue-20},95%,45%,1)`);
        ctx.fillStyle = g;
        ctx.shadowColor = `rgba(255,${this.hue > 60 ? 160 : 50},${this.hue > 60 ? 160 : 50},0.8)`;
        ctx.shadowBlur = Math.min(20, s * 0.8);
        ctx.fill();
        ctx.restore();
      }
    }

    // store small hearts
    let hearts = [];
    let spawnAccumulator = 0;

    function spawnSmallHeart(x, startY) {
      const size = 8 + Math.random() * 18;
      const vx = (Math.random() - 0.5) * 1.2;
      const vy = -1 - Math.random() * 0.5; // initial upward flicker
      const rotation = Math.random() * Math.PI * 2;
      const spin = (Math.random() - 0.5) * 0.06;
      const life = 120 + Math.random() * 180;
      const hue = 320 + Math.random() * 40; // pink/purple range
      hearts.push(new SmallHeart(x, startY, size, vx, vy, rotation, spin, life, hue));
    }

    // create a shower of hearts across width
    function spawnHeartsBatch(count) {
      for (let i = 0; i < count; i++) {
        const x = Math.random() * window.innerWidth;
        const startY = -20 - Math.random() * 120;
        spawnSmallHeart(x, startY);
      }
    }

    // click to burst hearts
    window.addEventListener('pointerdown', (e) => {
      for (let i = 0; i < 30; i++) {
        const x = e.clientX + (Math.random() - 0.5) * 120;
        const y = e.clientY + (Math.random() - 0.5) * 40;
        spawnSmallHeart(x, y);
      }
    }, { passive: true });

    // ---- animation loop ----
    let last = performance.now();

    // Matrix variables for rendering characters
    function randomChar() {
      return chars.charAt(Math.floor(Math.random() * chars.length));
    }

    // per-column drop speeds
    let dropSpeeds = [];
    function initDropSpeeds() {
      dropSpeeds = new Array(columns).fill(0).map(() => (1 + Math.random() * 2.4));
    }

    // initialize
    resize();
    initMatrixDrops();
    initDropSpeeds();
    spawnHeartsBatch(120); // initial hearts shower

    // draw one frame of matrix (semi-transparent overlay to create trailing)
    function drawMatrix(ctx) {
      // fade using translucent black rectangle for trailing effect
      ctx.fillStyle = `rgba(0, 0, 0, ${trailAlpha})`;
      ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);

      ctx.font = `${fontSize}px monospace`;
      for (let i = 0; i < columns; i++) {
        const x = i * columnSize + (columnSize * 0.15);
        const y = drops[i] * fontSize;
        // bright lead
        ctx.fillStyle = 'rgba(180,255,175,0.95)';
        ctx.fillText(randomChar(), x, y);
        // some slightly behind characters
        if (y - fontSize * 2 > 0) {
          ctx.fillStyle = 'rgba(80,220,100,0.35)';
          ctx.fillText(randomChar(), x, y - fontSize * 2);
        }
        drops[i] += dropSpeeds[i] * 0.6 + Math.random() * 0.8;
        if (drops[i] * fontSize > window.innerHeight + 50) {
          drops[i] = Math.random() * -50;
        }
      }
    }

    // heart spawn logic: seeds near top occasionally, and near big heart sometimes
    let heartSpawnTimer = 0;

    function update(dt) {
      // update big heart parameter time
      bigHeart.t += dt * 0.0012;

      // spawn small hearts constantly but controlled
      spawnAccumulator += dt * 0.02;
      if (spawnAccumulator > 1) {
        const toSpawn = Math.floor(spawnAccumulator);
        spawnAccumulator -= toSpawn;
        for (let i = 0; i < toSpawn; i++) {
          // bias spawn to upper half for falling effect
          const x = Math.random() * window.innerWidth;
          const startY = -10 - Math.random() * window.innerHeight * 0.2;
          if (Math.random() < 0.18) {
            // sometimes spawn from big heart horizontally
            const hx = bigHeart.x() + (Math.random() - 0.5) * bigHeart.size() * 0.6;
            spawnSmallHeart(hx, bigHeart.baseY() - bigHeart.size() * 0.2 + Math.random() * 30);
          } else {
            spawnSmallHeart(x, startY);
          }
        }
      }

      // occasional burst
      heartSpawnTimer += dt;
      if (heartSpawnTimer > 3500 + Math.random() * 2200) {
        heartSpawnTimer = 0;
        spawnHeartsBatch(26 + Math.floor(Math.random() * 30));
      }

      // update hearts array and purge dead hearts
      for (let i = hearts.length - 1; i >= 0; i--) {
        hearts[i].update();
        if (hearts[i].y > window.innerHeight + 60 || hearts[i].alpha <= 0) {
          hearts.splice(i, 1);
        }
      }
    }

    function draw() {
      // clear to transparent so matrix fade works with drawn shapes on top
      // We'll draw matrix first as background, then hearts, then big heart with glow overlay
      // draw matrix background (but don't fully clear the canvas to keep trailing)
      drawMatrix(ctx);

      // Draw small hearts
      for (let h of hearts) {
        h.draw(ctx);
      }

      // Draw big soft bouncing heart with glow
      const hx = bigHeart.x();
      const baseY = bigHeart.baseY();
      const size = Math.max(30, bigHeart.size());
      // gentle bounce: sine + eased magnitude
      const bounce = Math.sin(bigHeart.t * 1.1) * 14 + Math.sin(bigHeart.t * 0.28) * 6;
      const by = baseY + bounce;

      // shadow/glow
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      const glowRad = size * 0.9;
      const gradient = ctx.createRadialGradient(hx, by, 2, hx, by, glowRad);
      gradient.addColorStop(0, 'rgba(255,120,180,0.22)');
      gradient.addColorStop(0.4, 'rgba(255,60,140,0.12)');
      gradient.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(hx, by, glowRad, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // draw heart path filled with gradient
      ctx.save();
      drawHeartPath(ctx, hx, by, size * 1.02);
      const g = ctx.createLinearGradient(hx - size, by - size, hx + size, by + size);
      g.addColorStop(0, 'rgba(255,160,200,0.96)');
      g.addColorStop(0.5, 'rgba(255,40,120,0.98)');
      g.addColorStop(1, 'rgba(200,18,80,0.95)');
      ctx.fillStyle = g;
      ctx.shadowColor = 'rgba(255,80,150,0.9)';
      ctx.shadowBlur = Math.min(80, size * 0.55);
      ctx.fill();
      ctx.restore();

      // outline subtle
      ctx.save();
      ctx.lineWidth = Math.max(2, size * 0.02);
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      drawHeartPath(ctx, hx, by, size * 1.02);
      ctx.stroke();
      ctx.restore();

      // small shimmer near heart top
      ctx.save();
      ctx.globalAlpha = 0.16;
      ctx.fillStyle = 'white';
      ctx.beginPath();
      ctx.ellipse(hx - size * 0.22, by - size * 0.28, Math.max(6, size * 0.08), Math.max(6, size * 0.12), Math.PI / 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    function frame(now) {
      const dt = Math.min(60, now - last); // ms, clamp to avoid big jumps
      last = now;

      update(dt);
      draw();

      requestAnimationFrame(frame);
    }

    // initial clear to set black background (matrix will draw trails)
    ctx.fillStyle = 'rgba(0,0,0,1)';
    ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);

    // start loop
    requestAnimationFrame((t) => {
      last = t;
      frame(t);
    });

    // start periodic matrix speed shuffle to make it lively
    setInterval(() => {
      initDropSpeeds();
    }, 3800);

    // accessibility: pause animation if tab is hidden to save CPU
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // do nothing — requestAnimationFrame will throttle, but we can also reduce spawn frequency
      }
    });

    // ensure initial sizing
    resize();
  })();
  </script>
</body>
</html>
"""

components.html(html, height=900, scrolling=False,  allow_scripts=True)
