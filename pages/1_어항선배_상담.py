import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="픽셀 파우더 샌드박스 어항 Pro", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>픽셀 파우더 샌드박스 어항 Pro</title>
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

    .aquarium-container {
      flex: 1;
      position: relative;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      padding: 16px;
      gap: 16px;
      background: radial-gradient(circle at center, #151d2a 0%, #05070c 100%);
    }

    .glass-tank-frame {
      position: relative;
      flex: 1;
      height: 86vh;
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 0 20px rgba(255, 255, 255, 0.4);
      border: 4px solid rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(2px);
      overflow: hidden;
    }

    /* 사이드 쓰레기통 UI 스타일 */
    .trash-zone {
      width: 90px;
      height: 86vh;
      background: rgba(30, 41, 59, 0.6);
      border: 2px dashed #475569;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: #94a3b8;
      transition: all 0.2s ease;
      position: relative;
    }

    .trash-zone.drag-over {
      background: rgba(239, 68, 68, 0.2);
      border-color: #ef4444;
      color: #ef4444;
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
    }

    .trash-icon {
      font-size: 32px;
      transition: transform 0.2s ease;
    }

    .trash-zone.drag-over .trash-icon {
      transform: scale(1.2) rotate(-10deg);
    }

    .trash-label {
      font-size: 11px;
      font-weight: 600;
      text-align: center;
      line-height: 1.4;
    }

    .trash-count {
      font-size: 10px;
      background: #334155;
      padding: 2px 8px;
      border-radius: 10px;
      color: #38bdf8;
    }

    canvas {
      width: 100%;
      height: 100%;
      display: block;
      image-rendering: pixelated;
    }

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
      <i class="fa-solid fa-border-all"></i>
      <h1>픽셀 파우더 샌드박스 Pro</h1>
    </div>

    <nav class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tab-powder')"><i class="fa-solid fa-spray-can"></i>픽셀 파우더</button>
      <button class="tab-btn" onclick="switchTab('tab-fish')"><i class="fa-solid fa-fish"></i>생물 배치</button>
      <button class="tab-btn" onclick="switchTab('tab-equip')"><i class="fa-solid fa-plug"></i>장비 설정</button>
    </nav>

    <div class="tab-content active" id="tab-powder">
      <div class="section-title"><i class="fa-solid fa-sliders"></i> 브러시 크기 설정</div>
      <div class="slider-group">
        <div class="slider-header"><span>펜 크기</span><span id="pen-size-val">3 px</span></div>
        <input type="range" id="pen-size-slider" min="1" max="10" value="3" oninput="updatePenSize(this.value)">
      </div>

      <div class="section-title"><i class="fa-solid fa-hand-pointer"></i> 특수 도구 펜</div>
      <div class="btn-grid">
        <button class="tool-btn active" id="mode-select" onclick="setInteractionMode('select')"><i class="fa-solid fa-magnifying-glass"></i> 개체 선택펜</button>
        <button class="tool-btn" id="mode-net" onclick="setInteractionMode('net')"><i class="fa-solid fa-network-wired"></i> 만능 뜰채</button>
        <button class="tool-btn" id="mode-eraser" onclick="setInteractionMode('eraser')"><i class="fa-solid fa-eraser"></i> 픽셀 삭제펜</button>
        <button class="tool-btn" id="mode-drag" onclick="setInteractionMode('drag')"><i class="fa-solid fa-hand"></i> 개체 이동펜</button>
      </div>

      <div class="section-title"><i class="fa-solid fa-border-all"></i> 바닥재 & 구조물</div>
      <div class="btn-grid">
        <button class="tool-btn" id="mode-powder-sand" onclick="setInteractionMode('powder-sand')"><i class="fa-solid fa-square" style="color:#fde047"></i> 금사 모래</button>
        <button class="tool-btn" id="mode-powder-gravel" onclick="setInteractionMode('powder-gravel')"><i class="fa-solid fa-square" style="color:#d97706"></i> 갈색 자갈</button>
        <button class="tool-btn" id="mode-powder-stone" onclick="setInteractionMode('powder-stone')"><i class="fa-solid fa-cubes" style="color:#94a3b8"></i> 고정 암석(돌)</button>
        <button class="tool-btn" id="mode-powder-wood" onclick="setInteractionMode('powder-wood')"><i class="fa-solid fa-tree" style="color:#78350f"></i> 유목(나무)</button>
        <button class="tool-btn" id="mode-powder-seed" onclick="setInteractionMode('powder-seed')"><i class="fa-solid fa-seedling" style="color:#22c55e"></i> 풍성한 수초</button>
        <button class="tool-btn" id="mode-powder-food" onclick="setInteractionMode('powder-food')"><i class="fa-solid fa-cookie" style="color:#f59e0b"></i> 먹이 픽셀</button>
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
      <button class="action-btn btn-reset" onclick="resetTank()"><i class="fa-solid fa-rotate-right"></i> 전체 비우기</button>
    </div>
  </aside>

  <main class="aquarium-container">
    <div class="glass-tank-frame" id="tank-frame">
      <div class="status-overlay">
        <div class="status-item"><i class="fa-solid fa-temperature-full"></i> 수온: <span id="disp-temp">24°C</span></div>
        <div class="status-item"><i class="fa-solid fa-droplet"></i> 수질: <span id="disp-water">100%</span></div>
        <div class="status-item"><i class="fa-solid fa-fish"></i> 생물수: <span id="disp-count">0</span></div>
      </div>

      <div class="info-card" id="info-card">
        <h3><i class="fa-solid fa-circle-info"></i> <span id="info-name">네온테트라</span></h3>
        <div class="info-line"><span>종류:</span><span class="val" id="info-type">열대어</span></div>
        <div class="info-line"><span>기분:</span><span class="val" id="info-mood">행복함 😄</span></div>
        <div class="info-line"><span>포만감:</span><span class="val" id="info-hunger">배부름 (85%)</span></div>
        <div class="info-line"><span>수온 적응:</span><span class="val" id="info-temp-status">최적 (24°C)</span></div>
      </div>

      <canvas id="aquariumCanvas"></canvas>

      <div class="tank-banner">
        <i class="fa-solid fa-info-circle"></i>
        <span id="banner-text">원하는 도구를 선택하고 어항 안에서 자유롭게 표현해 보세요!</span>
      </div>
    </div>

    <!-- 어항 옆에 위치하는 쓰레기통 UI -->
    <div class="trash-zone" id="trash-zone" onclick="emptyNetToTrash()">
      <i class="fa-solid fa-trash-can trash-icon" id="trash-icon"></i>
      <div class="trash-label">뜰채 버리기<br><span style="font-size:9px; color:#64748b; font-weight:400;">(클릭/드래그)</span></div>
      <div class="trash-count" id="net-count-badge">담김: 0</div>
    </div>
  </main>

  <script>
    const canvas = document.getElementById('aquariumCanvas');
    const ctx = canvas.getContext('2d');
    const tankFrame = document.getElementById('tank-frame');
    const bannerText = document.getElementById('banner-text');
    const trashZone = document.getElementById('trash-zone');
    const netBadge = document.getElementById('net-count-badge');

    const infoCard = document.getElementById('info-card');
    const infoName = document.getElementById('info-name');
    const infoType = document.getElementById('info-type');
    const infoMood = document.getElementById('info-mood');
    const infoHunger = document.getElementById('info-hunger');
    const infoTempStatus = document.getElementById('info-temp-status');

    const PIXEL_SIZE = 4;

    let gridCols = 0;
    let gridRows = 0;
    let pixelGrid = [];

    function resizeCanvas() {
      canvas.width = Math.floor(tankFrame.clientWidth);
      canvas.height = Math.floor(tankFrame.clientHeight);
      
      gridCols = Math.floor(canvas.width / PIXEL_SIZE);
      gridRows = Math.floor(canvas.height / PIXEL_SIZE);

      if (pixelGrid.length === 0) {
        pixelGrid = new Array(gridCols * gridRows).fill(null);
      }
    }

    let interactionMode = 'select';
    let penSize = 3;
    let temperature = 24;
    let waterQuality = 100;
    let customLightColor = '#e0f2fe';

    let equipState = { thermometer: true, airstone: true, filter: true, heater: true };

    let creatures = [];
    let foods = [];
    let bubbles = [];
    let plants = [];

    // 뜰채 바구니 보관함
    let netInventory = { creatures: [], foods: [] };

    // 뜰채 모션 관련 상태 변수
    let netCursor = { x: -100, y: -100, isScooping: false, scoopProgress: 0, angle: 0 };

    let draggedCreature = null;
    let selectedCreature = null;
    let isMouseDown = false;

    function random(min, max) { return Math.random() * (max - min) + min; }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    /* 자연스러운 줄기와 잎을 갖춘 수초 클래스 */
    class NaturalPlant {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.maxHeight = random(100, 220);
        this.currentHeight = 5;
        this.stemSegments = [];
        this.leaves = [];
        this.swayOffset = random(0, Math.PI * 2);

        this.generateStructure();
      }

      generateStructure() {
        let currY = 0;
        let currX = 0;
        while (currY < this.maxHeight) {
          currY += random(12, 20);
          currX += random(-4, 4);
          this.stemSegments.push({ x: currX, y: currY });

          if (currY < this.maxHeight - 15) {
            this.leaves.push({
              y: currY,
              side: 1,
              length: random(12, 22)
            });
            this.leaves.push({
              y: currY + random(-3, 3),
              side: -1,
              length: random(12, 22)
            });
          }
        }
      }

      update() {
        if (this.currentHeight < this.maxHeight) {
          this.currentHeight += 0.3;
        }
        this.swayOffset += 0.02;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        let sway = Math.sin(this.swayOffset) * 6;

        ctx.beginPath();
        ctx.moveTo(0, 0);

        let activeSegments = this.stemSegments.filter(s => s.y <= this.currentHeight);
        for (let i = 0; i < activeSegments.length; i++) {
          let seg = activeSegments[i];
          let segSway = (seg.y / this.maxHeight) * sway;
          ctx.lineTo(seg.x + segSway, -seg.y);
        }
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 3.5;
        ctx.lineCap = 'round';
        ctx.stroke();

        for (let leaf of this.leaves) {
          if (leaf.y > this.currentHeight) continue;

          let leafSway = (leaf.y / this.maxHeight) * sway;
          let leafX = (leaf.side * 2) + leafSway;
          let leafY = -leaf.y;

          ctx.save();
          ctx.translate(leafX, leafY);
          ctx.rotate((leaf.side * 0.6) + Math.sin(this.swayOffset + leaf.y) * 0.1);

          ctx.fillStyle = leaf.y % 2 === 0 ? '#22c55e' : '#16a34a';
          ctx.beginPath();
          ctx.ellipse(leaf.side * (leaf.length / 2), 0, leaf.length / 2, 3.5, 0, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();
        }

        ctx.restore();
      }
    }

    function getGridIndex(gx, gy) {
      if (gx < 0 || gx >= gridCols || gy < 0 || gy >= gridRows) return -1;
      return gy * gridCols + gx;
    }

    function getPixel(gx, gy) {
      let idx = getGridIndex(gx, gy);
      return idx !== -1 ? pixelGrid[idx] : 'wall';
    }

    function setPixel(gx, gy, data) {
      let idx = getGridIndex(gx, gy);
      if (idx !== -1) pixelGrid[idx] = data;
    }

    function getSubstrateTopY(x) {
      let gx = Math.floor(x / PIXEL_SIZE);
      for (let gy = 0; gy < gridRows; gy++) {
        let p = getPixel(gx, gy);
        if (p && typeof p === 'object' && p.isSubstrate) {
          return gy * PIXEL_SIZE;
        }
      }
      return canvas.height - 20;
    }

    class Creature {
      constructor(type, x, y) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.type = type;
        this.x = x || random(80, canvas.width - 80);
        this.y = y || random(100, canvas.height - 150);
        this.vx = random(-1.2, 1.2) || 0.8;
        this.vy = random(-0.4, 0.4);
        this.facingRight = this.vx > 0;
        this.hunger = random(50, 80);
        this.tailAngle = random(0, Math.PI * 2);
        this.climbingPlant = null;

        if (type === 'neon') { this.name = '네온테트라'; this.size = 20; }
        else if (type === 'angel') { this.name = '엔젤피쉬'; this.size = 28; }
        else if (type === 'shrimp') { this.name = '체리새우'; this.size = 18; }
        else if (type === 'turtle') { this.name = '거북이'; this.size = 46; }
        else if (type === 'puffer') { this.name = '복어'; this.size = 26; }
      }

      update() {
        if (this === draggedCreature) return;

        this.tailAngle += 0.12;
        this.hunger = Math.max(0, this.hunger - 0.0015);
        let speedMult = (temperature < 20) ? 0.6 : (temperature > 28 ? 1.3 : 1.0);

        if (this.type === 'shrimp') {
          if (!this.climbingPlant && plants.length > 0 && Math.random() < 0.02) {
            for (let p of plants) {
              if (Math.abs(p.x - this.x) < 30 && p.currentHeight > 20) {
                this.climbingPlant = p;
                break;
              }
            }
          }

          if (this.climbingPlant) {
            let p = this.climbingPlant;
            let targetY = p.y - random(10, p.currentHeight);
            this.x += (p.x - this.x) * 0.05;
            this.y += (targetY - this.y) * 0.05;

            if (Math.random() < 0.01 || Math.abs(p.x - this.x) > 60) {
              this.climbingPlant = null;
            }
            return;
          }
        }

        let nearestFood = null;
        if (this.hunger < 85) {
          let minDist = 220;
          for (let f of foods) {
            let d = Math.hypot(f.x - this.x, f.y - this.y);
            if (d < minDist) { minDist = d; nearestFood = f; }
          }
        }

        if (nearestFood) {
          let angle = Math.atan2(nearestFood.y - this.y, nearestFood.x - this.x);
          this.vx = Math.cos(angle) * 1.4 * speedMult;
          this.vy = Math.sin(angle) * 1.4 * speedMult;

          if (Math.hypot(nearestFood.x - this.x, nearestFood.y - this.y) < this.size / 2 + 6) {
            let idx = foods.indexOf(nearestFood);
            if (idx > -1) {
              foods.splice(idx, 1);
              this.hunger = Math.min(100, this.hunger + 30);
              for (let i = 0; i < 3; i++) bubbles.push(new Bubble(this.x, this.y, random(2, 4), random(0.5, 1.5)));
            }
          }
        } else {
          if (Math.random() < 0.02) {
            this.vx = random(-1.2, 1.2) * speedMult;
            this.vy = random(-0.5, 0.5) * speedMult;
          }
        }

        if (Math.abs(this.vx) < 0.2) this.vx = this.facingRight ? 0.6 : -0.6;

        this.x += this.vx;
        this.y += this.vy;

        let groundY = getSubstrateTopY(this.x) - (this.size / 2);

        if (this.y > groundY) {
          this.y = groundY;
          this.vy = -Math.abs(this.vy) - 0.5;
        }

        if (this.y < 45) { this.y = 45; this.vy = Math.abs(this.vy) + 0.2; }
        if (this.x < 30) { this.x = 30; this.vx *= -1; }
        if (this.x > canvas.width - 30) { this.x = canvas.width - 30; this.vx *= -1; }

        if (this.vx > 0.05) this.facingRight = true;
        else if (this.vx < -0.05) this.facingRight = false;
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        if (selectedCreature === this) {
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2;
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.arc(0, 0, this.size + 10, 0, Math.PI * 2);
          ctx.stroke();
          ctx.setLineDash([]);
        }

        if (!this.facingRight) ctx.scale(-1, 1);
        const tailWag = Math.sin(this.tailAngle) * 3;

        if (this.type === 'neon') {
          ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.ellipse(0, 0, 16, 6, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#00f0ff'; ctx.beginPath(); ctx.fillRect(-10, -3, 18, 2); ctx.fill();
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.ellipse(4, 1, 7, 3, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = 'rgba(239, 68, 68, 0.8)';
          ctx.beginPath(); ctx.moveTo(-12, 0); ctx.lineTo(-20, -5 + tailWag); ctx.lineTo(-18, 0); ctx.lineTo(-20, 5 + tailWag); ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(8, -2, 2, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(8, -2, 1, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'angel') {
          ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.moveTo(10, 0); ctx.lineTo(-10, -12); ctx.lineTo(-12, 0); ctx.lineTo(-10, 12); ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.fillRect(-4, -10, 3, 20); ctx.fillRect(2, -6, 2, 12);
          ctx.fillStyle = '#cbd5e1';
          ctx.beginPath(); ctx.moveTo(-6, -8); ctx.lineTo(-16, -26); ctx.lineTo(-2, -8); ctx.fill();
          ctx.beginPath(); ctx.moveTo(-6, 8); ctx.lineTo(-18, 26); ctx.lineTo(-2, 8); ctx.fill();
          ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.arc(5, -2, 2, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'shrimp') {
          ctx.fillStyle = '#dc2626';
          ctx.beginPath(); ctx.ellipse(4, -1, 6, 4, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-2, 0, 5, 3.5, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-7, 1, 4, 3, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-11, 2, 3, 2, 0, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.moveTo(-13, 2); ctx.lineTo(-18, -1 + tailWag); ctx.lineTo(-18, 5 + tailWag); ctx.closePath(); ctx.fill();
          ctx.strokeStyle = '#fca5a5'; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.moveTo(2, 3); ctx.lineTo(0, 8); ctx.moveTo(-1, 3); ctx.lineTo(-4, 8); ctx.moveTo(-4, 3); ctx.lineTo(-7, 8); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(8, -2); ctx.lineTo(18, -8); ctx.moveTo(8, -1); ctx.lineTo(16, -2); ctx.stroke();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(6, -2, 1, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'turtle') {
          ctx.fillStyle = '#15803d'; ctx.beginPath(); ctx.ellipse(-2, 0, 22, 16, 0, 0, Math.PI * 2); ctx.fill();
          ctx.strokeStyle = '#166534'; ctx.lineWidth = 2; ctx.stroke();
          ctx.strokeStyle = '#4ade80'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.rect(-12, -8, 10, 8); ctx.rect(-2, -8, 10, 8); ctx.rect(-7, 0, 10, 8); ctx.stroke();
          ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.ellipse(22, 0, 8, 6, 0, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(24, -2, 1.5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#16a34a';
          ctx.beginPath(); ctx.ellipse(10, -14 + tailWag*0.5, 10, 5, Math.PI/4, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(10, 14 - tailWag*0.5, 10, 5, -Math.PI/4, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-14, -12, 6, 3, Math.PI/6, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.ellipse(-14, 12, 6, 3, -Math.PI/6, 0, Math.PI * 2); ctx.fill();

        } else if (this.type === 'puffer') {
          ctx.fillStyle = '#facc15'; ctx.beginPath(); ctx.arc(0, 0, 13, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#fef08a'; ctx.beginPath(); ctx.arc(0, 4, 10, 0, Math.PI); ctx.fill();
          ctx.strokeStyle = '#ca8a04'; ctx.lineWidth = 1.5;
          for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
            let sx = Math.cos(a) * 13; let sy = Math.sin(a) * 13;
            let ex = Math.cos(a) * 16; let ey = Math.sin(a) * 16;
            ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
          }
          ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(5, -4, 4, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(6, -4, 2, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = '#eab308';
          ctx.beginPath(); ctx.moveTo(-13, 0); ctx.lineTo(-19, -5 + tailWag); ctx.lineTo(-19, 5 + tailWag); ctx.closePath(); ctx.fill();
        }

        ctx.restore();
      }
    }

    class Food {
      constructor(x, y) { this.x = x; this.y = y; }
      update() {
        let groundY = getSubstrateTopY(this.x);
        if (this.y < groundY - 2) this.y += 0.8;
      }
      draw() { ctx.fillStyle = '#f59e0b'; ctx.fillRect(this.x - 2, this.y - 2, 4, 4); }
    }

    class Bubble {
      constructor(x, y, radius, speed) {
        this.x = x || random(20, canvas.width - 20);
        this.y = y || canvas.height - 20;
        this.radius = radius || random(2, 4);
        this.speed = speed || random(1, 2);
      }
      update() { this.y -= this.speed; this.x += Math.sin(this.y * 0.05) * 0.4; }
      draw() {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.strokeRect(Math.floor(this.x), Math.floor(this.y), PIXEL_SIZE, PIXEL_SIZE);
      }
    }

    function updatePixelPhysics() {
      for (let gy = gridRows - 2; gy >= 0; gy--) {
        for (let gx = 0; gx < gridCols; gx++) {
          let current = getPixel(gx, gy);
          if (current && typeof current === 'object' && current.falling) {
            if (!getPixel(gx, gy + 1)) {
              setPixel(gx, gy, null);
              setPixel(gx, gy + 1, current);
            } 
            else if (!getPixel(gx - 1, gy + 1) && Math.random() < 0.5) {
              setPixel(gx, gy, null);
              setPixel(gx - 1, gy + 1, current);
            } 
            else if (!getPixel(gx + 1, gy + 1) && Math.random() < 0.5) {
              setPixel(gx, gy, null);
              setPixel(gx + 1, gy + 1, current);
            }
          }
        }
      }
    }

    /* 뜰채 업데이트 및 렌더링 함수 */
    function drawFishNetCursor() {
      if (interactionMode !== 'net' || netCursor.x < 0) return;

      ctx.save();
      ctx.translate(netCursor.x, netCursor.y);

      // 떠내는 애니메이션 각도 및 회전 처리
      let currentAngle = netCursor.angle;
      if (netCursor.isScooping) {
        netCursor.scoopProgress += 0.12;
        currentAngle += Math.sin(netCursor.scoopProgress) * 0.8;
        if (netCursor.scoopProgress >= Math.PI) {
          netCursor.isScooping = false;
          netCursor.scoopProgress = 0;
        }
      }

      ctx.rotate(currentAngle);

      let netR = penSize * 8 + 12;

      // 1. 손잡이 (그립)
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(40, -40);
      ctx.stroke();

      // 2. 뜰채 프레임
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.ellipse(0, 0, netR, netR * 0.6, 0, 0, Math.PI * 2);
      ctx.stroke();

      // 3. 뜰채 그물망 (격자)
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let i = -netR + 4; i < netR; i += 6) {
        ctx.moveTo(i, -Math.sqrt(Math.max(0, netR*netR - i*i)) * 0.6);
        ctx.lineTo(i, Math.sqrt(Math.max(0, netR*netR - i*i)) * 0.6);
      }
      for (let j = -netR * 0.6 + 4; j < netR * 0.6; j += 4) {
        ctx.moveTo(-Math.sqrt(Math.max(0, (netR*netR)*(1 - (j*j)/(netR*0.6*netR*0.6)))), j);
        ctx.lineTo(Math.sqrt(Math.max(0, (netR*netR)*(1 - (j*j)/(netR*0.6*netR*0.6)))), j);
      }
      ctx.stroke();

      // 4. 뜰채 안에 수집된 개체 수 표시
      let totalCaptured = netInventory.creatures.length + netInventory.foods.length;
      if (totalCaptured > 0) {
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(0, -netR * 0.6 - 6, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(totalCaptured, 0, -netR * 0.6 - 5);
      }

      ctx.restore();
    }

    function updateNetBadge() {
      let count = netInventory.creatures.length + netInventory.foods.length;
      netBadge.innerText = `담김: ${count}`;
      if (count > 0) {
        trashZone.classList.add('drag-over');
      } else {
        trashZone.classList.remove('drag-over');
      }
    }

    function emptyNetToTrash() {
      let count = netInventory.creatures.length + netInventory.foods.length;
      if (count === 0) return;

      netInventory.creatures = [];
      netInventory.foods = [];
      updateNetBadge();

      bannerText.innerText = '뜰채의 모든 내용물을 쓰레기통에 비웠습니다!';
    }

    /* 마우스 이동 및 인터랙션 처리 */
    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      netCursor.x = e.clientX - rect.left;
      netCursor.y = e.clientY - rect.top;

      if (isMouseDown) handleMouseAction(e);
    });

    canvas.addEventListener('mouseleave', () => {
      netCursor.x = -100;
      netCursor.y = -100;
    });

    canvas.addEventListener('mousedown', (e) => {
      isMouseDown = true;
      handleMouseAction(e);
    });

    window.addEventListener('mouseup', () => {
      isMouseDown = false;
      draggedCreature = null;
    });

    function handleMouseAction(e) {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      let gx = Math.floor(mx / PIXEL_SIZE);
      let gy = Math.floor(my / PIXEL_SIZE);

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

      } else if (interactionMode === 'net') {
        // 뜰채 휘두르는 서핑 모션 활성화
        netCursor.isScooping = true;
        netCursor.scoopProgress = 0;

        let netRadius = penSize * 8 + 10;

        // 물고기/생물 떠서 뜰채에 보관
        for (let i = creatures.length - 1; i >= 0; i--) {
          if (Math.hypot(creatures[i].x - mx, creatures[i].y - my) < netRadius) {
            let removed = creatures.splice(i, 1)[0];
            netInventory.creatures.push(removed);
          }
        }
        // 먹이 떠서 뜰채에 보관
        for (let i = foods.length - 1; i >= 0; i--) {
          if (Math.hypot(foods[i].x - mx, foods[i].y - my) < netRadius) {
            let removed = foods.splice(i, 1)[0];
            netInventory.foods.push(removed);
          }
        }
        // 수초 제거
        for (let i = plants.length - 1; i >= 0; i--) {
          if (Math.hypot(plants[i].x - mx, plants[i].y - my) < netRadius) {
            plants.splice(i, 1);
          }
        }
        // 픽셀 지우기
        let pRadius = Math.floor(netRadius / PIXEL_SIZE);
        for (let dy = -pRadius; dy <= pRadius; dy++) {
          for (let dx = -pRadius; dx <= pRadius; dx++) {
            if (Math.hypot(dx, dy) <= pRadius) {
              setPixel(gx + dx, gy + dy, null);
            }
          }
        }

        updateNetBadge();

      } else if (interactionMode === 'eraser') {
        for (let dy = -penSize; dy <= penSize; dy++) {
          for (let dx = -penSize; dx <= penSize; dx++) {
            setPixel(gx + dx, gy + dy, null);
          }
        }
        for (let i = foods.length - 1; i >= 0; i--) {
          if (Math.hypot(foods[i].x - mx, foods[i].y - my) < penSize * 4) foods.splice(i, 1);
        }
        for (let i = creatures.length - 1; i >= 0; i--) {
          if (Math.hypot(creatures[i].x - mx, creatures[i].y - my) < creatures[i].size) creatures.splice(i, 1);
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

        for (let dy = -penSize + 1; dy < penSize; dy++) {
          for (let dx = -penSize + 1; dx < penSize; dx++) {
            let targetGx = gx + dx;
            let targetGy = gy + dy;

            if (type === 'sand') setPixel(targetGx, targetGy, { color: '#fde047', falling: true, isSubstrate: true });
            else if (type === 'gravel') setPixel(targetGx, targetGy, { color: '#d97706', falling: true, isSubstrate: true });
            else if (type === 'stone') setPixel(targetGx, targetGy, { color: '#94a3b8', falling: false, isSubstrate: false });
            else if (type === 'wood') setPixel(targetGx, targetGy, { color: '#78350f', falling: false, isSubstrate: false });
          }
        }

        if (type === 'seed' && Math.random() < 0.15) {
          let groundY = getSubstrateTopY(mx);
          plants.push(new NaturalPlant(mx, groundY));
        } else if (type === 'food' && Math.random() < 0.3) {
          foods.push(new Food(mx + random(-4, 4), my));
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

      infoHunger.innerText = `${Math.round(c.hunger)}% (${c.hunger > 80 ? '배부름' : (c.hunger > 40 ? '보통' : '배고픔')})`;

      let tempText = '최적 (24°C)';
      if (temperature < 20) tempText = '추움 ❄️';
      else if (temperature > 28) tempText = '더움 ☀️';
      infoTempStatus.innerText = tempText;
    }

    function updatePenSize(val) {
      penSize = parseInt(val);
      document.getElementById('pen-size-val').innerText = val + ' px';
    }

    function addCreature(type) { creatures.push(new Creature(type)); }

    function setInteractionMode(mode) {
      interactionMode = mode;
      document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`mode-${mode}`);
      if (activeBtn) activeBtn.classList.add('active');

      if (mode !== 'select') {
        selectedCreature = null;
        infoCard.style.display = 'none';
      }

      if (mode === 'select') bannerText.innerText = '개체 선택펜: 물고기를 클릭해 상태 정보를 조회하세요.';
      else if (mode === 'net') bannerText.innerText = '만능 뜰채: 어항 안을 떠내어 담은 후 우측 쓰레기통을 클릭해 비우세요!';
      else if (mode === 'eraser') bannerText.innerText = '픽셀 삭제펜: 지정 영역의 픽셀과 생물을 지웁니다.';
      else if (mode === 'drag') bannerText.innerText = '개체 이동펜: 원하는 생물을 집어 이동시킵니다.';
      else if (mode === 'powder-stone') bannerText.innerText = '고정 암석: 물고기 뒤쪽 레이어에 배치되는 입체 고정 구조물입니다.';
      else if (mode === 'powder-wood') bannerText.innerText = '유목: 물고기가 통과할 수 있는 통나무 구조물입니다.';
      else if (mode === 'powder-seed') bannerText.innerText = '수초: 풍성한 잎과 곡선 줄기가 오가며 자라는 자연 수초를 생성합니다.';
      else if (mode.startsWith('powder-')) bannerText.innerText = '픽셀 파우더: 입자를 떨어뜨려 바닥재를 채웁니다.';
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
      creatures = []; foods = []; bubbles = []; plants = [];
      pixelGrid = new Array(gridCols * gridRows).fill(null);
      netInventory = { creatures: [], foods: [] };
      updateNetBadge();
      selectedCreature = null; infoCard.style.display = 'none';
    }

    function takeSnapshot() {
      const img = canvas.toDataURL('image/png');
      const a = document.createElement('a'); a.href = img; a.download = 'pixel_aquarium.png'; a.click();
    }

    /* 메인 렌더링 루프 */
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      /* LAYER 1. 픽셀 바닥재/암석/유목 */
      updatePixelPhysics();

      for (let gy = 0; gy < gridRows; gy++) {
        for (let gx = 0; gx < gridCols; gx++) {
          let cell = getPixel(gx, gy);
          if (cell && typeof cell === 'object') {
            ctx.fillStyle = cell.color;
            ctx.fillRect(gx * PIXEL_SIZE, gy * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE);
          }
        }
      }

      /* LAYER 2. 자연 수초 */
      for (let plant of plants) {
        plant.update();
        plant.draw();
      }

      /* LAYER 3. 기포기 bubble 및 먹이 */
      if (equipState.airstone) {
        let airX = canvas.width * 0.5;
        if (Math.random() < 0.5) bubbles.push(new Bubble(airX + random(-10, 10), canvas.height - 20, random(2, 4), random(1.5, 2.5)));
      }

      for (let i = bubbles.length - 1; i >= 0; i--) {
        bubbles[i].update(); bubbles[i].draw();
        if (bubbles[i].y < 0) bubbles.splice(i, 1);
      }
      for (let f of foods) { f.update(); f.draw(); }

      /* LAYER 4. 생물 렌더링 */
      for (let c of creatures) {
        c.update();
        c.draw();
      }

      /* LAYER 5. 커스텀 뜰채 오버레이 렌더링 */
      drawFishNetCursor();

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
