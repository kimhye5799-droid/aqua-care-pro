import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="울트라 샌드박스 어항 시뮬레이터", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>울트라 샌드박스 어항 시뮬레이터</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #0b0f19;
      color: #f8fafc;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* Sidebar Layout */
    .sidebar {
      width: 340px;
      background-color: #151d2a;
      border-right: 1px solid #2a374a;
      display: flex;
      flex-direction: column;
      z-index: 20;
      transition: margin-left 0.3s ease;
      position: relative;
    }

    .sidebar.collapsed {
      margin-left: -340px;
    }

    .sidebar-toggle-btn {
      position: absolute;
      right: -36px;
      top: 16px;
      width: 36px;
      height: 36px;
      background: #151d2a;
      border: 1px solid #2a374a;
      border-left: none;
      border-radius: 0 8px 8px 0;
      color: #38bdf8;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 30;
      box-shadow: 4px 0 10px rgba(0,0,0,0.3);
    }

    .sidebar-header {
      padding: 14px 16px;
      background-color: #0b0f19;
      border-bottom: 1px solid #2a374a;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .sidebar-header i { font-size: 20px; color: #38bdf8; }
    .sidebar-header h1 { font-size: 15px; font-weight: 700; color: #f1f5f9; }

    /* Category Tabs */
    .tab-bar {
      display: flex;
      background: #0f172a;
      border-bottom: 1px solid #2a374a;
    }

    .tab-btn {
      flex: 1;
      padding: 10px 4px;
      font-size: 11px;
      font-weight: 600;
      color: #94a3b8;
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .tab-btn:hover { color: #e2e8f0; }
    .tab-btn.active {
      color: #38bdf8;
      border-bottom-color: #38bdf8;
      background: rgba(56, 189, 248, 0.05);
    }

    .tab-content {
      flex: 1;
      overflow-y: auto;
      padding: 14px;
      display: none;
      flex-direction: column;
      gap: 14px;
    }

    .tab-content.active { display: flex; }

    .section-title {
      font-size: 11px;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      margin-bottom: 6px;
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
      background-color: #222e3e;
      color: #e2e8f0;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 11px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .tool-btn:hover { background-color: #334155; border-color: #38bdf8; }
    .tool-btn.active {
      background-color: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
    }

    .slider-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
      background: #1e293b;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid #334155;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #cbd5e1;
    }

    .slider-group input[type="range"] {
      width: 100%;
      accent-color: #38bdf8;
      cursor: pointer;
    }

    .color-picker-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #1e293b;
      padding: 8px 10px;
      border-radius: 8px;
      border: 1px solid #334155;
      font-size: 11px;
    }

    .color-picker-row input[type="color"] {
      border: none;
      width: 28px;
      height: 28px;
      border-radius: 4px;
      cursor: pointer;
      background: none;
    }

    /* Main Container */
    .aquarium-container {
      flex: 1;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      background: radial-gradient(circle at center, #151d2a 0%, #05070c 100%);
    }

    .glass-tank-frame {
      position: relative;
      width: 100%;
      height: 86vh;
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(255, 255, 255, 0.4);
      border: 4px solid rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(2px);
      overflow: hidden;
      transition: background 0.3s ease;
    }

    canvas { width: 100%; height: 100%; display: block; }

    /* Environment Status Overlay */
    .status-overlay {
      position: absolute;
      top: 14px;
      left: 14px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 8px 14px;
      border-radius: 10px;
      display: flex;
      gap: 16px;
      font-size: 11px;
      z-index: 10;
      pointer-events: none;
    }

    .status-item { display: flex; align-items: center; gap: 6px; }
    .status-item i { color: #38bdf8; }

    /* Inspection Modal */
    .inspect-popup {
      position: absolute;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #38bdf8;
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 11px;
      color: #f8fafc;
      pointer-events: none;
      display: none;
      z-index: 30;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      backdrop-filter: blur(6px);
      min-width: 160px;
    }

    .inspect-title { font-weight: 700; color: #38bdf8; margin-bottom: 4px; border-bottom: 1px solid #334155; padding-bottom: 2px; }

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
      font-size: 11px;
      color: #e2e8f0;
      pointer-events: none;
    }

    .sidebar-footer {
      padding: 10px;
      border-top: 1px solid #2a374a;
      background: #0b0f19;
      display: flex;
      gap: 6px;
    }

    .action-btn {
      flex: 1;
      padding: 8px;
      border-radius: 6px;
      border: none;
      font-weight: 600;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      color: white;
    }
    .btn-snap { background-color: #10b981; }
    .btn-clean { background-color: #0ea5e9; }
    .btn-reset { background-color: #ef4444; }
  </style>
</head>
<body>

  <aside class="sidebar" id="sidebar">
    <button class="sidebar-toggle-btn" onclick="toggleSidebar()"><i class="fa-solid fa-bars"></i></button>

    <div class="sidebar-header">
      <i class="fa-solid fa-fish-fins"></i>
      <h1>울트라 샌드박스 어항</h1>
    </div>

    <!-- Tab Bar Navigation -->
    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tab-mode')"><i class="fa-solid fa-hand-pointer"></i>모드</button>
      <button class="tab-btn" onclick="switchTab('tab-env')"><i class="fa-solid fa-sliders"></i>환경</button>
      <button class="tab-btn" onclick="switchTab('tab-decor')"><i class="fa-solid fa-seedling"></i>장식</button>
      <button class="tab-btn" onclick="switchTab('tab-fish')"><i class="fa-solid fa-fish"></i>생물</button>
    </nav>

    <!-- TAB 1: Mode & Interaction -->
    <div class="tab-content active" id="tab-mode">
      <div class="section-title"><i class="fa-solid fa-hand-pointer"></i> 상호작용 도구</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="mode-feed" onclick="setInteractionMode('feed')"><i class="fa-solid fa-cookie"></i> 먹이 주기</button>
        <button class="tool-btn" id="mode-drag" onclick="setInteractionMode('drag')"><i class="fa-solid fa-up-down-left-right"></i> 자유 배치</button>
        <button class="tool-btn" id="mode-inspect" onclick="setInteractionMode('inspect')"><i class="fa-solid fa-magnifying-glass"></i> 관찰(Inspect)</button>
        <button class="tool-btn" id="mode-delete" onclick="setInteractionMode('delete')"><i class="fa-solid fa-eraser"></i> 개체 삭제</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-bowl-food"></i> 먹이 종류</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="food-floating" onclick="selectFood('floating')"><i class="fa-solid fa-cookie"></i> 부유성 먹이</button>
        <button class="tool-btn" id="food-bottom" onclick="selectFood('bottom')"><i class="fa-solid fa-dharmachakra"></i> 침강성 먹이</button>
      </div>
    </div>

    <!-- TAB 2: Environment Simulation -->
    <div class="tab-content" id="tab-env">
      <div class="section-title"><i class="fa-solid fa-temperature-high"></i> 수온 시뮬레이션</div>
      <div class="slider-group">
        <div class="slider-header"><span>수온 설정</span><span id="temp-val">24°C</span></div>
        <input type="range" id="temp-slider" min="15" max="35" value="24" oninput="updateTemperature(this.value)">
      </div>

      <div class="section-title"><i class="fa-solid fa-lightbulb"></i> 조명 피커 & 밝기</div>
      <div class="color-picker-row">
        <span>조명 색상 커스텀</span>
        <input type="color" id="light-color" value="#e0f2fe" onchange="updateLightColor(this.value)">
      </div>
      <div class="slider-group">
        <div class="slider-header"><span>조명 밝기</span><span id="light-val">80%</span></div>
        <input type="range" id="light-slider" min="20" max="100" value="80" oninput="updateLightBrightness(this.value)">
      </div>

      <div class="section-title"><i class="fa-solid fa-mountain-sun"></i> 바닥재 선택</div>
      <div class="btn-grid">
        <button class="tool-btn active" onclick="setGravel('gravel', this)"><i class="fa-solid fa-cubes"></i> 자연 자갈</button>
        <button class="tool-btn" onclick="setGravel('volcano', this)"><i class="fa-solid fa-volcano"></i> 화산석</button>
        <button class="tool-btn" onclick="setGravel('sand', this)"><i class="fa-solid fa-grip-lines-vertical"></i> 금사 모래</button>
        <button class="tool-btn" onclick="setGravel('crystal', this)"><i class="fa-solid fa-gem"></i> 크리스탈</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-fan"></i> 수조 장비</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="btn-air" onclick="toggleEquipment('air')"><i class="fa-solid fa-wind"></i> 기포기</button>
        <button class="tool-btn active" id="btn-filter" onclick="toggleEquipment('filter')"><i class="fa-solid fa-filter"></i> 여과기</button>
        <button class="tool-btn active" id="btn-heater" onclick="toggleEquipment('heater')"><i class="fa-solid fa-temperature-high"></i> 히터기</button>
      </div>
    </div>

    <!-- TAB 3: Decorations (Sandbox Placeables) -->
    <div class="tab-content" id="tab-decor">
      <div class="section-title"><i class="fa-solid fa-seedling"></i> 장식/수초 생성 (드래그 가능)</div>
      <div class="btn-grid">
        <button class="tool-btn" onclick="addPlant()"><i class="fa-solid fa-seedling"></i> 줄기 수초 추가</button>
        <button class="tool-btn" onclick="addRock()"><i class="fa-solid fa-gem"></i> 자연 수조석</button>
      </div>
    </div>

    <!-- TAB 4: Creatures -->
    <div class="tab-content" id="tab-fish">
      <div class="section-title"><i class="fa-solid fa-fish"></i> 생물 추가</div>
      <div class="btn-grid">
        <button class="tool-btn" onclick="addCreature('neon')"><i class="fa-solid fa-fish"></i> 네온테트라</button>
        <button class="tool-btn" onclick="addCreature('angel')"><i class="fa-solid fa-fish-fins"></i> 엔젤피쉬</button>
        <button class="tool-btn" onclick="addCreature('shrimp')"><i class="fa-solid fa-shrimp"></i> 체리새우</button>
        <button class="tool-btn" onclick="addCreature('turtle')"><i class="fa-solid fa-otter"></i> 거북이</button>
        <button class="tool-btn" onclick="addCreature('crab')"><i class="fa-solid fa-wine-glass"></i> 작은게</button>
        <button class="tool-btn" onclick="addCreature('puffer')"><i class="fa-solid fa-circle"></i> 복어</button>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="action-btn btn-snap" onclick="takeSnapshot()"><i class="fa-solid fa-camera"></i> 캡처</button>
      <button class="action-btn btn-clean" onclick="cleanFood()"><i class="fa-solid fa-broom"></i> 청소</button>
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 리셋</button>
    </div>
  </aside>

  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="status-overlay">
        <div class="status-item"><i class="fa-solid fa-temperature-full"></i> 수온: <span id="disp-temp">24°C</span></div>
        <div class="status-item"><i class="fa-solid fa-droplet"></i> 수질: <span id="disp-water">100% (깨끗함)</span></div>
        <div class="status-item"><i class="fa-solid fa-fish"></i> 개체수: <span id="disp-count">0</span></div>
      </div>

      <div class="inspect-popup" id="inspect-popup">
        <div class="inspect-title" id="inspect-name">생물 정보</div>
        <div id="inspect-details">상태 정보 로딩중...</div>
      </div>

      <canvas id="aquariumCanvas"></canvas>
    </div>

    <div class="tank-banner">
      <i class="fa-solid fa-info-circle"></i>
      <span id="banner-text">먹이 주기 모드입니다. 수조 안을 클릭하면 먹이가 배출됩니다.</span>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');
    const bannerText = document.getElementById('banner-text');
    const inspectPopup = document.getElementById('inspect-popup');

    function resizeCanvas() {
      canvas.width = tankFrame.clientWidth;
      canvas.height = tankFrame.clientHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    /* Global Sandbox States */
    let interactionMode = 'feed';
    let currentGravel = 'gravel';
    let selectedFoodType = 'floating';
    let temperature = 24;
    let waterQuality = 100;
    let customLightColor = '#e0f2fe';
    let lightBrightness = 0.8;

    let equipment = { air: true, filter: true, heater: true };
    let creatures = [];
    let foods = [];
    let bubbles = [];
    let plants = [];
    let rocks = [];

    let draggedObject = null;
    let dragType = null; // 'creature', 'plant', 'rock'
    const GRAVEL_HEIGHT = 45;

    const FOOD_TYPES = {
      floating: { color: '#f59e0b', size: 4, sinkSpeed: 0.8 },
      bottom: { color: '#ea580c', size: 6, sinkSpeed: 1.5 }
    };

    function random(min, max) { return Math.random() * (max - min) + min; }

    /* Creature Class with Ecosystem Attributes */
    class Creature {
      constructor(type, x, y) {
        this.type = type;
        this.x = x || random(60, canvas.width - 60);
        this.y = y || random(100, canvas.height - GRAVEL_HEIGHT - 60);
        this.vx = random(-1.5, 1.5);
        this.vy = random(-0.5, 0.5);
        this.size = 20;
        this.facingRight = this.vx > 0;
        this.isBottomDweller = false;
        this.fullness = 80; // 포만도 (0~100)
        this.age = 1;

        if (type === 'neon') { this.name = '네온테트라'; this.size = 16; }
        else if (type === 'angel') { this.name = '엔젤피쉬'; this.size = 26; }
        else if (type === 'shrimp') { this.name = '체리새우'; this.size = 14; this.isBottomDweller = true; this.y = canvas.height - GRAVEL_HEIGHT - 10; }
        else if (type === 'turtle') { this.name = '거북이'; this.size = 24; }
        else if (type === 'crab') { this.name = '작은게'; this.size = 20; this.isBottomDweller = true; this.y = canvas.height - GRAVEL_HEIGHT - 12; }
        else if (type === 'puffer') { this.name = '복어'; this.size = 20; }
      }

      update() {
        if (draggedObject === this) return;

        // Temperature speed multiplier
        let speedMult = 1.0;
        if (temperature < 20) speedMult = 0.5;
        else if (temperature > 28) speedMult = 1.5;

        // Decrease fullness slowly
        this.fullness = Math.max(0, this.fullness - 0.01);

        const floorY = canvas.height - GRAVEL_HEIGHT - this.size / 2;
        let nearestFood = null;
        let minDist = 250;

        for (let f of foods) {
          let d = Math.hypot(f.x - this.x, f.y - this.y);
          if (d < minDist) { minDist = d; nearestFood = f; }
        }

        if (nearestFood) {
          let dx = nearestFood.x - this.x;
          let dy = nearestFood.y - this.y;
          let angle = Math.atan2(dy, dx);
          let spd = (this.isBottomDweller ? 1.2 : 1.8) * speedMult;

          this.vx = Math.cos(angle) * spd;
          if (!this.isBottomDweller) this.vy = Math.sin(angle) * spd;

          if (minDist < this.size / 2 + 6) {
            let index = foods.indexOf(nearestFood);
            if (index > -1) {
              foods.splice(index, 1);
              this.fullness = Math.min(100, this.fullness + 25);
              for (let i = 0; i < 3; i++) bubbles.push(new Bubble(this.x, this.y, random(2, 4), random(0.5, 1.5)));
            }
          }
        } else {
          if (Math.random() < 0.02) {
            this.vx = random(-1.5, 1.5) * speedMult;
            if (!this.isBottomDweller) this.vy = random(-0.8, 0.8) * speedMult;
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
          ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.5;
          ctx.beginPath(); ctx.moveTo(-this.size + 4, -2); ctx.lineTo(this.size - 4, -2); ctx.stroke();
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.ellipse(-this.size / 2, 2, this.size / 3, 2.5, 0, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'angel') {
          ctx.fillStyle = '#f8fafc';
          ctx.beginPath(); ctx.moveTo(this.size / 2, 0); ctx.lineTo(-this.size / 2, -this.size / 1.5); ctx.lineTo(-this.size / 3, 0); ctx.lineTo(-this.size / 2, this.size / 1.5); ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#334155'; ctx.fillRect(-2, -this.size / 2, 3, this.size);
        } else if (this.type === 'shrimp') {
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.ellipse(0, 0, this.size, this.size / 3, 0, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.ellipse(0, -4, this.size, this.size / 1.4, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(this.size + 2, -2, 5, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'crab') {
          ctx.fillStyle = '#f97316'; ctx.beginPath(); ctx.ellipse(0, 0, this.size, this.size / 1.6, 0, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15'; ctx.beginPath(); ctx.arc(0, 0, this.size, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.arc(6, -4, 3, 0, Math.PI * 2); ctx.fill();
        }

        ctx.restore();
      }
    }

    class Food {
      constructor(x, y, typeKey) {
        this.x = x; this.y = y;
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
          // Pollution system
          waterQuality = Math.max(0, waterQuality - 0.005);
        }
      }
      draw() {
        ctx.save(); ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); ctx.restore();
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
      update() { this.y -= this.speed; this.wobble += 0.05; this.x += Math.sin(this.wobble) * 0.5; }
      draw() {
        ctx.save(); ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)'; ctx.fillStyle = 'rgba(255, 255, 255, 0.15)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.restore();
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
      plants = [{ x: 80, height: 180 }, { x: canvas.width - 120, height: 200 }];
      rocks = [{ x: 200, size: 30 }, { x: canvas.width - 220, size: 38 }];
    }
    initTank();

    /* Tab Switcher */
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }

    function toggleSidebar() {
      document.getElementById('sidebar').classList.toggle('collapsed');
    }

    /* Mouse Interaction Logic */
    canvas.addEventListener('mousedown', (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      if (interactionMode === 'feed') {
        for (let i = 0; i < 3; i++) foods.push(new Food(mx + random(-10, 10), my + random(-10, 10), selectedFoodType));
      } else if (interactionMode === 'drag') {
        // Check creatures first
        for (let c of creatures) {
          if (Math.hypot(c.x - mx, c.y - my) < c.size + 10) {
            draggedObject = c; dragType = 'creature'; return;
          }
        }
        // Check plants
        for (let p of plants) {
          if (Math.abs(p.x - mx) < 25 && my > canvas.height - GRAVEL_HEIGHT - p.height) {
            draggedObject = p; dragType = 'plant'; return;
          }
        }
        // Check rocks
        for (let r of rocks) {
          if (Math.hypot(r.x - mx, (canvas.height - GRAVEL_HEIGHT) - my) < r.size + 15) {
            draggedObject = r; dragType = 'rock'; return;
          }
        }
      } else if (interactionMode === 'inspect') {
        let found = false;
        for (let c of creatures) {
          if (Math.hypot(c.x - mx, c.y - my) < c.size + 15) {
            inspectPopup.style.display = 'block';
            inspectPopup.style.left = (mx + 20) + 'px';
            inspectPopup.style.top = (my - 20) + 'px';
            document.getElementById('inspect-name').innerText = c.name;
            document.getElementById('inspect-details').innerHTML = `
              포만도: ${Math.round(c.fullness)}%<br>
              수온 반응: ${temperature < 20 ? '추위 느끼는 중' : (temperature > 28 ? '더위 느끼는 중' : '쾌적함')}<br>
              위치: X:${Math.round(c.x)}, Y:${Math.round(c.y)}
            `;
            found = true;
            break;
          }
        }
        if (!found) inspectPopup.style.display = 'none';
      } else if (interactionMode === 'delete') {
        for (let i = creatures.length - 1; i >= 0; i--) {
          if (Math.hypot(creatures[i].x - mx, creatures[i].y - my) < creatures[i].size + 10) {
            creatures.splice(i, 1); return;
          }
        }
      }
    });

    canvas.addEventListener('mousemove', (e) => {
      if (draggedObject) {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        if (dragType === 'creature') {
          draggedObject.x = mx;
          draggedObject.y = e.clientY - rect.top;
        } else if (dragType === 'plant' || dragType === 'rock') {
          draggedObject.x = mx;
        }
      }
    });

    window.addEventListener('mouseup', () => { draggedObject = null; dragType = null; });

    function setInteractionMode(mode) {
      interactionMode = mode;
      document.querySelectorAll('#tab-mode .tool-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(`mode-${mode}`).classList.add('active');
      inspectPopup.style.display = 'none';

      if (mode === 'feed') { canvas.style.cursor = 'crosshair'; bannerText.innerText = '먹이 주기 모드입니다. 수조를 클릭하면 먹이가 배출됩니다.'; }
      else if (mode === 'drag') { canvas.style.cursor = 'grab'; bannerText.innerText = '자유 배치 모드입니다. 물고기, 수초, 바위를 마우스로 잡고 이동해 보세요.'; }
      else if (mode === 'inspect') { canvas.style.cursor = 'zoom-in'; bannerText.innerText = '관찰 모드입니다. 생물을 클릭하여 상세 포만도 및 상태를 확인해보세요.'; }
      else if (mode === 'delete') { canvas.style.cursor = 'not-allowed'; bannerText.innerText = '개체 삭제 모드입니다. 지우고 싶은 생물을 클릭하세요.'; }
    }

    function updateTemperature(val) {
      temperature = parseInt(val);
      document.getElementById('temp-val').innerText = val + '°C';
      document.getElementById('disp-temp').innerText = val + '°C';
    }

    function updateLightColor(hex) {
      customLightColor = hex;
      applyLighting();
    }

    function updateLightBrightness(val) {
      lightBrightness = val / 100;
      document.getElementById('light-val').innerText = val + '%';
      applyLighting();
    }

    function applyLighting() {
      tankFrame.style.background = `radial-gradient(circle at center, ${customLightColor} 0%, #05070c 100%)`;
      tankFrame.style.opacity = lightBrightness;
    }

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
      document.getElementById(`btn-${eq}`).classList.toggle('active', equipment[eq]);
    }

    function addPlant() { plants.push({ x: random(60, canvas.width - 60), height: random(150, 220) }); }
    function addRock() { rocks.push({ x: random(60, canvas.width - 60), size: random(25, 40) }); }
    function addCreature(type) { creatures.push(new Creature(type)); }
    function cleanFood() { foods = []; waterQuality = 100; }
    function resetTank() { foods = []; bubbles = []; initTank(); waterQuality = 100; }

    function takeSnapshot() {
      const image = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = image; a.download = 'my_sandbox_aquarium.png';
      a.click();
    }

    function drawGravel() {
      const gHeight = GRAVEL_HEIGHT;
      const yStart = canvas.height - gHeight;

      if (currentGravel === 'gravel') ctx.fillStyle = '#d97706';
      else if (currentGravel === 'volcano') ctx.fillStyle = '#334155';
      else if (currentGravel === 'sand') ctx.fillStyle = '#fde047';
      else if (currentGravel === 'crystal') ctx.fillStyle = '#e0f2fe';

      ctx.fillRect(0, yStart, canvas.width, gHeight);

      for (let r of rocks) {
        ctx.fillStyle = '#475569';
        ctx.beginPath(); ctx.arc(r.x, canvas.height - GRAVEL_HEIGHT + 10, r.size, Math.PI, 0); ctx.fill();
      }
    }

    function drawPlants() {
      ctx.save();
      const plantY = canvas.height - GRAVEL_HEIGHT + 8;
      const time = Date.now() * 0.0025;

      for (let p of plants) {
        const segments = 12;
        const segHeight = p.height / segments;
        let prevX = p.x; let prevY = plantY;

        for (let i = 1; i <= segments; i++) {
          const progress = i / segments;
          const sway = Math.sin(time + progress * 2.2) * (progress * 18);
          const currentX = p.x + sway;
          const currentY = plantY - (i * segHeight);

          ctx.strokeStyle = '#15803d'; ctx.lineWidth = 2.5;
          ctx.beginPath(); ctx.moveTo(prevX, prevY); ctx.lineTo(currentX, currentY); ctx.stroke();

          ctx.save(); ctx.translate(currentX, currentY);
          const leafSize = 8 + (1 - progress) * 4;
          ctx.fillStyle = '#22c55e';
          ctx.beginPath(); ctx.ellipse(-leafSize * 0.8, -2, leafSize, leafSize * 0.45, -0.3, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(leafSize * 0.8, -2, leafSize, leafSize * 0.45, 0.3, 0, Math.PI * 2); ctx.fill();
          ctx.restore();

          prevX = currentX; prevY = currentY;
        }
      }
      ctx.restore();
    }

    function drawEquipmentVisuals() {
      if (equipment.air) {
        ctx.fillStyle = '#64748b'; ctx.fillRect(80, canvas.height - GRAVEL_HEIGHT - 10, 30, 10);
        if (Math.random() < 0.4) bubbles.push(new Bubble(95, canvas.height - GRAVEL_HEIGHT - 10));
      }
      if (equipment.filter) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.35)'; ctx.fillRect(canvas.width - 70, 0, 50, 120);
        ctx.fillStyle = '#0ea5e9'; ctx.fillRect(canvas.width - 65, 110, 40, 8);
        if (waterQuality < 100) waterQuality = Math.min(100, waterQuality + 0.01);
      }
      if (equipment.heater) {
        ctx.fillStyle = '#475569'; ctx.fillRect(30, 40, 10, 180);
        ctx.fillStyle = '#ef4444'; ctx.fillRect(32, 180, 6, 35);
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawGravel();
      drawPlants();
      drawEquipmentVisuals();

      for (let i = bubbles.length - 1; i >= 0; i--) {
        bubbles[i].update(); bubbles[i].draw();
        if (bubbles[i].y < 0) bubbles.splice(i, 1);
      }

      for (let f of foods) { f.update(); f.draw(); }
      for (let c of creatures) { c.update(); c.draw(); }

      document.getElementById('disp-count').innerText = creatures.length;
      document.getElementById('disp-water').innerText = `${Math.round(waterQuality)}% (${waterQuality > 80 ? '깨끗함' : '오염됨'})`;

      requestAnimationFrame(animate);
    }

    applyLighting();
    animate();
  </script>
</body>
</html>
"""

components.html(html_code, height=780, scrolling=False)
