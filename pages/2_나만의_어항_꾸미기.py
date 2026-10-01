import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="투명 유리 어항 시뮬레이터", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>투명 유리 어항 시뮬레이터</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #0f172a;
      color: #f8fafc;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* Side Control Panel */
    .sidebar {
      width: 300px;
      background-color: #1e293b;
      border-right: 1px solid #334155;
      display: flex;
      flex-direction: column;
      z-index: 10;
      box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
    }

    .sidebar-header {
      padding: 16px;
      background-color: #0f172a;
      border-bottom: 1px solid #334155;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sidebar-header i {
      font-size: 22px;
      color: #38bdf8;
    }

    .sidebar-header h1 {
      font-size: 16px;
      font-weight: 700;
      color: #f1f5f9;
    }

    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .section-title {
      font-size: 12px;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }

    .tool-btn {
      background-color: #334155;
      color: #e2e8f0;
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      text-align: left;
    }

    .tool-btn:hover {
      background-color: #475569;
      color: #ffffff;
      border-color: #38bdf8;
    }

    .tool-btn.active {
      background-color: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    .tool-btn i {
      font-size: 13px;
      color: #38bdf8;
      width: 16px;
      text-align: center;
    }

    .tool-btn.active i {
      color: #ffffff;
    }

    /* Main Aquarium Container */
    .aquarium-container {
      flex: 1;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      background: radial-gradient(circle at center, #1e293b 0%, #090d16 100%);
    }

    /* Crystal Clear Glass Tank Design */
    .glass-tank-frame {
      position: relative;
      width: 100%;
      height: 88vh;
      border-radius: 16px;
      box-shadow: 
        0 20px 50px rgba(0, 0, 0, 0.6),
        inset 0 0 20px rgba(255, 255, 255, 0.4),
        inset 0 0 60px rgba(56, 189, 248, 0.2);
      border: 4px solid rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(2px);
      overflow: hidden;
      background: linear-gradient(180deg, 
        rgba(224, 242, 254, 0.85) 0%, 
        rgba(186, 230, 253, 0.75) 40%, 
        rgba(125, 211, 252, 0.7) 80%,
        rgba(56, 189, 248, 0.8) 100%);
    }

    /* Light Rays Effect */
    .light-rays {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 100%;
      background: repeating-linear-gradient(
        105deg,
        rgba(255, 255, 255, 0.25) 0px,
        rgba(255, 255, 255, 0.25) 30px,
        transparent 30px,
        transparent 90px
      );
      pointer-events: none;
      opacity: 0.6;
    }

    .water-surface {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 20px;
      background: linear-gradient(to bottom, rgba(255,255,255,0.7), transparent);
      border-bottom: 2px solid rgba(255,255,255,0.5);
      pointer-events: none;
    }

    canvas {
      width: 100%;
      height: 100%;
      display: block;
      cursor: crosshair;
    }

    .tank-banner {
      position: absolute;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 12px;
      color: #e2e8f0;
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .tank-banner i {
      color: #38bdf8;
    }

    .sidebar-footer {
      padding: 12px;
      border-top: 1px solid #334155;
      background: #0f172a;
      display: flex;
      gap: 8px;
    }

    .action-btn {
      flex: 1;
      padding: 8px;
      border-radius: 6px;
      border: none;
      font-weight: 600;
      font-size: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .btn-reset { background-color: #ef4444; color: white; }
    .btn-reset:hover { background-color: #dc2626; }
    .btn-clean { background-color: #0ea5e9; color: white; }
    .btn-clean:hover { background-color: #0284c7; }
  </style>
</head>
<body>

  <aside class="sidebar">
    <div class="sidebar-header">
      <i class="fa-solid fa-fish-fins"></i>
      <h1>투명 수조 커스텀</h1>
    </div>

    <div class="sidebar-content">
      <div>
        <div class="section-title"><i class="fa-solid fa-mountain-sun"></i> 바닥재 선택</div>
        <div class="btn-grid">
          <button class="tool-btn active" onclick="setGravel('gravel', this)"><i class="fa-solid fa-cubes"></i> 자연 자갈</button>
          <button class="tool-btn" onclick="setGravel('volcano', this)"><i class="fa-solid fa-volcano"></i> 화산석</button>
          <button class="tool-btn" onclick="setGravel('sand', this)"><i class="fa-solid fa-grip-lines-vertical"></i> 금사 모래</button>
          <button class="tool-btn" onclick="setGravel('crystal', this)"><i class="fa-solid fa-gem"></i> 크리스탈</button>
        </div>
      </div>

      <div>
        <div class="section-title"><i class="fa-solid fa-fan"></i> 수조 장비</div>
        <div class="btn-grid">
          <button class="tool-btn active" id="btn-air" onclick="toggleEquipment('air')"><i class="fa-solid fa-wind"></i> 기포기</button>
          <button class="tool-btn active" id="btn-filter" onclick="toggleEquipment('filter')"><i class="fa-solid fa-filter"></i> 여과기</button>
          <button class="tool-btn" id="btn-heater" onclick="toggleEquipment('heater')"><i class="fa-solid fa-temperature-high"></i> 히터기</button>
          <button class="tool-btn active" id="btn-moss" onclick="togglePlant()"><i class="fa-solid fa-seedling"></i> 마디 수초</button>
        </div>
      </div>

      <div>
        <div class="section-title"><i class="fa-solid fa-shrimp"></i> 생물 추가</div>
        <div class="btn-grid">
          <button class="tool-btn" onclick="addCreature('neon')"><i class="fa-solid fa-fish"></i> 네온테트라</button>
          <button class="tool-btn" onclick="addCreature('angel')"><i class="fa-solid fa-fish-fins"></i> 엔젤피쉬</button>
          <button class="tool-btn" onclick="addCreature('shrimp')"><i class="fa-solid fa-shrimp"></i> 체리새우</button>
          <button class="tool-btn" onclick="addCreature('turtle')"><i class="fa-solid fa-otter"></i> 거북이</button>
          <button class="tool-btn" onclick="addCreature('crab')"><i class="fa-solid fa-wine-glass"></i> 작은게</button>
          <button class="tool-btn" onclick="addCreature('puffer')"><i class="fa-solid fa-circle"></i> 복어</button>
        </div>
      </div>

      <div>
        <div class="section-title"><i class="fa-solid fa-bowl-food"></i> 먹이 선택</div>
        <div class="btn-grid">
          <button class="tool-btn active" id="food-floating" onclick="selectFood('floating')"><i class="fa-solid fa-cookie"></i> 열대어 먹이</button>
          <button class="tool-btn" id="food-bottom" onclick="selectFood('bottom')"><i class="fa-solid fa-dharmachakra"></i> 침강성 먹이</button>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="action-btn btn-clean" onclick="cleanFood()"><i class="fa-solid fa-broom"></i> 청소</button>
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 리셋</button>
    </div>
  </aside>

  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="water-surface"></div>
      <div class="light-rays"></div>
      <canvas id="aquariumCanvas"></canvas>
    </div>
    <div class="tank-banner">
      <i class="fa-solid fa-lightbulb"></i>
      <span>수조 안을 클릭해 먹이를 주세요. 체인 형태 마디 수초가 살랑살랑 움직입니다.</span>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');

    function resizeCanvas() {
      canvas.width = tankFrame.clientWidth;
      canvas.height = tankFrame.clientHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let currentGravel = 'gravel';
    let selectedFoodType = 'floating';
    let equipment = { air: true, filter: true, heater: false };
    let hasPlant = true;

    let creatures = [];
    let foods = [];
    let bubbles = [];

    const GRAVEL_HEIGHT = 45;

    const FOOD_TYPES = {
      floating: { color: '#f59e0b', size: 4, sinkSpeed: 0.8 },
      bottom: { color: '#ea580c', size: 6, sinkSpeed: 1.5 }
    };

    function random(min, max) {
      return Math.random() * (max - min) + min;
    }

    class Creature {
      constructor(type, x, y) {
        this.type = type;
        this.x = x || random(50, canvas.width - 50);
        this.y = y || random(100, canvas.height - GRAVEL_HEIGHT - 50);
        this.vx = random(-1.5, 1.5);
        this.vy = random(-0.5, 0.5);
        this.size = 20;
        this.facingRight = this.vx > 0;
        this.isBottomDweller = false;
        this.tailAngle = 0;

        if (type === 'neon') {
          this.size = 16;
        } else if (type === 'angel') {
          this.size = 26;
        } else if (type === 'shrimp') {
          this.size = 14;
          this.isBottomDweller = true;
          this.y = canvas.height - GRAVEL_HEIGHT - 10;
        } else if (type === 'turtle') {
          this.size = 24;
        } else if (type === 'crab') {
          this.size = 20;
          this.isBottomDweller = true;
          this.y = canvas.height - GRAVEL_HEIGHT - 12;
        } else if (type === 'puffer') {
          this.size = 20;
        }
      }

      update() {
        const floorY = canvas.height - GRAVEL_HEIGHT - this.size / 2;

        let nearestFood = null;
        let minDist = 250;

        for (let f of foods) {
          let d = Math.hypot(f.x - this.x, f.y - this.y);
          if (d < minDist) {
            minDist = d;
            nearestFood = f;
          }
        }

        if (nearestFood) {
          let dx = nearestFood.x - this.x;
          let dy = nearestFood.y - this.y;
          let angle = Math.atan2(dy, dx);
          let speed = this.isBottomDweller ? 1.2 : 1.8;

          this.vx = Math.cos(angle) * speed;
          if (!this.isBottomDweller) this.vy = Math.sin(angle) * speed;

          if (minDist < this.size / 2 + 6) {
            let index = foods.indexOf(nearestFood);
            if (index > -1) {
              foods.splice(index, 1);
              for (let i = 0; i < 3; i++) {
                bubbles.push(new Bubble(this.x, this.y, random(2, 4), random(0.5, 1.5)));
              }
            }
          }
        } else {
          if (Math.random() < 0.02) {
            this.vx = random(-1.5, 1.5);
            if (!this.isBottomDweller) this.vy = random(-0.8, 0.8);
          }
        }

        this.x += this.vx;

        if (this.isBottomDweller) {
          this.y = floorY;
          this.vy = 0;
        } else {
          this.y += this.vy;
          if (this.y < 40) { this.y = 40; this.vy *= -1; }
          if (this.y > floorY) { this.y = floorY; this.vy *= -1; }
        }

        if (this.x < 30) { this.x = 30; this.vx *= -1; }
        if (this.x > canvas.width - 30) { this.x = canvas.width - 30; this.vx *= -1; }

        if (Math.abs(this.vx) > 0.1) this.facingRight = this.vx > 0;
        this.tailAngle += 0.15;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        if (!this.facingRight) ctx.scale(-1, 1);

        if (this.type === 'neon') {
          ctx.fillStyle = '#0284c7';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 2.5, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(-this.size + 4, -2);
          ctx.lineTo(this.size - 4, -2);
          ctx.stroke();

          ctx.fillStyle = '#ef4444';
          ctx.beginPath();
          ctx.ellipse(-this.size / 2, 2, this.size / 3, 2.5, 0, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'angel') {
          ctx.fillStyle = '#f8fafc';
          ctx.beginPath();
          ctx.moveTo(this.size / 2, 0);
          ctx.lineTo(-this.size / 2, -this.size / 1.5);
          ctx.lineTo(-this.size / 3, 0);
          ctx.lineTo(-this.size / 2, this.size / 1.5);
          ctx.closePath();
          ctx.fill();

          ctx.fillStyle = '#334155';
          ctx.fillRect(-2, -this.size / 2, 3, this.size);

        } else if (this.type === 'shrimp') {
          ctx.fillStyle = '#ef4444';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 3, 0, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d';
          ctx.beginPath();
          ctx.ellipse(0, -4, this.size, this.size / 1.4, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#22c55e';
          ctx.beginPath();
          ctx.arc(this.size + 2, -2, 5, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'crab') {
          ctx.fillStyle = '#f97316';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 1.6, 0, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15';
          ctx.beginPath();
          ctx.arc(0, 0, this.size, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#0f172a';
          ctx.beginPath();
          ctx.arc(6, -4, 3, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();
      }
    }

    class Food {
      constructor(x, y, typeKey) {
        this.x = x;
        this.y = y;
        this.type = FOOD_TYPES[typeKey];
        this.radius = this.type.size;
        this.color = this.type.color;
        this.sinkSpeed = this.type.sinkSpeed;
      }

      update() {
        const floorY = canvas.height - GRAVEL_HEIGHT + 8 - this.radius;
        if (this.y < floorY) {
          this.y += this.sinkSpeed;
          this.x += Math.sin(this.y * 0.05) * 0.3;
        } else {
          this.y = floorY;
        }
      }

      draw() {
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }

    class Bubble {
      constructor(x, y, radius, speed) {
        this.x = x || random(20, canvas.width - 20);
        this.y = y || canvas.height - GRAVEL_HEIGHT;
        this.radius = radius || random(2, 5);
        this.speed = speed || random(1, 2.2);
        this.wobble = random(0, Math.PI * 2);
      }

      update() {
        this.y -= this.speed;
        this.wobble += 0.05;
        this.x += Math.sin(this.wobble) * 0.5;
      }

      draw() {
        ctx.save();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.restore();
      }
    }

    function initTank() {
      creatures = [
        new Creature('neon', 150, 200),
        new Creature('neon', 220, 240),
        new Creature('angel', 400, 180),
        new Creature('shrimp', 300, 0),
        new Creature('turtle', 500, 300),
        new Creature('crab', 600, 0),
        new Creature('puffer', 250, 320)
      ];
    }
    initTank();

    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      for (let i = 0; i < 3; i++) {
        foods.push(new Food(clickX + random(-10, 10), clickY + random(-10, 10), selectedFoodType));
      }
    });

    function setGravel(type, btn) {
      currentGravel = type;
      btn.parentElement.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function selectFood(type) {
      selectedFoodType = type;
      document.getElementById('food-floating').classList.toggle('active', type === 'floating');
      document.getElementById('food-bottom').classList.toggle('active', type === 'bottom');
    }

    function toggleEquipment(eq) {
      equipment[eq] = !equipment[eq];
      const btn = document.getElementById(`btn-${eq}`);
      if (btn) btn.classList.toggle('active', equipment[eq]);
    }

    function togglePlant() {
      hasPlant = !hasPlant;
      document.getElementById('btn-moss').classList.toggle('active', hasPlant);
    }

    function addCreature(type) {
      creatures.push(new Creature(type));
    }

    function cleanFood() { foods = []; }

    function resetTank() {
      foods = [];
      bubbles = [];
      initTank();
    }

    function drawGravel() {
      const gHeight = GRAVEL_HEIGHT;
      const yStart = canvas.height - gHeight;

      if (currentGravel === 'gravel') {
        ctx.fillStyle = '#d97706';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
      } else if (currentGravel === 'volcano') {
        ctx.fillStyle = '#334155';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
      } else if (currentGravel === 'sand') {
        ctx.fillStyle = '#fde047';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
      } else if (currentGravel === 'crystal') {
        ctx.fillStyle = '#e0f2fe';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
      }
    }

    /* SEGMENTED CHAIN PLANTS (마디마디 잎 수초) */
    function drawPlants() {
      if (!hasPlant) return;

      ctx.save();
      const plantY = canvas.height - GRAVEL_HEIGHT + 8;
      const time = Date.now() * 0.0025;

      function drawStemPlant(baseX, totalHeight, leafColor, stemColor, phaseOffset) {
        const segments = 15;
        const segHeight = totalHeight / segments;

        let prevX = baseX;
        let prevY = plantY;

        for (let i = 1; i <= segments; i++) {
          const progress = i / segments;
          const sway = Math.sin(time + phaseOffset + progress * 2.2) * (progress * 20);
          const currentX = baseX + sway;
          const currentY = plantY - (i * segHeight);

          ctx.strokeStyle = stemColor;
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(currentX, currentY);
          ctx.stroke();

          ctx.save();
          ctx.translate(currentX, currentY);

          const angle = Math.atan2(currentY - prevY, currentX - prevX) + Math.PI / 2;
          ctx.rotate(angle);

          const leafSize = 8 + (1 - progress) * 4;
          ctx.fillStyle = leafColor;

          ctx.beginPath();
          ctx.ellipse(-leafSize * 0.8, -2, leafSize, leafSize * 0.45, -0.3, 0, Math.PI * 2);
          ctx.fill();

          ctx.beginPath();
          ctx.ellipse(leafSize * 0.8, -2, leafSize, leafSize * 0.45, 0.3, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();

          prevX = currentX;
          prevY = currentY;
        }
      }

      drawStemPlant(70, 180, '#16a34a', '#15803d', 0);
      drawStemPlant(95, 210, '#22c55e', '#166534', 0.8);
      drawStemPlant(120, 160, '#4ade80', '#15803d', 1.5);

      drawStemPlant(canvas.width - 240, 170, '#15803d', '#166534', 2.1);
      drawStemPlant(canvas.width - 215, 220, '#22c55e', '#15803d', 2.8);

      drawStemPlant(canvas.width - 100, 160, '#16a34a', '#15803d', 1.2);
      drawStemPlant(canvas.width - 75, 190, '#4ade80', '#166534', 0.4);

      ctx.restore();
    }

    function drawEquipmentVisuals() {
      if (equipment.air) {
        if (Math.random() < 0.4) bubbles.push(new Bubble(100, canvas.height - GRAVEL_HEIGHT));
        if (Math.random() < 0.4) bubbles.push(new Bubble(canvas.width - 100, canvas.height - GRAVEL_HEIGHT));
      }

      if (equipment.filter) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fillRect(canvas.width - 70, 0, 50, 100);
      }

      if (equipment.heater) {
        ctx.fillStyle = '#64748b';
        ctx.fillRect(30, 60, 10, 160);
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(32, 160, 6, 40);
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawGravel();
      drawPlants();
      drawEquipmentVisuals();

      for (let i = bubbles.length - 1; i >= 0; i--) {
        bubbles[i].update();
        bubbles[i].draw();
        if (bubbles[i].y < 0) bubbles.splice(i, 1);
      }

      for (let f of foods) {
        f.update();
        f.draw();
      }

      for (let c of creatures) {
        c.update();
        c.draw();
      }

      requestAnimationFrame(animate);
    }

    animate();
  </script>
</body>
</html>
"""

# Streamlit HTML 컴포넌트 렌더링 (높이 지정)
components.html(html_code, height=750, scrolling=False)
