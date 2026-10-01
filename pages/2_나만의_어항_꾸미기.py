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
      width: 320px;
      background-color: #1e293b;
      border-right: 1px solid #334155;
      display: flex;
      flex-direction: column;
      z-index: 10;
      box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
    }

    .sidebar-header {
      padding: 20px;
      background-color: #0f172a;
      border-bottom: 1px solid #334155;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sidebar-header i {
      font-size: 24px;
      color: #38bdf8;
    }

    .sidebar-header h1 {
      font-size: 18px;
      font-weight: 700;
      color: #f1f5f9;
    }

    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .section-title {
      font-size: 13px;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .tool-btn {
      background-color: #334155;
      color: #e2e8f0;
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      text-align: left;
    }

    .tool-btn:hover {
      background-color: #475569;
      color: #ffffff;
      border-color: #38bdf8;
      transform: translateY(-1px);
    }

    .tool-btn.active {
      background-color: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    .tool-btn i {
      font-size: 14px;
      color: #38bdf8;
      width: 18px;
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
      padding: 24px;
      background: radial-gradient(circle at center, #1e293b 0%, #090d16 100%);
    }

    /* Crystal Clear Glass Tank Design */
    .glass-tank-frame {
      position: relative;
      width: 100%;
      max-width: 1100px;
      height: 90vh;
      max-height: 720px;
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

    /* Water surface glow */
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

    /* Bottom Info Banner */
    .tank-banner {
      position: absolute;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 8px 18px;
      border-radius: 20px;
      font-size: 13px;
      color: #e2e8f0;
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .tank-banner i {
      color: #38bdf8;
    }

    /* Controls footer */
    .sidebar-footer {
      padding: 16px;
      border-top: 1px solid #334155;
      background: #0f172a;
      display: flex;
      gap: 8px;
    }

    .action-btn {
      flex: 1;
      padding: 10px;
      border-radius: 8px;
      border: none;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-reset {
      background-color: #ef4444;
      color: white;
    }
    .btn-reset:hover {
      background-color: #dc2626;
    }

    .btn-clean {
      background-color: #0ea5e9;
      color: white;
    }
    .btn-clean:hover {
      background-color: #0284c7;
    }
  </style>
</head>
<body>

  <!-- Left Control Panel -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <i class="fa-solid fa-fish-fins"></i>
      <h1>투명 수조 커스텀</h1>
    </div>

    <div class="sidebar-content">
      <!-- 1. 지형 / 바닥재 -->
      <div>
        <div class="section-title"><i class="fa-solid fa-mountain-sun"></i> 바닥재 선택</div>
        <div class="btn-grid">
          <button class="tool-btn active" onclick="setGravel('gravel')"><i class="fa-solid fa-cubes"></i> 자연 자갈</button>
          <button class="tool-btn" onclick="setGravel('volcano')"><i class="fa-solid fa-volcano"></i> 화산석</button>
          <button class="tool-btn" onclick="setGravel('sand')"><i class="fa-solid fa-grip-lines-vertical"></i> 금사 모래</button>
          <button class="tool-btn" onclick="setGravel('crystal')"><i class="fa-solid fa-gem"></i> 크리스탈</button>
        </div>
      </div>

      <!-- 2. 장비 / 데코 -->
      <div>
        <div class="section-title"><i class="fa-solid fa-fan"></i> 여과 및 수조 장비</div>
        <div class="btn-grid">
          <button class="tool-btn active" id="btn-air" onclick="toggleEquipment('air')"><i class="fa-solid fa-wind"></i> 기포기 (버블)</button>
          <button class="tool-btn active" id="btn-filter" onclick="toggleEquipment('filter')"><i class="fa-solid fa-filter"></i> 걸이식 여과기</button>
          <button class="tool-btn" id="btn-heater" onclick="toggleEquipment('heater')"><i class="fa-solid fa-temperature-high"></i> 히터기</button>
          <button class="tool-btn active" id="btn-moss" onclick="togglePlant()"><i class="fa-solid fa-seedling"></i> 프리미엄 수초</button>
        </div>
      </div>

      <!-- 3. 생물 추가 -->
      <div>
        <div class="section-title"><i class="fa-solid fa-shrimp"></i> 생물 추가</div>
        <div class="btn-grid">
          <button class="tool-btn" onclick="addCreature('neon')"><i class="fa-solid fa-fish"></i> 네온테트라</button>
          <button class="tool-btn" onclick="addCreature('angel')"><i class="fa-solid fa-fish-fins"></i> 엔젤피쉬</button>
          <button class="tool-btn" onclick="addCreature('shrimp')"><i class="fa-solid fa-shrimp"></i> 체리새우</button>
          <button class="tool-btn" onclick="addCreature('turtle')"><i class="fa-solid fa-otter"></i> 미니거북이</button>
          <button class="tool-btn" onclick="addCreature('crab')"><i class="fa-solid fa-wine-glass"></i> 꽃게/작은게</button>
          <button class="tool-btn" onclick="addCreature('puffer')"><i class="fa-solid fa-circle"></i> 복어</button>
        </div>
      </div>

      <!-- 4. 먹이 선택 -->
      <div>
        <div class="section-title"><i class="fa-solid fa-bowl-food"></i> 먹이 주기 (수조 클릭)</div>
        <div class="btn-grid">
          <button class="tool-btn active" id="food-floating" onclick="selectFood('floating')"><i class="fa-solid fa-cookie"></i> 열대어 사료</button>
          <button class="tool-btn" id="food-bottom" onclick="selectFood('bottom')"><i class="fa-solid fa-dharmachakra"></i> 새우/저서 사료</button>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="action-btn btn-clean" onclick="cleanFood()"><i class="fa-solid fa-broom"></i> 먹이 청소</button>
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 리셋</button>
    </div>
  </aside>

  <!-- Main View Area -->
  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="water-surface"></div>
      <div class="light-rays"></div>
      <canvas id="aquariumCanvas"></canvas>
    </div>
    <div class="tank-banner">
      <i class="fa-solid fa-lightbulb"></i>
      <span>수조 안을 클릭하면 먹이가 떨어집니다. 마디마디 잎이 달린 수초를 자유롭게 세팅해보세요!</span>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');

    // Canvas Resizing
    function resizeCanvas() {
      canvas.width = tankFrame.clientWidth;
      canvas.height = tankFrame.clientHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // State
    let currentGravel = 'gravel';
    let selectedFoodType = 'floating';
    let equipment = { air: true, filter: true, heater: false };
    let hasPlant = true;

    // Entities
    let creatures = [];
    let foods = [];
    let bubbles = [];

    // Gravel heights
    const GRAVEL_HEIGHT = 50;

    // Food Types Config
    const FOOD_TYPES = {
      floating: { color: '#f59e0b', size: 5, sinkSpeed: 0.8, isBottom: false },
      bottom: { color: '#ea580c', size: 7, sinkSpeed: 1.5, isBottom: true }
    };

    // Helper: Random range
    function random(min, max) {
      return Math.random() * (max - min) + min;
    }

    // Creature Class
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

        // Type Specific Properties
        if (type === 'neon') {
          this.color = '#0284c7';
          this.stripe = '#38bdf8';
          this.size = 18;
        } else if (type === 'angel') {
          this.color = '#f8fafc';
          this.stripe = '#334155';
          this.size = 28;
        } else if (type === 'shrimp') {
          this.color = '#ef4444';
          this.size = 16;
          this.isBottomDweller = true;
          this.y = canvas.height - GRAVEL_HEIGHT - 10;
        } else if (type === 'turtle') {
          this.color = '#15803d';
          this.size = 26;
          this.isBottomDweller = false;
        } else if (type === 'crab') {
          this.color = '#f97316';
          this.size = 22;
          this.isBottomDweller = true;
          this.y = canvas.height - GRAVEL_HEIGHT - 12;
        } else if (type === 'puffer') {
          this.color = '#facc15';
          this.size = 22;
        }
      }

      update() {
        const floorY = canvas.height - GRAVEL_HEIGHT - this.size / 2;

        // 1. Food Detection AI
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
          if (!this.isBottomDweller) {
            this.vy = Math.sin(angle) * speed;
          }

          if (minDist < this.size / 2 + 8) {
            let index = foods.indexOf(nearestFood);
            if (index > -1) {
              foods.splice(index, 1);
              for (let i = 0; i < 4; i++) {
                bubbles.push(new Bubble(this.x, this.y, random(2, 4), random(0.5, 1.5)));
              }
            }
          }
        } else {
          if (Math.random() < 0.02) {
            this.vx = random(-1.5, 1.5);
            if (!this.isBottomDweller) {
              this.vy = random(-0.8, 0.8);
            }
          }
        }

        this.x += this.vx;

        if (this.isBottomDweller) {
          this.y = floorY;
          this.vy = 0;
        } else {
          this.y += this.vy;

          if (this.y < 40) {
            this.y = 40;
            this.vy *= -1;
          }
          if (this.y > floorY) {
            this.y = floorY;
            this.vy *= -1;
          }
        }

        if (this.x < 30) {
          this.x = 30;
          this.vx *= -1;
        }
        if (this.x > canvas.width - 30) {
          this.x = canvas.width - 30;
          this.vx *= -1;
        }

        if (Math.abs(this.vx) > 0.1) {
          this.facingRight = this.vx > 0;
        }

        this.tailAngle += 0.15;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        if (!this.facingRight) {
          ctx.scale(-1, 1);
        }

        if (this.type === 'neon') {
          ctx.fillStyle = '#0284c7';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 2.5, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(-this.size + 4, -2);
          ctx.lineTo(this.size - 4, -2);
          ctx.stroke();

          ctx.fillStyle = '#ef4444';
          ctx.beginPath();
          ctx.ellipse(-this.size / 2, 2, this.size / 3, 3, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = 'rgba(255,255,255,0.7)';
          let tailWiggle = Math.sin(this.tailAngle) * 4;
          ctx.beginPath();
          ctx.moveTo(-this.size, 0);
          ctx.lineTo(-this.size - 8, -6 + tailWiggle);
          ctx.lineTo(-this.size - 8, 6 + tailWiggle);
          ctx.closePath();
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
          ctx.fillRect(-2, -this.size / 2, 4, this.size);

          ctx.fillStyle = '#0f172a';
          ctx.beginPath();
          ctx.arc(8, -4, 3, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'shrimp') {
          ctx.fillStyle = '#ef4444';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 3, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#fca5a5';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(this.size, -2);
          ctx.lineTo(this.size + 10, -8);
          ctx.stroke();

          ctx.beginPath();
          for (let i = -5; i <= 5; i += 4) {
            ctx.moveTo(i, 3);
            ctx.lineTo(i + 2, 8);
          }
          ctx.stroke();

        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d';
          ctx.beginPath();
          ctx.ellipse(0, -4, this.size, this.size / 1.4, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#166534';
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.fillStyle = '#22c55e';
          ctx.beginPath();
          ctx.arc(this.size + 2, -2, 6, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#000';
          ctx.beginPath();
          ctx.arc(this.size + 4, -4, 1.5, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#22c55e';
          ctx.beginPath();
          ctx.ellipse(8, 8, 8, 4, Math.PI / 4, 0, Math.PI * 2);
          ctx.ellipse(-8, 8, 6, 3, -Math.PI / 4, 0, Math.PI * 2);
          ctx.fill();

        } else if (this.type === 'crab') {
          ctx.fillStyle = '#f97316';
          ctx.beginPath();
          ctx.ellipse(0, 0, this.size, this.size / 1.6, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.beginPath();
          ctx.arc(this.size - 2, -this.size / 2, 6, 0, Math.PI * 2);
          ctx.arc(-this.size + 2, -this.size / 2, 6, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#0f172a';
          ctx.beginPath();
          ctx.arc(6, -8, 2, 0, Math.PI * 2);
          ctx.arc(-6, -8, 2, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#ea580c';
          ctx.lineWidth = 2;
          ctx.beginPath();
          for (let side of [-1, 1]) {
            ctx.moveTo(side * 8, 4);
            ctx.lineTo(side * 14, 10);
            ctx.moveTo(side * 4, 4);
            ctx.lineTo(side * 10, 12);
          }
          ctx.stroke();

        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15';
          ctx.beginPath();
          ctx.arc(0, 0, this.size, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#fef08a';
          ctx.beginPath();
          ctx.arc(2, 4, this.size * 0.7, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#0f172a';
          ctx.beginPath();
          ctx.arc(8, -4, 3.5, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();
      }
    }

    // Food Class
    class Food {
      constructor(x, y, typeKey) {
        this.x = x;
        this.y = y;
        this.type = FOOD_TYPES[typeKey];
        this.radius = this.type.size;
        this.color = this.type.color;
        this.sinkSpeed = this.type.sinkSpeed;
        this.isLanded = false;
      }

      update() {
        const floorY = canvas.height - GRAVEL_HEIGHT + 10 - this.radius;

        if (this.y < floorY) {
          this.y += this.sinkSpeed;
          this.x += Math.sin(this.y * 0.05) * 0.3;
        } else {
          this.y = floorY;
          this.isLanded = true;
        }
      }

      draw() {
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'rgba(255,255,255,0.4)';
        ctx.beginPath();
        ctx.arc(this.x - 1.5, this.y - 1.5, this.radius * 0.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }

    // Bubble Class
    class Bubble {
      constructor(x, y, radius, speed) {
        this.x = x || random(20, canvas.width - 20);
        this.y = y || canvas.height - GRAVEL_HEIGHT;
        this.radius = radius || random(2, 6);
        this.speed = speed || random(1, 2.5);
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

    // Initial Default Setup
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

    // Click canvas to drop food
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      for (let i = 0; i < 3; i++) {
        foods.push(new Food(clickX + random(-12, 12), clickY + random(-10, 10), selectedFoodType));
      }
    });

    // Control Functions
    function setGravel(type) {
      currentGravel = type;
      document.querySelectorAll('.tool-btn').forEach(btn => {
        if (btn.getAttribute('onclick')?.includes('setGravel')) {
          btn.classList.remove('active');
        }
      });
      event.currentTarget.classList.add('active');
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

    function cleanFood() {
      foods = [];
    }

    function resetTank() {
      foods = [];
      bubbles = [];
      initTank();
    }

    // Drawing Gravel / Ground
    function drawGravel() {
      const gHeight = GRAVEL_HEIGHT;
      const yStart = canvas.height - gHeight;

      if (currentGravel === 'gravel') {
        ctx.fillStyle = '#d97706';
        ctx.fillRect(0, yStart, canvas.width, gHeight);

        ctx.fillStyle = '#b45309';
        for (let x = 10; x < canvas.width; x += 20) {
          ctx.beginPath();
          ctx.arc(x, yStart + 15, 8, 0, Math.PI * 2);
          ctx.arc(x + 10, yStart + 30, 10, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (currentGravel === 'volcano') {
        ctx.fillStyle = '#334155';
        ctx.fillRect(0, yStart, canvas.width, gHeight);

        ctx.fillStyle = '#1e293b';
        for (let x = 15; x < canvas.width; x += 25) {
          ctx.beginPath();
          ctx.arc(x, yStart + 20, 12, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (currentGravel === 'sand') {
        ctx.fillStyle = '#fde047';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
        ctx.fillStyle = '#eab308';
        ctx.fillRect(0, yStart, canvas.width, 6);
      } else if (currentGravel === 'crystal') {
        ctx.fillStyle = '#e0f2fe';
        ctx.fillRect(0, yStart, canvas.width, gHeight);
        ctx.fillStyle = '#bae6fd';
        for (let x = 10; x < canvas.width; x += 18) {
          ctx.beginPath();
          ctx.arc(x, yStart + 15, 6, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    // NEW REALISTIC CHAIN/SEGMENTED AQUATIC PLANTS (마디 마디 잎사귀 수초)
    function drawPlants() {
      if (!hasPlant) return;

      ctx.save();
      const plantY = canvas.height - GRAVEL_HEIGHT + 10;
      const time = Date.now() * 0.0025;

      // Helper to render a segmented "chain-like" stem plant (Anacharis/Elodea style)
      function drawStemPlant(baseX, totalHeight, leafColor, stemColor, phaseOffset) {
        const segments = 16;
        const segHeight = totalHeight / segments;

        let prevX = baseX;
        let prevY = plantY;

        for (let i = 1; i <= segments; i++) {
          const progress = i / segments;
          const sway = Math.sin(time + phaseOffset + progress * 2.2) * (progress * 22);
          const currentX = baseX + sway;
          const currentY = plantY - (i * segHeight);

          // 1. Draw central stem segment
          ctx.strokeStyle = stemColor;
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(currentX, currentY);
          ctx.stroke();

          // 2. Draw leaf node (creates realistic chain/segmented leaf look)
          ctx.save();
          ctx.translate(currentX, currentY);

          // Calculate stem tilt
          const angle = Math.atan2(currentY - prevY, currentX - prevX) + Math.PI / 2;
          ctx.rotate(angle);

          // Leaf cluster (Left & Right pairs)
          const leafSize = 9 + (1 - progress) * 5; // Larger near base
          ctx.fillStyle = leafColor;

          // Left leaf
          ctx.beginPath();
          ctx.ellipse(-leafSize * 0.8, -2, leafSize, leafSize * 0.45, -0.3, 0, Math.PI * 2);
          ctx.fill();

          // Right leaf
          ctx.beginPath();
          ctx.ellipse(leafSize * 0.8, -2, leafSize, leafSize * 0.45, 0.3, 0, Math.PI * 2);
          ctx.fill();

          // Node center dot highlight
          ctx.fillStyle = '#86efac';
          ctx.beginPath();
          ctx.arc(0, 0, 2, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();

          prevX = currentX;
          prevY = currentY;
        }
      }

      // Draw multiple plant clusters on the bottom of the aquarium
      // Group 1: Left Cluster
      drawStemPlant(70, 180, '#16a34a', '#15803d', 0);
      drawStemPlant(95, 210, '#22c55e', '#166534', 0.8);
      drawStemPlant(120, 160, '#4ade80', '#15803d', 1.5);

      // Group 2: Middle-Right Cluster
      drawStemPlant(canvas.width - 240, 170, '#15803d', '#166534', 2.1);
      drawStemPlant(canvas.width - 215, 220, '#22c55e', '#15803d', 2.8);

      // Group 3: Right Cluster
      drawStemPlant(canvas.width - 100, 160, '#16a34a', '#15803d', 1.2);
      drawStemPlant(canvas.width - 75, 190, '#4ade80', '#166534', 0.4);

      ctx.restore();
    }

    // Equipment Visuals
    function drawEquipmentVisuals() {
      // Air Bubbler
      if (equipment.air) {
        if (Math.random() < 0.4) {
          bubbles.push(new Bubble(100, canvas.height - GRAVEL_HEIGHT));
        }
        if (Math.random() < 0.4) {
          bubbles.push(new Bubble(canvas.width - 100, canvas.height - GRAVEL_HEIGHT));
        }
      }

      // Filter Water Flow (Right Side)
      if (equipment.filter) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fillRect(canvas.width - 70, 0, 50, 120);

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(canvas.width - 45, 120, 20, 0, Math.PI);
        ctx.stroke();
      }

      // Heater (Left side red glow)
      if (equipment.heater) {
        ctx.fillStyle = '#64748b';
        ctx.fillRect(30, 60, 12, 180);
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(33, 180, 6, 50);

        ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
        ctx.beginPath();
        ctx.arc(36, 200, 40, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Main Render Loop
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 1. Draw Background Decor & Ground
      drawGravel();
      drawPlants();
      drawEquipmentVisuals();

      // 2. Bubbles Update & Draw
      for (let i = bubbles.length - 1; i >= 0; i--) {
        bubbles[i].update();
        bubbles[i].draw();
        if (bubbles[i].y < 0) {
          bubbles.splice(i, 1);
        }
      }

      // 3. Foods Update & Draw
      for (let f of foods) {
        f.update();
        f.draw();
      }

      // 4. Creatures Update & Draw
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
```eof

### 🌿 수초 그래픽 개선 내용
1. **마디 마디 잎사귀 체인 그래픽 구조**: 줄기 마디마다 양쪽으로 타원형 잎사귀가 촘촘하게 달려 상하로 이어지는 진짜 수초(검정말/아나카리스 형태) 그래픽으로 변경되었습니다.
2. **자연스러운 수중 흔들림**: 수류 움직임에 따라 마디별 각도와 잎사귀 위치가 곡선을 그리며 유기적으로 살랑살랑 흔들립니다.
