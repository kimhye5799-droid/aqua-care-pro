import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="픽셀 파우더 어항 Sandbox", layout="wide")

html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body { background-color: #060c18; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; height: 100vh; overflow: hidden; }
  
  #sidebar { width: 300px; background-color: #0f192e; padding: 12px; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; border-right: 1px solid #1e2e4a; }
  .panel-title { font-size: 13px; font-weight: bold; color: #38bdf8; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; }
  
  .mode-btn-group { display: flex; gap: 4px; }
  .mode-btn { flex: 1; padding: 8px 4px; background-color: #182642; border: 1px solid #24385e; color: #94a3b8; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: bold; }
  .mode-btn.active { background-color: #0284c7; color: #ffffff; border-color: #38bdf8; box-shadow: 0 0 8px rgba(56, 189, 248, 0.4); }
  
  .tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; }
  .tool-btn { padding: 7px 6px; background-color: #182642; border: 1px solid #24385e; color: #e2e8f0; border-radius: 6px; cursor: pointer; font-size: 11px; text-align: left; display: flex; align-items: center; gap: 4px; }
  .tool-btn.active { border-color: #38bdf8; background-color: #1e3a8a; color: #38bdf8; font-weight: bold; box-shadow: 0 0 6px rgba(56,189,248,0.3); }
  
  .box-card { background: #182642; padding: 8px; border-radius: 6px; border: 1px solid #24385e; display: flex; flex-direction: column; gap: 5px; }
  .slider-label { font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; }
  input[type="range"], input[type="color"] { width: 100%; accent-color: #38bdf8; cursor: pointer; }
  input[type="color"] { height: 24px; border: none; background: transparent; }

  #main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: #020611; padding: 10px; }
  canvas { border: 3px solid #0284c7; border-radius: 12px; cursor: crosshair; box-shadow: 0 0 35px rgba(2, 132, 199, 0.35); background: #000; }
  
  #status-bar { position: absolute; top: 18px; left: 50%; transform: translateX(-50%); background: rgba(15, 25, 46, 0.95); padding: 6px 18px; border-radius: 20px; border: 1px solid #38bdf8; display: flex; gap: 15px; font-size: 12px; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
  
  #info-box { position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%); background: rgba(15, 25, 46, 0.95); padding: 10px 20px; border-radius: 10px; border: 1px solid #38bdf8; font-size: 12px; display: none; gap: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }

  #right-panel { width: 110px; background-color: #0f192e; padding: 12px 8px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; border-left: 1px solid #1e2e4a; }
  .trash-box { width: 100%; height: 110px; border: 2px dashed #ef4444; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #ef4444; font-size: 11px; gap: 6px; cursor: pointer; }
  .trash-box:hover { background: rgba(239, 68, 68, 0.15); }
  
  .act-btn { padding: 8px; border: none; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; color: white; width: 100%; }
  .btn-reset { background: #ef4444; }
  .btn-clean { background: #0284c7; }
</style>
</head>
<body>

<div id="sidebar">
  <div>
    <div class="panel-title">🌊 서식 환경 (담수 / 해수)</div>
    <div class="mode-btn-group">
      <button class="mode-btn active" id="btn-fresh" onclick="setTankEnv('FRESH')">🌿 담수 어항</button>
      <button class="mode-btn" id="btn-salt" onclick="setTankEnv('SALT')">🪸 해수 어항</button>
    </div>
  </div>

  <div>
    <div class="panel-title">🛠️ 도구 모드</div>
    <div class="mode-btn-group">
      <button class="mode-btn active" id="tab-powder" onclick="setCategory('POWDER')">파우더</button>
      <button class="mode-btn" id="tab-creature" onclick="setCategory('CREATURE')">생물</button>
      <button class="mode-btn" id="tab-equip" onclick="setCategory('EQUIP')">장비</button>
    </div>
  </div>

  <div class="box-card">
    <div class="slider-label"><span>🖌️ 브러시 크기</span><span id="brush-val">4 px</span></div>
    <input type="range" id="brush-size" min="1" max="10" value="4" oninput="brushSize=parseInt(this.value); document.getElementById('brush-val').innerText=this.value+' px';">
  </div>

  <div id="sec-powder">
    <div class="panel-title">🧪 펜 도구 & 바닥재</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('SELECT', this)">🔍 개체 선택펜</button>
      <button class="tool-btn" onclick="setTool('MOVE', this)">✋ 개체 이동펜</button>
      <button class="tool-btn" onclick="setTool('ERASER_ALL', this)">🧹 만능 지우개</button>
      <button class="tool-btn" onclick="setTool('DEL_PIXEL', this)">✏️ 픽셀 삭제펜</button>
      <button class="tool-btn active" onclick="setTool('SAND', this)">🟨 금사 모래</button>
      <button class="tool-btn" onclick="setTool('SOIL', this)">🤎 영양 소일</button>
      <button class="tool-btn" onclick="setTool('ROCK', this)">🪨 고정 암석</button>
      <button class="tool-btn" onclick="setTool('WOOD', this)">🪵 고정 유목</button>
      <button class="tool-btn" onclick="setTool('SEED', this)">🌱 수초 씨앗</button>
      <button class="tool-btn" onclick="setTool('FOOD', this)">🟡 먹이 입자</button>
    </div>
  </div>

  <div id="sec-creature" style="display:none;">
    <div class="panel-title">🐟 어종 선택 (총 12종)</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('GUPPY', this)">🐟 구피 (담수)</button>
      <button class="tool-btn" onclick="setTool('TETRA', this)">💙 네온테트라(담수)</button>
      <button class="tool-btn" onclick="setTool('SHRIMP', this)">🦐 체리새우(담수)</button>
      <button class="tool-btn" onclick="setTool('DISCUS', this)">🔴 디스커스(담수)</button>
      <button class="tool-btn" onclick="setTool('ANGEL', this)">🤍 엔젤피쉬(담수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEMI', this)">🐢 반수생거북(담수)</button>
      <button class="tool-btn" onclick="setTool('CLOWN', this)">🧡 크라운피쉬(해수)</button>
      <button class="tool-btn" onclick="setTool('BLUETANG', this)">💙 블루탱(해수)</button>
      <button class="tool-btn" onclick="setTool('PUFFER', this)">🐡 복어(해수)</button>
      <button class="tool-btn" onclick="setTool('YELLOWTANG', this)">💛 옐로우탱(해수)</button>
      <button class="tool-btn" onclick="setTool('QUEENANGEL', this)">👑 퀸엔젤(해수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEA', this)">🐢 바다거북(해수)</button>
    </div>
  </div>

  <div id="sec-equip" style="display:none;">
    <div class="panel-title">🫧 어항 장비 설치</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('BUBBLER_MOVE', this)">🫧 강력 기포기 이동</button>
      <button class="tool-btn" onclick="setTool('FILTER_MOVE', this)">🌀 측면 여과기 이동</button>
      <button class="tool-btn" onclick="setTool('HEATER_MOVE', this)">🔥 어항 히터 이동</button>
    </div>
  </div>

  <div class="box-card">
    <div class="panel-title">💡 조명 및 수온 제어</div>
    <div class="slider-label"><span>🌡️ 수온</span><span id="temp-val">24°C</span></div>
    <input type="range" min="18" max="32" value="24" oninput="document.getElementById('temp-val').innerText=this.value+'°C'; document.getElementById('txt-temp').innerText=this.value;">
    
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
      <span style="font-size:11px; color:#94a3b8;">💡 조명 색상</span>
      <button id="btn-light-toggle" onclick="toggleLight()" style="padding:2px 8px; font-size:10px; background:#0284c7; border:none; color:white; border-radius:4px; cursor:pointer;">ON</button>
    </div>
    <input type="color" id="light-color" value="#00b4d8">
  </div>

  <div style="margin-top:auto; display:flex; gap:6px;">
    <button class="act-btn btn-clean" onclick="cleanPoop()">🧹 똥 청소</button>
    <button class="act-btn btn-reset" onclick="clearTank()">🔄 전체 비우기</button>
  </div>
</div>

<div id="main-container">
  <div id="status-bar">
    <span id="txt-env" style="color:#38bdf8;">🌿 담수 어항</span>
    <span>🌡️ 수온: <span id="txt-temp">24</span>°C</span>
    <span>💧 수질: <span id="txt-quality">100</span>%</span>
    <span>🐠 생물: <span id="txt-count">0</span>마리</span>
  </div>

  <canvas id="sandCanvas" width="1000" height="650"></canvas>

  <div id="info-box">
    <span>📌 어종: <b id="info-name" style="color:#38bdf8;">-</b></span>
    <span>❤️ 체력: <b id="info-hp" style="color:#4ade80;">100%</b></span>
    <span>🍗 포만감: <b id="info-food" style="color:#facc15;">80%</b></span>
    <span>💩 장 상태: <b id="info-poop" style="color:#fb923c;">양호</b></span>
  </div>
</div>

<div id="right-panel">
  <div class="trash-box" onclick="clearTank()">
    <span style="font-size:28px;">🗑️</span>
    <span>비우기</span>
  </div>
  <button class="act-btn" style="background:#0284c7; height:50px;" onclick="addRandomCreature()">🐠 랜던 풀어주기</button>
</div>

<script>
const WIDTH = 500;
const HEIGHT = 325;
const SCALE = 2;

const canvas = document.getElementById('sandCanvas');
const ctx = canvas.getContext('2d');

let grid = Array.from({length: HEIGHT}, () => new Uint8Array(WIDTH));
let poopTypeGrid = Array.from({length: HEIGHT}, () => new Uint8Array(WIDTH));

let tankEnv = 'FRESH';
let currentTool = 'SAND';
let brushSize = 4;
let lightOn = true;

let equipPos = {
  bubbler: { x: 100, y: 310 },
  filter: { x: 460, y: 80 },
  heater: { x: 30, y: 150 }
};

let creatures = [];
let selectedCreature = null;
let draggedCreature = null;

// 어종 데이터 (크기 및 모양 명확히 구분)
const SPECIES_DATA = {
  SHRIMP: { name: '체리새우', env: 'FRESH', color: '#ef4444', size: 6, poopType: 2 },
  GUPPY: { name: '구피', env: 'FRESH', color: '#f59e0b', tailColor: '#ef4444', size: 10, poopType: 1 },
  TETRA: { name: '네온테트라', env: 'FRESH', color: '#0284c7', tailColor: '#ef4444', size: 10, poopType: 2 },
  DISCUS: { name: '디스커스', env: 'FRESH', color: '#dc2626', stripeColor: '#38bdf8', size: 18, poopType: 3 },
  ANGEL: { name: '엔젤피쉬', env: 'FRESH', color: '#f8fafc', stripeColor: '#0f172a', size: 18, poopType: 1 },
  TURTLE_SEMI: { name: '반수생거북', env: 'FRESH', color: '#15803d', shellColor: '#78350f', size: 26, poopType: 3 },
  
  CLOWN: { name: '크라운피쉬', env: 'SALT', color: '#ea580c', stripeColor: '#ffffff', size: 12, poopType: 1 },
  BLUETANG: { name: '블루탱', env: 'SALT', color: '#1d4ed8', tailColor: '#facc15', size: 14, poopType: 1 },
  PUFFER: { name: '복어', env: 'SALT', color: '#facc15', bellyColor: '#ffffff', size: 16, poopType: 3 },
  YELLOWTANG: { name: '옐로우탱', env: 'SALT', color: '#facc15', size: 14, poopType: 1 },
  QUEENANGEL: { name: '퀸엔젤', env: 'SALT', color: '#2563eb', stripeColor: '#facc15', size: 20, poopType: 3 },
  TURTLE_SEA: { name: '바다거북', env: 'SALT', color: '#0d9488', shellColor: '#1e3a8a', size: 34, poopType: 3 }
};

function toggleLight() {
  lightOn = !lightOn;
  document.getElementById('btn-light-toggle').innerText = lightOn ? 'ON' : 'OFF';
  document.getElementById('btn-light-toggle').style.background = lightOn ? '#0284c7' : '#64748b';
}

function setTankEnv(env) {
  tankEnv = env;
  document.getElementById('btn-fresh').classList.toggle('active', env === 'FRESH');
  document.getElementById('btn-salt').classList.toggle('active', env === 'SALT');
  document.getElementById('txt-env').innerText = env === 'FRESH' ? '🌿 담수 어항' : '🪸 해수 어항';
  document.getElementById('txt-env').style.color = env === 'FRESH' ? '#38bdf8' : '#fb923c';
}

function setCategory(cat) {
  document.getElementById('tab-powder').classList.toggle('active', cat === 'POWDER');
  document.getElementById('tab-creature').classList.toggle('active', cat === 'CREATURE');
  document.getElementById('tab-equip').classList.toggle('active', cat === 'EQUIP');

  document.getElementById('sec-powder').style.display = cat === 'POWDER' ? 'block' : 'none';
  document.getElementById('sec-creature').style.display = cat === 'CREATURE' ? 'block' : 'none';
  document.getElementById('sec-equip').style.display = cat === 'EQUIP' ? 'block' : 'none';
}

function setTool(tool, btn) {
  currentTool = tool;
  document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}

function clearTank() {
  for (let y = 0; y < HEIGHT; y++) {
    grid[y].fill(0);
    poopTypeGrid[y].fill(0);
  }
  creatures = [];
  selectedCreature = null;
  document.getElementById('info-box').style.display = 'none';
}

function cleanPoop() {
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      if (grid[y][x] === 8) {
        grid[y][x] = 0;
        poopTypeGrid[y][x] = 0;
      }
    }
  }
}

function addRandomCreature() {
  const keys = Object.keys(SPECIES_DATA);
  const randomKey = keys[Math.floor(Math.random() * keys.length)];
  creatures.push(new Creature(randomKey, Math.random() * (WIDTH - 80) + 40, Math.random() * (HEIGHT - 100) + 50));
}

class Creature {
  constructor(type, x, y) {
    this.type = type;
    this.info = SPECIES_DATA[type];
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 1.0;
    this.vy = (Math.random() - 0.5) * 0.6;
    this.fullness = 60;
    this.health = 100;
    this.digestTimer = 0;
    this.animFrame = Math.random() * 10;
  }

  update() {
    this.animFrame += 0.15;

    if (this.info.env !== tankEnv) {
      this.health -= 0.12;
    }

    this.fullness -= 0.005;
    if (this.fullness < 0) this.fullness = 0;

    // 먹이를 먹고 포만감이 채워지면 똥 배출
    if (this.fullness > 40) {
      this.digestTimer += 1;
      if (this.digestTimer > 400) {
        this.poop();
        this.digestTimer = 0;
        this.fullness -= 10;
      }
    }

    // 적극적으로 먹이 추적
    if (this.fullness < 95) {
      this.findAndEatFood();
    }

    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 25 || this.x > WIDTH - 25) this.vx *= -1;
    if (this.y < 25 || this.y > HEIGHT - 35) this.vy *= -1;

    if (Math.random() < 0.02) {
      this.vx += (Math.random() - 0.5) * 0.5;
      this.vy += (Math.random() - 0.5) * 0.3;
      this.vx = Math.max(-1.5, Math.min(1.5, this.vx));
      this.vy = Math.max(-1.0, Math.min(1.0, this.vy));
    }
  }

  findAndEatFood() {
    let cx = Math.floor(this.x);
    let cy = Math.floor(this.y);
    let found = false;

    // 반경 30px 이내 먹이 탐색 및 돌진
    for (let dy = -30; dy <= 30; dy += 2) {
      for (let dx = -30; dx <= 30; dx += 2) {
        let nx = cx + dx;
        let ny = cy + dy;
        if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
          if (grid[ny][nx] === 7) { // 먹이 발견시 먹이 쪽으로 유 헤엄
            this.vx = dx * 0.05;
            this.vy = dy * 0.05;
            found = true;
            
            // 근접시 섭취
            if (Math.abs(dx) <= 4 && Math.abs(dy) <= 4) {
              grid[ny][nx] = 0;
              this.fullness = Math.min(100, this.fullness + 8);
            }
            return;
          }
        }
      }
    }
  }

  poop() {
    let px = Math.floor(this.x);
    let py = Math.floor(this.y) + Math.floor(this.info.size / 2) + 2;
    if (px >= 0 && px < WIDTH && py >= 0 && py < HEIGHT) {
      grid[py][px] = 8;
      poopTypeGrid[py][px] = this.info.poopType;
    }
  }

  draw() {
    let sx = this.x * SCALE;
    let sy = this.y * SCALE;
    let dir = this.vx >= 0 ? 1 : -1;
    let wiggle = Math.sin(this.animFrame) * 3;
    let s = this.info.size;

    ctx.save();
    ctx.translate(sx, sy);

    // 고퀄리티 픽셀 도트 아트
    if (this.type === 'TURTLE_SEMI') {
      // 반수생 거북이 (귀여운 도트 디자인)
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-s/2, -s/3, s, s*0.7); // 등껍질
      ctx.fillStyle = '#f59e0b'; // 등 테두리
      ctx.strokeRect(-s/2, -s/3, s, s*0.7);
      
      ctx.fillStyle = '#16a34a'; // 머리 & 다리
      ctx.fillRect(dir * (s/2), -s/6, s/3, s/3);
      ctx.fillStyle = '#ef4444'; ctx.fillRect(dir * (s/1.8), -s/10, 2, 2); // 빨간 볼
      ctx.fillStyle = '#16a34a';
      ctx.fillRect(-s/3, -s/2, 4, 4); ctx.fillRect(s/6, -s/2, 4, 4);
      ctx.fillRect(-s/3, s/3, 4, 4); ctx.fillRect(s/6, s/3, 4, 4);
    } 
    else if (this.type === 'TURTLE_SEA') {
      // 바다 거북이
      ctx.fillStyle = '#0f766e';
      ctx.fillRect(-s/2, -s/3, s, s*0.65);
      ctx.fillStyle = '#115e59';
      ctx.fillRect(-s/3, -s/4, s*0.6, s*0.5);

      ctx.fillStyle = '#0d9488'; // 유선형 머리 & 지느러미
      ctx.fillRect(dir * (s/2), -s/8, s/3, s/3);
      ctx.fillRect(-s/4, -s/1.5, s/3, s/2);
      ctx.fillRect(-s/4, s/3, s/3, s/2);
    }
    else {
      // 열대어 & 해수어 (지느러미, 꼬리 살랑거림)
      ctx.fillStyle = this.info.color;
      ctx.fillRect(-s/2, -s/3, s, s*0.6);

      if (this.info.stripeColor) {
        ctx.fillStyle = this.info.stripeColor;
        ctx.fillRect(-s/6, -s/3, 3, s*0.6);
      }

      // 눈
      ctx.fillStyle = '#ffffff'; ctx.fillRect(dir * (s/3), -s/5, 3, 3);
      ctx.fillStyle = '#000000'; ctx.fillRect(dir * (s/3) + (dir > 0 ? 1 : 0), -s/5 + 1, 1, 1);

      // 꼬리
      ctx.fillStyle = this.info.tailColor || this.info.color;
      ctx.beginPath();
      ctx.moveTo(-dir * (s/2), 0);
      ctx.lineTo(-dir * (s * 0.9), -s/3 + wiggle);
      ctx.lineTo(-dir * (s * 0.9), s/3 + wiggle);
      ctx.fill();
    }

    if (selectedCreature === this) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.strokeRect(-s, -s, s*2, s*2);
    }

    if (this.info.env !== tankEnv) {
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(-s*0.8, -s*0.8, s*1.6, s*1.6);
    }

    ctx.restore();
  }
}

let isMouseDown = false;

canvas.addEventListener('mousedown', e => {
  isMouseDown = true;
  const rect = canvas.getBoundingClientRect();
  const mx = Math.floor((e.clientX - rect.left) / SCALE);
  const my = Math.floor((e.clientY - rect.top) / SCALE);

  if (currentTool === 'SELECT') {
    selectedCreature = creatures.find(c => Math.abs(c.x - mx) < c.info.size && Math.abs(c.y - my) < c.info.size);
    const infoBox = document.getElementById('info-box');
    if (selectedCreature) {
      infoBox.style.display = 'flex';
      document.getElementById('info-name').innerText = selectedCreature.info.name;
      document.getElementById('info-hp').innerText = Math.max(0, Math.floor(selectedCreature.health)) + '%';
      document.getElementById('info-food').innerText = Math.floor(selectedCreature.fullness) + '%';
      document.getElementById('info-poop').innerText = selectedCreature.digestTimer > 200 ? '배변 임박' : '양호';
    } else {
      infoBox.style.display = 'none';
    }
    return;
  }

  if (currentTool === 'MOVE') {
    draggedCreature = creatures.find(c => Math.abs(c.x - mx) < c.info.size && Math.abs(c.y - my) < c.info.size);
    return;
  }

  handleInput(e);
});

canvas.addEventListener('mousemove', e => {
  const rect = canvas.getBoundingClientRect();
  const mx = Math.floor((e.clientX - rect.left) / SCALE);
  const my = Math.floor((e.clientY - rect.top) / SCALE);

  if (draggedCreature && isMouseDown) {
    draggedCreature.x = mx;
    draggedCreature.y = my;
    return;
  }

  if (isMouseDown) handleInput(e);
});

canvas.addEventListener('mouseup', () => {
  isMouseDown = false;
  draggedCreature = null;
});

function handleInput(e) {
  const rect = canvas.getBoundingClientRect();
  const mx = Math.floor((e.clientX - rect.left) / SCALE);
  const my = Math.floor((e.clientY - rect.top) / SCALE);

  if (mx < 0 || mx >= WIDTH || my < 0 || my >= HEIGHT) return;

  if (currentTool === 'BUBBLER_MOVE') { equipPos.bubbler = {x: mx, y: my}; return; }
  if (currentTool === 'FILTER_MOVE') { equipPos.filter = {x: mx, y: my}; return; }
  if (currentTool === 'HEATER_MOVE') { equipPos.heater = {x: mx, y: my}; return; }

  if (SPECIES_DATA[currentTool]) {
    if (e.type === 'mousedown') {
      creatures.push(new Creature(currentTool, mx, my));
    }
    return;
  }

  // 씨앗 및 브러시 도구 작동
  for (let dy = -brushSize; dy <= brushSize; dy++) {
    for (let dx = -brushSize; dx <= brushSize; dx++) {
      let nx = mx + dx;
      let ny = my + dy;
      if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
        if (currentTool === 'SAND') grid[ny][nx] = 1;
        else if (currentTool === 'SOIL') grid[ny][nx] = 2;
        else if (currentTool === 'ROCK') grid[ny][nx] = 3;
        else if (currentTool === 'WOOD') grid[ny][nx] = 4;
        else if (currentTool === 'SEED') { grid[ny][nx] = 5; } // 씨앗 즉시 도포
        else if (currentTool === 'FOOD') grid[ny][nx] = 7;
        else if (currentTool === 'ERASER_ALL' || currentTool === 'DEL_PIXEL') {
          grid[ny][nx] = 0;
          poopTypeGrid[ny][nx] = 0;
        }
      }
    }
  }
}

function updatePhysics() {
  for (let y = HEIGHT - 2; y >= 0; y--) {
    for (let x = 0; x < WIDTH; x++) {
      let type = grid[y][x];

      if (type === 1 || type === 2 || type === 7 || type === 8) {
        if (grid[y + 1][x] === 0) {
          grid[y + 1][x] = type;
          poopTypeGrid[y + 1][x] = poopTypeGrid[y][x];
          grid[y][x] = 0;
          poopTypeGrid[y][x] = 0;
        } else if (x > 0 && grid[y + 1][x - 1] === 0) {
          grid[y + 1][x - 1] = type;
          grid[y][x] = 0;
        } else if (x < WIDTH - 1 && grid[y + 1][x + 1] === 0) {
          grid[y + 1][x + 1] = type;
          grid[y][x] = 0;
        }
      }

      // 수초 씨앗(5)은 바닥재 위에서 줄기 성장
      if (type === 5) {
        let under = grid[y + 1] ? grid[y + 1][x] : 0;
        if ([1, 2, 3, 4, 6].includes(under)) {
          if (Math.random() < 0.08) {
            grid[y][x] = 6;
            if (y > 10 && Math.random() < 0.75) grid[y - 1][x] = 5;
          }
        }
      }
    }
  }
}

function loop() {
  updatePhysics();

  ctx.fillStyle = tankEnv === 'FRESH' ? '#030a17' : '#010512';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 조명 이펙트
  if (lightOn) {
    let lightColor = document.getElementById('light-color').value;
    ctx.fillStyle = lightColor;
    ctx.globalAlpha = 0.12;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.globalAlpha = 1.0;
  }

  // 1. 대폭 강화된 기포기 이펙트 (보글보글 물살)
  ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
  for (let i = 0; i < 12; i++) {
    let bx = equipPos.bubbler.x + (Math.random() - 0.5) * 12;
    let by = equipPos.bubbler.y - Math.random() * 80;
    let bSize = Math.random() * 3 + 1;
    ctx.fillRect(bx * SCALE, by * SCALE, bSize, bSize);
  }
  ctx.fillStyle = '#475569';
  ctx.fillRect((equipPos.bubbler.x - 8) * SCALE, equipPos.bubbler.y * SCALE, 16 * SCALE, 8 * SCALE);

  // 2. 여과기
  ctx.fillStyle = '#1e293b';
  ctx.fillRect(equipPos.filter.x * SCALE, equipPos.filter.y * SCALE, 16 * SCALE, 35 * SCALE);

  // 3. 히터
  ctx.fillStyle = '#334155';
  ctx.fillRect(equipPos.heater.x * SCALE, equipPos.heater.y * SCALE, 6 * SCALE, 45 * SCALE);
  ctx.fillStyle = '#ef4444';
  ctx.fillRect((equipPos.heater.x + 1) * SCALE, (equipPos.heater.y + 30) * SCALE, 4 * SCALE, 12 * SCALE);

  // 파우더 그리기
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      let t = grid[y][x];
      if (t === 0) continue;

      if (t === 1) ctx.fillStyle = '#f59e0b';
      else if (t === 2) ctx.fillStyle = '#57534e';
      else if (t === 3) ctx.fillStyle = '#475569';
      else if (t === 4) ctx.fillStyle = '#78350f';
      else if (t === 5) ctx.fillStyle = '#86efac'; // 발아 전 씨앗
      else if (t === 6) ctx.fillStyle = '#16a34a'; // 자란 수초
      else if (t === 7) ctx.fillStyle = '#facc15'; // 먹이
      else if (t === 8) { // 똥
        let pt = poopTypeGrid[y][x];
        if (pt === 1) ctx.fillStyle = '#451a03';
        else if (pt === 2) ctx.fillStyle = '#78350f';
        else ctx.fillStyle = '#1c1917';
      }
      ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
    }
  }

  // 생물 그리기
  for (let i = creatures.length - 1; i >= 0; i--) {
    let c = creatures[i];
    c.update();
    c.draw();
    if (c.health <= 0) {
      creatures.splice(i, 1);
      if (selectedCreature === c) selectedCreature = null;
    }
  }

  document.getElementById('txt-count').innerText = creatures.length;
  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(html_code, height=680)
