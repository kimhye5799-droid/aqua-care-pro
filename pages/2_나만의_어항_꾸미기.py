import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="울트라 샌드박스 어항 Pro", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>울트라 샌드박스 어항 Pro</title>
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

    .drag-item {
      cursor: grab;
      border: 1px dashed #38bdf8;
      background: rgba(56, 189, 248, 0.1);
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

    .ghost-preview {
      position: fixed;
      pointer-events: none;
      z-index: 1000;
      opacity: 0.75;
      font-size: 28px;
      color: #38bdf8;
      display: none;
      transform: translate(-50%, -50%);
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

  <!-- Ghost Drag Preview -->
  <div class="ghost-preview" id="ghost-preview"><i class="fa-solid fa-fish"></i></div>

  <aside class="sidebar" id="sidebar">
    <button class="sidebar-toggle-btn" onclick="toggleSidebar()"><i class="fa-solid fa-bars"></i></button>

    <div class="sidebar-header">
      <i class="fa-solid fa-fish-fins"></i>
      <h1>울트라 샌드박스 어항 Pro</h1>
    </div>

    <!-- Tab Bar Navigation -->
    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tab-mode')"><i class="fa-solid fa-hand-pointer"></i>모드</button>
      <button class="tab-btn" onclick="switchTab('tab-decor')"><i class="fa-solid fa-paintbrush"></i>꾸미기</button>
      <button class="tab-btn" onclick="switchTab('tab-equip')"><i class="fa-solid fa-plug"></i>장비</button>
      <button class="tab-btn" onclick="switchTab('tab-fish')"><i class="fa-solid fa-fish"></i>생물</button>
    </nav>

    <!-- TAB 1: Interactivity Mode -->
    <div class="tab-content active" id="tab-mode">
      <div class="section-title"><i class="fa-solid fa-hand-pointer"></i> 상호작용 도구</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="mode-feed" onclick="setInteractionMode('feed')"><i class="fa-solid fa-cookie"></i> 먹이 흩뿌리기</button>
        <button class="tool-btn" id="mode-drag" onclick="setInteractionMode('drag')"><i class="fa-solid fa-up-down-left-right"></i> 생물 잡고 이동</button>
        <button class="tool-btn" id="mode-delete" onclick="setInteractionMode('delete')"><i class="fa-solid fa-eraser"></i> 개체 삭제</button>
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

    <!-- TAB 2: Sandbox Drawing & Decoration -->
    <div class="tab-content" id="tab-decor">
      <div class="section-title"><i class="fa-solid fa-paintbrush"></i> 직접 그리기 모드</div>
      <div class="btn-grid">
        <button class="tool-btn" id="mode-draw-plant" onclick="setInteractionMode('draw-plant')"><i class="fa-solid fa-seedling"></i> 수초 그리기</button>
        <button class="tool-btn" id="mode-draw-sand" onclick="setInteractionMode('draw-sand')"><i class="fa-solid fa-mound"></i> 모래/지형 쌓기</button>
        <button class="tool-btn" id="mode-add-wood" onclick="setInteractionMode('add-wood')"><i class="fa-solid fa-tree"></i> 나무/유목 배치</button>
        <button class="tool-btn" id="mode-add-rock" onclick="setInteractionMode('add-rock')"><i class="fa-solid fa-gem"></i> 바위/돌 배치</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-mountain-sun"></i> 바닥 재질</div>
      <div class="btn-grid">
        <button class="tool-btn active" onclick="setGravel('gravel', this)"><i class="fa-solid fa-cubes"></i> 자연 자갈</button>
        <button class="tool-btn" onclick="setGravel('volcano', this)"><i class="fa-solid fa-volcano"></i> 화산석</button>
        <button class="tool-btn" onclick="setGravel('sand', this)"><i class="fa-solid fa-grip-lines-vertical"></i> 금사 모래</button>
        <button class="tool-btn" onclick="setGravel('crystal', this)"><i class="fa-solid fa-gem"></i> 크리스탈</button>
      </div>
    </div>

    <!-- TAB 3: Aquarium Equipment -->
    <div class="tab-content" id="tab-equip">
      <div class="section-title"><i class="fa-solid fa-plug"></i> 어항 필수 장비 On/Off</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="eq-thermometer" onclick="toggleEquipment('thermometer')"><i class="fa-solid fa-temperature-full"></i> 수온계 (ON)</button>
        <button class="tool-btn active" id="eq-airstone" onclick="toggleEquipment('airstone')"><i class="fa-solid fa-wind"></i> 산소 기포기 (ON)</button>
        <button class="tool-btn active" id="eq-filter" onclick="toggleEquipment('filter')"><i class="fa-solid fa-filter"></i> 스펀지 여과기 (ON)</button>
        <button class="tool-btn active" id="eq-heater" onclick="toggleEquipment('heater')"><i class="fa-solid fa-fire"></i> 수중 히터 (ON)</button>
      </div>
    </div>

    <!-- TAB 4: Creatures -->
    <div class="tab-content" id="tab-fish">
      <div class="section-title"><i class="fa-solid fa-fish"></i> 생물 추가 (끌어서 드롭)</div>
      <div class="btn-grid">
        <div class="tool-btn drag-item" onmousedown="startSidebarDrag(event, 'neon', 'fa-fish')"><i class="fa-solid fa-fish"></i> 네온테트라</div>
        <div class="tool-btn drag-item" onmousedown="startSidebarDrag(event, 'angel', 'fa-fish-fins')"><i class="fa-solid fa-fish-fins"></i> 엔젤피쉬</div>
        <div class="tool-btn drag-item" onmousedown="startSidebarDrag(event, 'shrimp', 'fa-shrimp')"><i class="fa-solid fa-shrimp"></i> 체리새우</div>
        <div class="tool-btn drag-item" onmousedown="startSidebarDrag(event, 'turtle', 'fa-otter')"><i class="fa-solid fa-otter"></i> 거북이</div>
        <div class="tool-btn drag-item" onmousedown="startSidebarDrag(event, 'puffer', 'fa-circle')"><i class="fa-solid fa-circle"></i> 복어</div>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="action-btn btn-snap" onclick="takeSnapshot()"><i class="fa-solid fa-camera"></i> 캡처</button>
      <button class="action-btn btn-clean" onclick="cleanFood()"><i class="fa-solid fa-broom"></i> 청소</button>
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 어항 비우기</button>
    </div>
  </aside>

  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="status-overlay">
        <div class="status-item"><i class="fa-solid fa-temperature-full"></i> 수온: <span id="disp-temp">24°C</span></div>
        <div class="status-item"><i class="fa-solid fa-droplet"></i> 수질: <span id="disp-water">100% (깨끗함)</span></div>
        <div class="status-item"><i class="fa-solid fa-fish"></i> 개체수: <span id="disp-count">0</span></div>
      </div>

      <canvas id="aquariumCanvas"></canvas>
    </div>

    <div class="tank-banner">
      <i class="fa-solid fa-info-circle"></i>
      <span id="banner-text">초기 상태는 비어있습니다. 생물과 꾸미기 도구를 이용하여 나만의 수조를 완성해보세요!</span>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');
    const bannerText = document.getElementById('banner-text');
    const ghostPreview = document.getElementById('ghost-preview');

    function resizeCanvas() {
      canvas.width = tankFrame.clientWidth;
      canvas.height = tankFrame.clientHeight;
      initTerrain();
    }

    /* Global States */
    let interactionMode = 'feed';
    let currentGravel = 'gravel';
    let temperature = 24;
    let waterQuality = 100;
    let customLightColor = '#e0f2fe';

    /* Equipments State */
    let equipState = {
      thermometer: true,
      airstone: true,
      filter: true,
      heater: true
    };

    /* Empty Initial Collections */
    let creatures = [];
    let foods = [];
    let bubbles = [];
    let customPlants = []; // drawn plant stems/leaves
    let terrainHeights = []; // sand height map
    let woods = [];
    let rocks = [];

    let draggedCreature = null;
    let isMouseDown = false;
    let lastMouseX = 0, lastMouseY = 0;
    let sidebarDraggingType = null;

    const BASE_GRAVEL_HEIGHT = 45;

    function initTerrain() {
      if (terrainHeights.length !== canvas.width) {
        terrainHeights = new Array(canvas.width).fill(BASE_GRAVEL_HEIGHT);
      }
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function random(min, max) { return Math.random() * (max - min) + min; }

    /* Creature Graphics */
    class Creature {
      constructor(type, x, y) {
        this.type = type;
        this.x = x || random(60, canvas.width - 60);
        this.y = y || random(100, canvas.height - BASE_GRAVEL_HEIGHT - 60);
        this.vx = random(-1.5, 1.5);
        this.vy = random(-0.5, 0.5);
        this.size = 22;
        this.facingRight = this.vx > 0;
        this.isBottomDweller = false;
        this.isGrabbed = false;
        this.tailAngle = 0;

        if (type === 'neon') { this.size = 20; }
        else if (type === 'angel') { this.size = 28; }
        else if (type === 'shrimp') { this.size = 18; this.isBottomDweller = true; }
        else if (type === 'turtle') { this.size = 26; }
        else if (type === 'puffer') { this.size = 24; }
      }

      update() {
        if (this.isGrabbed) return;

        this.tailAngle += 0.15;
        let speedMult = (temperature < 20) ? 0.5 : (temperature > 28 ? 1.4 : 1.0);
        
        let groundY = canvas.height - (terrainHeights[Math.floor(this.x)] || BASE_GRAVEL_HEIGHT) - this.size / 2;

        let nearestFood = null;
        let minDist = 200;

        for (let f of foods) {
          let d = Math.hypot(f.x - this.x, f.y - this.y);
          if (d < minDist) { minDist = d; nearestFood = f; }
        }

        if (nearestFood) {
          let angle = Math.atan2(nearestFood.y - this.y, nearestFood.x - this.x);
          let spd = 2.0 * speedMult;
          this.vx = Math.cos(angle) * spd;
          if (!this.isBottomDweller) this.vy = Math.sin(angle) * spd;

          if (minDist < this.size / 2 + 6) {
            let index = foods.indexOf(nearestFood);
            if (index > -1) {
              foods.splice(index, 1);
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

        if (this.isGrabbed) {
          ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(0, 0, this.size + 10, 0, Math.PI * 2); ctx.stroke();
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
          ctx.beginPath(); ctx.ellipse(9, 4, 3, 2.5, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.moveTo(11, 4); ctx.lineTo(16, 2); ctx.lineTo(16, 7); ctx.closePath(); ctx.fill();
          ctx.strokeStyle = '#fca5a5'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(-11, -3); ctx.lineTo(-22, -10); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(-11, -1); ctx.lineTo(-20, -4); ctx.stroke();
          ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 1.2;
          for(let i=0; i<4; i++) {
            ctx.beginPath(); ctx.moveTo(-6 + i*3, 2); ctx.lineTo(-8 + i*3, 8); ctx.stroke();
          }

        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.ellipse(0, -3, 14, 10, 0, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = '#166534'; ctx.lineWidth = 1.5; ctx.stroke();
          ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(-2, -3, 3, 0, Math.PI*2); ctx.arc(4, -3, 3, 0, Math.PI*2); ctx.fill();
          ctx.fillStyle = '#4ade80'; ctx.beginPath(); ctx.arc(-14, -3, 5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(-15, -4, 1, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-10, 5, 5, 2.5, 0.4, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(8, 5, 4, 2, -0.4, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15'; ctx.beginPath(); ctx.arc(0, 0, 13, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.arc(2, 3, 9, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#ca8a04';
          ctx.beginPath(); ctx.arc(-4, -5, 1.2, 0, Math.PI*2); ctx.arc(2, -6, 1.2, 0, Math.PI*2); ctx.fill();
          ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(-7, -4, 3.5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(-8, -4, 1.8, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#eab308';
          ctx.beginPath(); ctx.moveTo(12, 0); ctx.lineTo(18, -4 + tailWag); ctx.lineTo(18, 4 + tailWag); ctx.closePath(); ctx.fill();
        }

        ctx.restore();
      }
    }

    class Food {
      constructor(x, y) { this.x = x; this.y = y; this.radius = 3.5; }
      update() {
        const groundY = canvas.height - (terrainHeights[Math.floor(this.x)] || BASE_GRAVEL_HEIGHT) - this.radius;
        if (this.y < groundY) { this.y += 1.2; this.x += Math.sin(this.y * 0.05) * 0.3; }
        else { this.y = groundY; waterQuality = Math.max(0, waterQuality - 0.003); }
      }
      draw() {
        ctx.save(); ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      }
    }

    class Bubble {
      constructor(x, y, radius, speed) {
        this.x = x || random(20, canvas.width - 20);
        this.y = y || canvas.height - 40;
        this.radius = radius || random(2, 4.5);
        this.speed = speed || random(1, 2.2);
        this.wobble = random(0, Math.PI * 2);
      }
      update() { this.y -= this.speed; this.wobble += 0.05; this.x += Math.sin(this.wobble) * 0.5; }
      draw() {
        ctx.save(); ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)'; ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.restore();
      }
    }

    /* Sidebar Drag Drop Creature */
    function startSidebarDrag(e, type, iconClass) {
      sidebarDraggingType = type;
      ghostPreview.innerHTML = `<i class="fa-solid ${iconClass}"></i>`;
      ghostPreview.style.display = 'block';
      ghostPreview.style.left = e.clientX + 'px';
      ghostPreview.style.top = e.clientY + 'px';
    }

    window.addEventListener('mousemove', (e) => {
      if (sidebarDraggingType) {
        ghostPreview.style.left = e.clientX + 'px';
        ghostPreview.style.top = e.clientY + 'px';
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (sidebarDraggingType) {
        const rect = canvas.getBoundingClientRect();
        if (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom) {
          creatures.push(new Creature(sidebarDraggingType, e.clientX - rect.left, e.clientY - rect.top));
        }
        sidebarDraggingType = null;
        ghostPreview.style.display = 'none';
      }
    });

    /* Interactive Drawing & Actions on Canvas */
    let currentPlantPath = null;

    canvas.addEventListener('mousedown', (e) => {
      isMouseDown = true;
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      if (interactionMode === 'feed') {
        foods.push(new Food(mx, my));
      } else if (interactionMode === 'drag') {
        for (let c of creatures) {
          if (Math.hypot(c.x - mx, c.y - my) < c.size + 15) {
            draggedCreature = c; c.isGrabbed = true; break;
          }
        }
      } else if (interactionMode === 'draw-plant') {
        currentPlantPath = [{ x: mx, y: my }];
        customPlants.push(currentPlantPath);
      } else if (interactionMode === 'draw-sand') {
        addSandAt(mx, 15);
      } else if (interactionMode === 'add-wood') {
        woods.push({ x: mx, y: canvas.height - (terrainHeights[Math.floor(mx)] || BASE_GRAVEL_HEIGHT), size: random(40, 70) });
      } else if (interactionMode === 'add-rock') {
        rocks.push({ x: mx, y: canvas.height - (terrainHeights[Math.floor(mx)] || BASE_GRAVEL_HEIGHT), size: random(25, 45) });
      } else if (interactionMode === 'delete') {
        for (let i = creatures.length - 1; i >= 0; i--) {
          if (Math.hypot(creatures[i].x - mx, creatures[i].y - my) < creatures[i].size + 10) {
            creatures.splice(i, 1); return;
          }
        }
      }
    });

    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = Math.floor(e.clientX - rect.left);
      const my = Math.floor(e.clientY - rect.top);

      if (isMouseDown) {
        if (interactionMode === 'feed' && Math.random() < 0.25) {
          foods.push(new Food(mx + random(-10, 10), my));
        } else if (interactionMode === 'drag' && draggedCreature) {
          draggedCreature.x = mx; draggedCreature.y = my;
        } else if (interactionMode === 'draw-plant' && currentPlantPath) {
          currentPlantPath.push({ x: mx, y: my });
        } else if (interactionMode === 'draw-sand') {
          addSandAt(mx, 8);
        }
      }
    });

    canvas.addEventListener('mouseup', () => {
      isMouseDown = false;
      if (draggedCreature) { draggedCreature.isGrabbed = false; draggedCreature = null; }
      currentPlantPath = null;
    });

    function addSandAt(x, amount) {
      for (let i = Math.max(0, x - 25); i < Math.min(canvas.width, x + 25); i++) {
        let dist = Math.abs(i - x);
        terrainHeights[i] = Math.min(canvas.height - 100, terrainHeights[i] + Math.max(0, amount - dist * 0.3));
      }
    }

    function setInteractionMode(mode) {
      interactionMode = mode;
      document.querySelectorAll('#tab-mode .tool-btn, #tab-decor .tool-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`mode-${mode}`);
      if (activeBtn) activeBtn.classList.add('active');

      if (mode === 'feed') bannerText.innerText = '먹이 모드: 마우스를 눌러 먹이를 퍼뜨려주세요.';
      else if (mode === 'drag') bannerText.innerText = '이동 모드: 물고기/생물을 붙잡고 드래그해 이동하세요.';
      else if (mode === 'draw-plant') bannerText.innerText = '수초 그리기 모드: 마우스를 누른 채 위로 그리면 수초가 생성됩니다.';
      else if (mode === 'draw-sand') bannerText.innerText = '모래 쌓기 모드: 어항 바닥을 문질러 언덕과 모래 지형을 만드세요.';
      else if (mode === 'add-wood') bannerText.innerText = '유목 배치 모드: 클릭한 위치에 나무 유목을 만듭니다.';
      else if (mode === 'add-rock') bannerText.innerText = '바위 배치 모드: 클릭한 위치에 수조석을 배치합니다.';
    }

    function toggleEquipment(item) {
      equipState[item] = !equipState[item];
      const btn = document.getElementById(`eq-${item}`);
      btn.classList.toggle('active', equipState[item]);
      const nameMap = { thermometer: '수온계', airstone: '산소 기포기', filter: '스펀지 여과기', heater: '수중 히터' };
      btn.innerHTML = `<i class="fa-solid fa-plug"></i> ${nameMap[item]} (${equipState[item] ? 'ON' : 'OFF'})`;
    }

    function updateTemperature(val) {
      temperature = parseInt(val);
      document.getElementById('temp-val').innerText = val + '°C';
      document.getElementById('disp-temp').innerText = val + '°C';
    }

    function updateLightColor(hex) { customLightColor = hex; tankFrame.style.background = `radial-gradient(circle at center, ${customLightColor} 0%, #05070c 100%)`; }

    function setGravel(type, btn) {
      currentGravel = type;
      btn.parentElement.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
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
      foods = []; bubbles = []; creatures = []; customPlants = []; woods = []; rocks = [];
      terrainHeights = new Array(canvas.width).fill(BASE_GRAVEL_HEIGHT);
      waterQuality = 100;
    }

    function takeSnapshot() {
      const image = canvas.toDataURL('image/png');
      const a = document.createElement('a'); a.href = image; a.download = 'aquarium_sandbox.png'; a.click();
    }

    /* Drawing Functions */
    function drawTerrain() {
      if (currentGravel === 'gravel') ctx.fillStyle = '#d97706';
      else if (currentGravel === 'volcano') ctx.fillStyle = '#334155';
      else if (currentGravel === 'sand') ctx.fillStyle = '#fde047';
      else if (currentGravel === 'crystal') ctx.fillStyle = '#e0f2fe';

      ctx.beginPath();
      ctx.moveTo(0, canvas.height);
      for (let x = 0; x < canvas.width; x++) {
        ctx.lineTo(x, canvas.height - terrainHeights[x]);
      }
      ctx.lineTo(canvas.width, canvas.height);
      ctx.closePath();
      ctx.fill();
    }

    function drawCustomPlants() {
      ctx.save();
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 3.5;
      ctx.lineCap = 'round';

      for (let path of customPlants) {
        if (path.length < 2) continue;
        ctx.beginPath();
        ctx.moveTo(path[0].x, path[0].y);
        for (let i = 1; i < path.length; i++) {
          ctx.lineTo(path[i].x, path[i].y);
        }
        ctx.stroke();

        // Leaf details
        ctx.fillStyle = '#15803d';
        for (let i = 0; i < path.length; i += 4) {
          ctx.beginPath();
          ctx.arc(path[i].x, path[i].y, 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      ctx.restore();
    }

    function drawWoodsAndRocks() {
      for (let r of rocks) {
        ctx.fillStyle = '#475569'; ctx.beginPath();
        ctx.arc(r.x, r.y - r.size / 2, r.size, Math.PI, 0); ctx.fill();
      }

      for (let w of woods) {
        ctx.strokeStyle = '#78350f'; ctx.lineWidth = 10; ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(w.x, w.y);
        ctx.lineTo(w.x + w.size * 0.6, w.y - w.size);
        ctx.lineTo(w.x + w.size, w.y - w.size * 0.4);
        ctx.stroke();
      }
    }

    /* Equipment Drawing */
    function drawEquipments() {
      // 1. Digital Thermometer (Left Glass)
      if (equipState.thermometer) {
        ctx.fillStyle = '#1e293b'; ctx.fillRect(15, 60, 24, 90);
        ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.strokeRect(15, 60, 24, 90);
        ctx.fillStyle = '#ef4444'; ctx.fillRect(24, 80, 6, 50);
        ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 10px sans-serif';
        ctx.fillText(`${temperature}°C`, 13, 165);
      }

      // 2. Air Stone & Bubbles (Bottom Middle)
      if (equipState.airstone) {
        const airX = canvas.width * 0.5;
        const airY = canvas.height - (terrainHeights[Math.floor(airX)] || BASE_GRAVEL_HEIGHT) - 8;
        ctx.fillStyle = '#64748b'; ctx.fillRect(airX - 15, airY, 30, 8);

        if (Math.random() < 0.6) {
          bubbles.push(new Bubble(airX + random(-10, 10), airY, random(2, 4), random(1.5, 3.0)));
        }
      }

      // 3. Sponge Filter (Right Back)
      if (equipState.filter) {
        const fx = canvas.width - 45;
        const fy = canvas.height - (terrainHeights[Math.floor(fx)] || BASE_GRAVEL_HEIGHT) - 70;
        ctx.fillStyle = '#0f172a'; ctx.fillRect(fx - 12, fy, 24, 60); // Sponge
        ctx.fillStyle = '#94a3b8'; ctx.fillRect(fx - 3, fy - 40, 6, 40); // Tube
        if (Math.random() < 0.4) bubbles.push(new Bubble(fx, fy - 40, 3, 2));
      }

      // 4. Heater (Left Back)
      if (equipState.heater) {
        const hx = 55;
        ctx.fillStyle = '#334155'; ctx.fillRect(hx, 50, 8, 120);
        ctx.fillStyle = (temperature > 26) ? '#ef4444' : '#10b981'; ctx.beginPath(); ctx.arc(hx + 4, 160, 5, 0, Math.PI * 2); ctx.fill();
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawTerrain();
      drawWoodsAndRocks();
      drawCustomPlants();
      drawEquipments();

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

    animate();
  </script>
</body>
</html>
"""

components.html(html_code, height=780, scrolling=False)
