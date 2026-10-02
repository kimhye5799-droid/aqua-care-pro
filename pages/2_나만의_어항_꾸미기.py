import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="파우더 샌드박스 어항 Pro", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파우더 샌드박스 어항 Pro</title>
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

    .sidebar.collapsed { margin-left: -340px; }

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

    /* Main Canvas Container */
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

    /* Info Inspection Box */
    .info-card {
      position: absolute;
      top: 14px;
      right: 14px;
      width: 220px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(8px);
      border: 1px solid #38bdf8;
      border-radius: 12px;
      padding: 12px;
      font-size: 11px;
      z-index: 15;
      display: none;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }

    .info-card h3 { font-size: 13px; color: #38bdf8; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
    .info-line { display: flex; justify-content: space-between; margin-bottom: 4px; color: #cbd5e1; }
    .info-line span.val { color: #f8fafc; font-weight: 600; }

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
      <i class="fa-solid fa-wand-magic-sparkles"></i>
      <h1>파우더 샌드박스 어항 Pro</h1>
    </div>

    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tab-powder')"><i class="fa-solid fa-spray-can"></i>파우더 펜</button>
      <button class="tab-btn" onclick="switchTab('tab-fish')"><i class="fa-solid fa-fish"></i>생물 배치</button>
      <button class="tab-btn" onclick="switchTab('tab-equip')"><i class="fa-solid fa-plug"></i>장비 설정</button>
    </nav>

    <!-- TAB 1: Powder & Pen Mode -->
    <div class="tab-content active" id="tab-powder">
      <div class="section-title"><i class="fa-solid fa-hand-pointer"></i> 특수 도구 펜</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="mode-select" onclick="setInteractionMode('select')"><i class="fa-solid fa-magnifying-glass"></i> 개체 선택펜</button>
        <button class="tool-btn" id="mode-eraser" onclick="setInteractionMode('eraser')"><i class="fa-solid fa-eraser"></i> 삭제펜 (지우개)</button>
        <button class="tool-btn" id="mode-drag" onclick="setInteractionMode('drag')"><i class="fa-solid fa-hand"></i> 개체 이동펜</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-spray-can"></i> 파우더 흩뿌리기</div>
      <div class="btn-grid">
        <button class="tool-btn" id="mode-powder-sand" onclick="setInteractionMode('powder-sand')"><i class="fa-solid fa-mound"></i> 모래 파우더</button>
        <button class="tool-btn" id="mode-powder-gravel" onclick="setInteractionMode('powder-gravel')"><i class="fa-solid fa-cubes"></i> 자갈 파우더</button>
        <button class="tool-btn" id="mode-powder-seed" onclick="setInteractionMode('powder-seed')"><i class="fa-solid fa-seedling"></i> 수초 씨앗</button>
        <button class="tool-btn" id="mode-powder-food" onclick="setInteractionMode('powder-food')"><i class="fa-solid fa-cookie"></i> 먹이 파우더</button>
        <button class="tool-btn" id="mode-powder-bubble" onclick="setInteractionMode('powder-bubble')"><i class="fa-solid fa-soap"></i> 버블 파우더</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-sliders"></i> 수온 & 조명</div>
      <div class="slider-group">
        <div class="slider-header"><span>수온 설정</span><span id="temp-val">24°C</span></div>
        <input type="range" id="temp-slider" min="15" max="35" value="24" oninput="updateTemperature(this.value)">
      </div>
      <div class="color-picker-row">
        <span>조명 색상</span>
        <input type="color" id="light-color" value="#e0f2fe" onchange="updateLightColor(this.value)">
      </div>
    </div>

    <!-- TAB 2: Creatures -->
    <div class="tab-content" id="tab-fish">
      <div class="section-title"><i class="fa-solid fa-fish"></i> 클릭하여 어항에 생성</div>
      <div class="btn-grid">
        <button class="tool-btn" onclick="addCreature('neon')"><i class="fa-solid fa-fish"></i> 네온테트라</button>
        <button class="tool-btn" onclick="addCreature('angel')"><i class="fa-solid fa-fish-fins"></i> 엔젤피쉬</button>
        <button class="tool-btn" onclick="addCreature('shrimp')"><i class="fa-solid fa-shrimp"></i> 체리새우</button>
        <button class="tool-btn" onclick="addCreature('turtle')"><i class="fa-solid fa-otter"></i> 거북이</button>
        <button class="tool-btn" onclick="addCreature('puffer')"><i class="fa-solid fa-circle"></i> 복어</button>
      </div>
    </div>

    <!-- TAB 3: Equipment -->
    <div class="tab-content" id="tab-equip">
      <div class="section-title"><i class="fa-solid fa-plug"></i> 수조 필수 장비</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="eq-thermometer" onclick="toggleEquipment('thermometer')"><i class="fa-solid fa-temperature-full"></i> 온도계 (ON)</button>
        <button class="tool-btn active" id="eq-airstone" onclick="toggleEquipment('airstone')"><i class="fa-solid fa-wind"></i> 산소 기포기 (ON)</button>
        <button class="tool-btn active" id="eq-filter" onclick="toggleEquipment('filter')"><i class="fa-solid fa-filter"></i> 여과기 (ON)</button>
        <button class="tool-btn active" id="eq-heater" onclick="toggleEquipment('heater')"><i class="fa-solid fa-fire"></i> 히터 (ON)</button>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="action-btn btn-snap" onclick="takeSnapshot()"><i class="fa-solid fa-camera"></i> 캡처</button>
      <button class="action-btn btn-clean" onclick="cleanFood()"><i class="fa-solid fa-broom"></i> 청소</button>
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 초기화</button>
    </div>
  </aside>

  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="status-overlay">
        <div class="status-item"><i class="fa-solid fa-temperature-full"></i> 수온: <span id="disp-temp">24°C</span></div>
        <div class="status-item"><i class="fa-solid fa-droplet"></i> 수질: <span id="disp-water">100%</span></div>
        <div class="status-item"><i class="fa-solid fa-fish"></i> 생물수: <span id="disp-count">0</span></div>
      </div>

      <!-- Creature Info Inspector Box -->
      <div class="info-card" id="info-card">
        <h3><i class="fa-solid fa-circle-info"></i> <span id="info-name">네온테트라</span></h3>
        <div class="info-line"><span>종류:</span><span class="val" id="info-type">열대어</span></div>
        <div class="info-line"><span>기분:</span><span class="val" id="info-mood">행복함 😄</span></div>
        <div class="info-line"><span>포만감:</span><span class="val" id="info-hunger">배부름 (85%)</span></div>
        <div class="info-line"><span>수온 적응:</span><span class="val" id="info-temp-status">최적 (24°C)</span></div>
      </div>

      <canvas id="aquariumCanvas"></canvas>
    </div>

    <div class="tank-banner">
      <i class="fa-solid fa-info-circle"></i>
      <span id="banner-text">개체 선택펜: 물고기를 클릭하면 종류와 상태 정보를 상세히 확인합니다.</span>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');
    const bannerText = document.getElementById('banner-text');

    /* Inspector Card Elements */
    const infoCard = document.getElementById('info-card');
    const infoName = document.getElementById('info-name');
    const infoType = document.getElementById('info-type');
    const infoMood = document.getElementById('info-mood');
    const infoHunger = document.getElementById('info-hunger');
    const infoTempStatus = document.getElementById('info-temp-status');

    function resizeCanvas() {
      canvas.width = tankFrame.clientWidth;
      canvas.height = tankFrame.clientHeight;
      if (terrainHeights.length !== canvas.width) {
        terrainHeights = new Array(canvas.width).fill(40);
      }
    }

    let interactionMode = 'select';
    let temperature = 24;
    let waterQuality = 100;
    let customLightColor = '#e0f2fe';

    let equipState = { thermometer: true, airstone: true, filter: true, heater: true };

    let creatures = [];
    let foods = [];
    let bubbles = [];
    let powders = []; // Particles for powder mode
    let terrainHeights = [];
    let plantSeeds = [];

    let draggedCreature = null;
    let selectedCreature = null;
    let isMouseDown = false;

    function random(min, max) { return Math.random() * (max - min) + min; }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    /* Creature Logic & Inspector Data */
    class Creature {
      constructor(type, x, y) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.type = type;
        this.x = x || random(80, canvas.width - 80);
        this.y = y || random(100, canvas.height - 120);
        this.vx = random(-1.5, 1.5);
        this.vy = random(-0.5, 0.5);
        this.size = 22;
        this.facingRight = this.vx > 0;
        this.isBottomDweller = (type === 'shrimp');
        this.hunger = random(60, 90);
        this.tailAngle = 0;

        if (type === 'neon') { this.name = '네온테트라'; this.size = 20; }
        else if (type === 'angel') { this.name = '엔젤피쉬'; this.size = 28; }
        else if (type === 'shrimp') { this.name = '체리새우'; this.size = 18; }
        else if (type === 'turtle') { this.name = '거북이'; this.size = 26; }
        else if (type === 'puffer') { this.name = '복어'; this.size = 24; }
      }

      update() {
        if (this === draggedCreature) return;

        this.tailAngle += 0.15;
        this.hunger = Math.max(0, this.hunger - 0.005);

        let speedMult = (temperature < 20) ? 0.6 : (temperature > 28 ? 1.3 : 1.0);
        let groundY = canvas.height - (terrainHeights[Math.floor(this.x)] || 40) - this.size / 2;

        /* Food Searching */
        let nearestFood = null;
        let minDist = 180;
        for (let f of foods) {
          let d = Math.hypot(f.x - this.x, f.y - this.y);
          if (d < minDist) { minDist = d; nearestFood = f; }
        }

        if (nearestFood) {
          let angle = Math.atan2(nearestFood.y - this.y, nearestFood.x - this.x);
          this.vx = Math.cos(angle) * 2.0 * speedMult;
          if (!this.isBottomDweller) this.vy = Math.sin(angle) * 2.0 * speedMult;

          if (minDist < this.size / 2 + 6) {
            let idx = foods.indexOf(nearestFood);
            if (idx > -1) {
              foods.splice(idx, 1);
              this.hunger = Math.min(100, this.hunger + 25);
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
          this.y = groundY;
          this.vy = 0;
        } else {
          this.y += this.vy;
          if (this.y < 40) { this.y = 40; this.vy *= -1; }
          if (this.y > groundY) { this.y = groundY; this.vy *= -1; }
        }

        if (this.x < 30) { this.x = 30; this.vx *= -1; }
        if (this.x > canvas.width - 30) { this.x = canvas.width - 30; this.vx *= -1; }
        if (Math.abs(this.vx) > 0.1) this.facingRight = this.vx > 0;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        if (selectedCreature === this) {
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2;
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.arc(0, 0, this.size + 12, 0, Math.PI * 2);
          ctx.stroke();
          ctx.setLineDash([]);
        }

        if (!this.facingRight) ctx.scale(-1, 1);
        const tailWag = Math.sin(this.tailAngle) * 4;

        if (this.type === 'neon') {
          ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.ellipse(0, 0, 18, 7, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#00f0ff'; ctx.beginPath(); ctx.fillRect(-12, -3, 20, 2.5); ctx.fill();
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.ellipse(4, 1, 8, 4, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = 'rgba(239, 68, 68, 0.7)';
          ctx.beginPath(); ctx.moveTo(15, 0); ctx.lineTo(24, -6 + tailWag); ctx.lineTo(22, 0); ctx.lineTo(24, 6 + tailWag); ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(-10, -2, 2.5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(-10, -2, 1.2, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'angel') {
          ctx.fillStyle = '#e2e8f0'; ctx.beginPath(); ctx.moveTo(12, 0); ctx.lineTo(-10, -14); ctx.lineTo(-14, 0); ctx.lineTo(-10, 14); ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.fillRect(-4, -12, 3, 24); ctx.fillRect(2, -8, 2.5, 16);
          ctx.fillStyle = '#cbd5e1';
          ctx.beginPath(); ctx.moveTo(-6, -10); ctx.lineTo(-16, -28); ctx.lineTo(-2, -10); ctx.fill();
          ctx.beginPath(); ctx.moveTo(-6, 10); ctx.lineTo(-18, 30); ctx.lineTo(-2, 10); ctx.fill();
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.arc(6, -3, 2.5, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'shrimp') {
          ctx.fillStyle = '#dc2626';
          ctx.beginPath(); ctx.ellipse(-6, -2, 7, 5, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(0, 0, 5, 4, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(5, 2, 4, 3, 0, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = '#fca5a5'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(-11, -3); ctx.lineTo(-22, -10); ctx.stroke();

        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.ellipse(0, -3, 14, 10, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#4ade80'; ctx.beginPath(); ctx.arc(-14, -3, 5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(-15, -4, 1, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15'; ctx.beginPath(); ctx.arc(0, 0, 13, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(-7, -4, 3.5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(-8, -4, 1.8, 0, Math.PI * 2); ctx.fill();
        }

        ctx.restore();
      }
    }

    /* Powder Particles Physics */
    class Powder {
      constructor(x, y, color, type) {
        this.x = x; this.y = y; this.color = color; this.type = type;
        this.vy = random(1.5, 3.5);
        this.vx = random(-0.5, 0.5);
        this.radius = random(2, 3.5);
      }

      update() {
        let groundY = canvas.height - (terrainHeights[Math.floor(this.x)] || 40);
        if (this.y < groundY) {
          this.y += this.vy;
          this.x += this.vx;
        } else {
          if (this.type === 'sand' || this.type === 'gravel') {
            let ix = Math.floor(this.x);
            if (ix >= 0 && ix < canvas.width) {
              terrainHeights[ix] = Math.min(canvas.height - 80, terrainHeights[ix] + 0.8);
            }
            return false; // Remove particle after landing on ground
          } else if (this.type === 'seed') {
            plantSeeds.push({ x: this.x, y: groundY, height: 0, maxH: random(30, 80) });
            return false;
          }
        }
        return true;
      }

      draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    class Food {
      constructor(x, y) { this.x = x; this.y = y; this.radius = 3; }
      update() {
        let groundY = canvas.height - (terrainHeights[Math.floor(this.x)] || 40) - this.radius;
        if (this.y < groundY) { this.y += 1.2; }
      }
      draw() { ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); }
    }

    class Bubble {
      constructor(x, y, radius, speed) {
        this.x = x || random(20, canvas.width - 20);
        this.y = y || canvas.height - 40;
        this.radius = radius || random(2, 4);
        this.speed = speed || random(1, 2);
      }
      update() { this.y -= this.speed; this.x += Math.sin(this.y * 0.05) * 0.4; }
      draw() {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)'; ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      }
    }

    /* Mouse Interaction Handler */
    canvas.addEventListener('mousedown', (e) => {
      isMouseDown = true;
      handleMouseAction(e);
    });

    canvas.addEventListener('mousemove', (e) => {
      if (isMouseDown) handleMouseAction(e);
    });

    window.addEventListener('mouseup', () => {
      isMouseDown = false;
      draggedCreature = null;
    });

    function handleMouseAction(e) {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      if (interactionMode === 'select') {
        let found = false;
        for (let c of creatures) {
          if (Math.hypot(c.x - mx, c.y - my) < c.size + 10) {
            selectedCreature = c;
            showCreatureInfo(c);
            found = true;
            break;
          }
        }
        if (!found) { selectedCreature = null; infoCard.style.display = 'none'; }

      } else if (interactionMode === 'eraser') {
        // Erase particles, plants, foods & decrease sand height
        for (let i = foods.length - 1; i >= 0; i--) {
          if (Math.hypot(foods[i].x - mx, foods[i].y - my) < 20) foods.splice(i, 1);
        }
        for (let i = plantSeeds.length - 1; i >= 0; i--) {
          if (Math.hypot(plantSeeds[i].x - mx, plantSeeds[i].y - my) < 25) plantSeeds.splice(i, 1);
        }
        for (let i = creatures.length - 1; i >= 0; i--) {
          if (Math.hypot(creatures[i].x - mx, creatures[i].y - my) < creatures[i].size + 10) creatures.splice(i, 1);
        }
        for (let x = Math.max(0, Math.floor(mx - 20)); x < Math.min(canvas.width, Math.floor(mx + 20)); x++) {
          terrainHeights[x] = Math.max(10, terrainHeights[x] - 2);
        }

      } else if (interactionMode === 'drag') {
        if (!draggedCreature) {
          for (let c of creatures) {
            if (Math.hypot(c.x - mx, c.y - my) < c.size + 10) { draggedCreature = c; break; }
          }
        } else {
          draggedCreature.x = mx; draggedCreature.y = my;
        }

      } else if (interactionMode.startsWith('powder-')) {
        let type = interactionMode.replace('powder-', '');
        for (let i = 0; i < 4; i++) {
          let px = mx + random(-12, 12);
          let py = my + random(-12, 12);

          if (type === 'sand') powders.push(new Powder(px, py, '#fde047', 'sand'));
          else if (type === 'gravel') powders.push(new Powder(px, py, '#d97706', 'gravel'));
          else if (type === 'seed') powders.push(new Powder(px, py, '#22c55e', 'seed'));
          else if (type === 'food') foods.push(new Food(px, py));
          else if (type === 'bubble') bubbles.push(new Bubble(px, py, random(2, 4), random(1, 2.5)));
        }
      }
    }

    function showCreatureInfo(c) {
      infoCard.style.display = 'block';
      infoName.innerText = c.name;
      infoType.innerText = c.type === 'shrimp' ? '갑각류' : (c.type === 'turtle' ? '파충류' : '열대어');

      let moodText = '행복함 😄';
      if (c.hunger < 30) moodText = '배고픔 😫';
      else if (temperature < 18 || temperature > 30) moodText = '스트레스 😰';
      infoMood.innerText = moodText;

      infoHunger.innerText = `${Math.round(c.hunger)}% (${c.hunger > 60 ? '배부름' : '출출함'})`;

      let tempText = '최적 (24°C)';
      if (temperature < 20) tempText = '추움 ❄️';
      else if (temperature > 28) tempText = '더움 ☀️';
      infoTempStatus.innerText = tempText;
    }

    function addCreature(type) { creatures.push(new Creature(type)); }

    function setInteractionMode(mode) {
      interactionMode = mode;
      document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`mode-${mode}`);
      if (activeBtn) activeBtn.classList.add('active');

      if (mode === 'select') bannerText.innerText = '개체 선택펜: 물고기를 클릭해 상세 종/상태 정보를 조회하세요.';
      else if (mode === 'eraser') bannerText.innerText = '삭제펜: 마우스 영역 내의 지형, 수초, 생물을 삭제합니다.';
      else if (mode === 'drag') bannerText.innerText = '이동펜: 원하는 생물을 마우스로 집어 이동시킵니다.';
      else if (mode.startsWith('powder-')) bannerText.innerText = '파우더 모드: 마우스를 문질러 알갱이 입자를 흩뿌리세요!';
    }

    function toggleEquipment(item) {
      equipState[item] = !equipState[item];
      const btn = document.getElementById(`eq-${item}`);
      btn.classList.toggle('active', equipState[item]);
      const nameMap = { thermometer: '온도계', airstone: '산소 기포기', filter: '여과기', heater: '히터' };
      btn.innerHTML = `<i class="fa-solid fa-plug"></i> ${nameMap[item]} (${equipState[item] ? 'ON' : 'OFF'})`;
    }

    function updateTemperature(val) {
      temperature = parseInt(val);
      document.getElementById('temp-val').innerText = val + '°C';
      document.getElementById('disp-temp').innerText = val + '°C';
      if (selectedCreature) showCreatureInfo(selectedCreature);
    }

    function updateLightColor(hex) {
      customLightColor = hex;
      tankFrame.style.background = `radial-gradient(circle at center, ${customLightColor} 0%, #05070c 100%)`;
    }

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }

    function toggleSidebar() { document.getElementById('sidebar').classList.toggle('collapsed'); }
    function cleanFood() { foods = []; waterQuality = 100; }
    function resetTank() {
      creatures = []; foods = []; powders = []; bubbles = []; plantSeeds = [];
      terrainHeights = new Array(canvas.width).fill(40);
      selectedCreature = null; infoCard.style.display = 'none';
    }

    function takeSnapshot() {
      const img = canvas.toDataURL('image/png');
      const a = document.createElement('a'); a.href = img; a.download = 'powder_aquarium.png'; a.click();
    }

    /* Render Main Loop */
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      /* 1. Draw Sand/Gravel Terrain */
      ctx.fillStyle = '#d97706';
      ctx.beginPath();
      ctx.moveTo(0, canvas.height);
      for (let x = 0; x < canvas.width; x++) {
        ctx.lineTo(x, canvas.height - terrainHeights[x]);
      }
      ctx.lineTo(canvas.width, canvas.height);
      ctx.closePath();
      ctx.fill();

      /* 2. Plant Growth Simulation */
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 3;
      for (let plant of plantSeeds) {
        if (plant.height < plant.maxH) plant.height += 0.1;
        ctx.beginPath();
        ctx.moveTo(plant.x, plant.y);
        ctx.lineTo(plant.x, plant.y - plant.height);
        ctx.stroke();

        ctx.fillStyle = '#15803d';
        ctx.beginPath();
        ctx.arc(plant.x - 3, plant.y - plant.height, 3, 0, Math.PI * 2);
        ctx.arc(plant.x + 3, plant.y - plant.height * 0.7, 3, 0, Math.PI * 2);
        ctx.fill();
      }

      /* 3. Equipments */
      if (equipState.airstone) {
        let airX = canvas.width * 0.5;
        if (Math.random() < 0.5) bubbles.push(new Bubble(airX + random(-10, 10), canvas.height - 40, random(2, 4), random(1.5, 2.5)));
      }

      /* 4. Powders & Particles */
      for (let i = powders.length - 1; i >= 0; i--) {
        if (!powders[i].update()) powders.splice(i, 1);
        else powders[i].draw();
      }

      /* 5. Bubbles & Foods */
      for (let i = bubbles.length - 1; i >= 0; i--) {
        bubbles[i].update(); bubbles[i].draw();
        if (bubbles[i].y < 0) bubbles.splice(i, 1);
      }
      for (let f of foods) { f.update(); f.draw(); }

      /* 6. Creatures */
      for (let c of creatures) { c.update(); c.draw(); }

      /* Update Status */
      document.getElementById('disp-count').innerText = creatures.length;
      document.getElementById('disp-water').innerText = `${Math.round(waterQuality)}%`;

      requestAnimationFrame(animate);
    }

    animate();
  </script>
</body>
</html>
"""

components.html(html_code, height=780, scrolling=False)
