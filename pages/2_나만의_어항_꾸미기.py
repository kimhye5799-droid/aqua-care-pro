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
  body { background-color: #080f1e; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; height: 100vh; overflow: hidden; }
  
  /* 패널 공통 */
  #sidebar { width: 290px; background-color: #0f1a30; padding: 14px; display: flex; flex-direction: column; gap: 12px; overflow-y: auto; border-right: 1px solid #1e2f4d; }
  .panel-title { font-size: 13px; font-weight: bold; color: #4cc9f0; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }
  
  .mode-btn-group { display: flex; gap: 4px; }
  .mode-btn { flex: 1; padding: 8px 4px; background-color: #162646; border: 1px solid #233861; color: #94a3b8; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: bold; transition: 0.2s; }
  .mode-btn.active { background-color: #0284c7; color: #ffffff; border-color: #38bdf8; box-shadow: 0 0 8px rgba(56, 189, 248, 0.4); }
  
  .tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .tool-btn { padding: 8px 6px; background-color: #162646; border: 1px solid #233861; color: #e2e8f0; border-radius: 6px; cursor: pointer; font-size: 11px; text-align: left; display: flex; align-items: center; gap: 5px; }
  .tool-btn.active { border-color: #38bdf8; background-color: #1e3a8a; color: #38bdf8; font-weight: bold; box-shadow: 0 0 6px rgba(56,189,248,0.3); }
  
  .box-card { background: #162646; padding: 10px; border-radius: 6px; border: 1px solid #233861; display: flex; flex-direction: column; gap: 6px; }
  .slider-label { font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; }
  input[type="range"], input[type="color"] { width: 100%; accent-color: #38bdf8; cursor: pointer; }
  input[type="color"] { height: 26px; border: none; background: transparent; }

  /* 메인 화면 */
  #main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: #030712; padding: 10px; }
  canvas { border: 3px solid #0284c7; border-radius: 12px; cursor: crosshair; box-shadow: 0 0 30px rgba(2, 132, 199, 0.3); background: #000; }
  
  #status-bar { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); background: rgba(15, 26, 48, 0.92); padding: 8px 20px; border-radius: 20px; border: 1px solid #38bdf8; display: flex; gap: 16px; font-size: 12px; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
  
  #info-box { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(15, 26, 48, 0.95); padding: 10px 20px; border-radius: 10px; border: 1px solid #4cc9f0; font-size: 12px; display: none; gap: 15px; }

  /* 우측 제어판 */
  #right-panel { width: 110px; background-color: #0f1a30; padding: 14px 10px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; border-left: 1px solid #1e2f4d; }
  .trash-box { width: 100%; height: 110px; border: 2px dashed #ef4444; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #ef4444; font-size: 11px; gap: 6px; cursor: pointer; transition: 0.2s; }
  .trash-box:hover { background: rgba(239, 68, 68, 0.15); }
  
  .act-btn { padding: 9px; border: none; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; color: white; width: 100%; }
  .btn-reset { background: #ef4444; }
  .btn-clean { background: #0284c7; }
</style>
</head>
<body>

<!-- 왼쪽 사이드바 -->
<div id="sidebar">
  <div>
    <div class="panel-title">🌊 어항 환경 (담수 / 해수)</div>
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
    <div class="slider-label"><span>🖌️ 브러시 크기</span><span id="brush-val">3 px</span></div>
    <input type="range" id="brush-size" min="1" max="10" value="3" oninput="brushSize=parseInt(this.value); document.getElementById('brush-val').innerText=this.value+' px';">
  </div>

  <!-- 1. 파우더 모드 -->
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

  <!-- 2. 생물 모드 -->
  <div id="sec-creature" style="display:none;">
    <div class="panel-title">🐟 어종 및 픽셀 생물</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('GUPPY', this)">🐟 구피 (담수)</button>
      <button class="tool-btn" onclick="setTool('TETRA', this)">💙 네온테트라(담수)</button>
      <button class="tool-btn" onclick="setTool('SHRIMP', this)">🦐 체리새우(담수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEMI', this)">🐢 반수생거북(담수)</button>
      <button class="tool-btn" onclick="setTool('CLOWN', this)">🧡 크라운피쉬(해수)</button>
      <button class="tool-btn" onclick="setTool('BLUETANG', this)">💙 블루탱(해수)</button>
      <button class="tool-btn" onclick="setTool('PUFFER', this)">🐡 복어(해수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEA', this)">🐢 바다거북(해수)</button>
    </div>
  </div>

  <!-- 3. 장비 모드 -->
  <div id="sec-equip" style="display:none;">
    <div class="panel-title">🫧 어항 풀장비 복원</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('BUBBLER_MOVE', this)">🫧 기포기 (이동가능)</button>
      <button class="tool-btn" onclick="setTool('FILTER_MOVE', this)">🌀 측면 여과기</button>
      <button class="tool-btn" onclick="setTool('HEATER_MOVE', this)">🔥 어항 히터</button>
    </div>
  </div>

  <!-- 환경 세부 설정 -->
  <div class="box-card">
    <div class="panel-title">⚙️ 어항 제어</div>
    <div class="slider-label"><span>🌡️ 수온 설정</span><span id="temp-val">24°C</span></div>
    <input type="range" min="18" max="32" value="24" oninput="document.getElementById('temp-val').innerText=this.value+'°C'; document.getElementById('txt-temp').innerText=this.value;">
    
    <div class="slider-label" style="margin-top:6px;"><span>💡 조명 색상</span></div>
    <input type="color" id="light-color" value="#00b4d8">
  </div>

  <div style="margin-top:auto; display:flex; gap:6px;">
    <button class="act-btn btn-clean" onclick="cleanPoop()">🧹 똥 청소</button>
    <button class="act-btn btn-reset" onclick="clearTank()">🔄 리셋</button>
  </div>
</div>

<!-- 메인 Canvas 어항 -->
<div id="main-container">
  <div id="status-bar">
    <span id="txt-env" style="color:#38bdf8;">🌿 담수 어항</span>
    <span>🌡️ 수온: <span id="txt-temp">24</span>°C</span>
    <span>💧 수질: <span id="txt-quality">100</span>%</span>
    <span>🐠 생물: <span id="txt-count">0</span>마리</span>
  </div>

  <!-- 1000x650 대형 픽셀 어항 -->
  <canvas id="sandCanvas" width="1000" height="650"></canvas>

  <div id="info-box">
    <span>📌 이름: <b id="info-name" style="color:#38bdf8;">-</b></span>
    <span>❤️ 건강: <b id="info-hp" style="color:#4ade80;">100%</b></span>
    <span>🍗 포만감: <b id="info-food" style="color:#facc15;">80%</b></span>
    <span>💩 장 상태: <b id="info-poop" style="color:#fb923c;">보통</b></span>
  </div>
</div>

<!-- 우측 제어판 -->
<div id="right-panel">
  <div class="trash-box" onclick="clearTank()">
    <span style="font-size:28px;">🗑️</span>
    <span>물체 버리기</span>
    <span style="font-size:9px; color:#94a3b8;">(클릭시 비우기)</span>
  </div>
  <button class="act-btn" style="background:#0284c7; height:50px;" onclick="addRandomCreature()">🐠 생물 풀어주기</button>
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
let brushSize = 3;

// 장비 위치 좌표
let equipPos = {
  bubbler: { x: 80, y: 310 },
  filter: { x: 460, y: 80 },
  heater: { x: 30, y: 150 }
};

let creatures = [];
let selectedCreature = null;
let draggedCreature = null;

// 어종 데이터 및 귀여운 픽셀 아웃라인
const SPECIES_DATA = {
  GUPPY: { name: '구피', env: 'FRESH', color: '#f59e0b', tailColor: '#ef4444', size: 8, poopType: 1 },
  TETRA: { name: '네온테트라', env: 'FRESH', color: '#0284c7', tailColor: '#ef4444', size: 7, poopType: 2 },
  SHRIMP: { name: '체리새우', env: 'FRESH', color: '#ef4444', tailColor: '#f87171', size: 6, poopType: 2 },
  TURTLE_SEMI: { name: '반수생거북', env: 'FRESH', color: '#15803d', shellColor: '#78350f', size: 16, poopType: 3 },
  CLOWN: { name: '크라운피쉬', env: 'SALT', color: '#f97316', stripeColor: '#ffffff', size: 9, poopType: 1 },
  BLUETANG: { name: '블루탱', env: 'SALT', color: '#1d4ed8', tailColor: '#facc15', size: 10, poopType: 1 },
  PUFFER: { name: '복어', env: 'SALT', color: '#facc15', bellyColor: '#ffffff', size: 12, poopType: 3 },
  TURTLE_SEA: { name: '바다거북', env: 'SALT', color: '#0d9488', shellColor: '#1e3a8a', size: 22, poopType: 3 }
};

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
  creatures.push(new Creature(randomKey, Math.random() * (WIDTH - 60) + 30, Math.random() * (HEIGHT - 80) + 40));
}

// 생물 객체
class Creature {
  constructor(type, x, y) {
    this.type = type;
    this.info = SPECIES_DATA[type];
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 1.0;
    this.vy = (Math.random() - 0.5) * 0.6;
    this.fullness = 75;
    this.health = 100;
    this.digestTimer = 0;
    this.animFrame = 0;
  }

  update() {
    this.animFrame += 0.1;

    // 담수/해수 불일치 시 사망
    if (this.info.env !== tankEnv) {
      this.health -= 0.1;
    }

    // 포만감 느리게 소모
    this.fullness -= 0.006;
    if (this.fullness < 0) this.fullness = 0;

    // 배변 시뮬레이션
    if (this.fullness > 35) {
      this.digestTimer += 1;
      if (this.digestTimer > 550) {
        this.poop();
        this.digestTimer = 0;
        this.fullness -= 8;
      }
    }

    // 먹이 탐색
    if (this.fullness < 95) {
      this.findFood();
    }

    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 20 || this.x > WIDTH - 20) this.vx *= -1;
    if (this.y < 20 || this.y > HEIGHT - 30) this.vy *= -1;

    if (Math.random() < 0.02) {
      this.vx += (Math.random() - 0.5) * 0.4;
      this.vy += (Math.random() - 0.5) * 0.3;
      this.vx = Math.max(-1.2, Math.min(1.2, this.vx));
      this.vy = Math.max(-0.8, Math.min(0.8, this.vy));
    }
  }

  findFood() {
    let cx = Math.floor(this.x);
    let cy = Math.floor(this.y);
    for (let dy = -8; dy <= 8; dy++) {
      for (let dx = -8; dx <= 8; dx++) {
        let nx = cx + dx;
        let ny = cy + dy;
        if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
          if (grid[ny][nx] === 7) { // 먹이 발견
            grid[ny][nx] = 0;
            this.fullness = Math.min(100, this.fullness + 6); // 느리게 참
            return;
          }
        }
      }
    }
  }

  poop() {
    let px = Math.floor(this.x);
    let py = Math.floor(this.y) + 4;
    if (px >= 0 && px < WIDTH && py >= 0 && py < HEIGHT) {
      grid[py][px] = 8;
      poopTypeGrid[py][px] = this.info.poopType;
    }
  }

  draw() {
    let sx = this.x * SCALE;
    let sy = this.y * SCALE;
    let dir = this.vx >= 0 ? 1 : -1;
    let tailWiggle = Math.sin(this.animFrame) * 2;

    ctx.save();
    ctx.translate(sx, sy);

    // 귀여운 픽셀 아웃라인 그리기
    if (this.type === 'TURTLE_SEMI') {
      // 반수생 거북
      ctx.fillStyle = this.info.shellColor;
      ctx.fillRect(-10, -6, 20, 12); // 등껍질
      ctx.fillStyle = this.info.color;
      ctx.fillRect(dir * 10, -4, 6, 6); // 머리
      ctx.fillRect(-8, -10, 4, 4); ctx.fillRect(4, -10, 4, 4); // 다리
      ctx.fillRect(-8, 6, 4, 4); ctx.fillRect(4, 6, 4, 4);
    } else if (this.type === 'TURTLE_SEA') {
      // 바다 거북
      ctx.fillStyle = this.info.shellColor;
      ctx.fillRect(-16, -10, 32, 20); // 큰 등껍질
      ctx.fillStyle = this.info.color;
      ctx.fillRect(dir * 16, -6, 10, 10); // 머리
      ctx.fillRect(-12, -18, 10, 8); ctx.fillRect(4, -18, 10, 8); // 큰 앞지느러미
    } else {
      // 일반 열대어 / 해수어
      let s = this.info.size;
      ctx.fillStyle = this.info.color;
      ctx.fillRect(-s, -s/2, s*1.6, s); // 몸통

      // 눈
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(dir * (s/2), -s/3, 3, 3);
      ctx.fillStyle = '#000000';
      ctx.fillRect(dir * (s/2) + (dir > 0 ? 1 : 0), -s/3 + 1, 1, 1);

      // 살랑거리는 꼬리
      ctx.fillStyle = this.info.tailColor || this.info.color;
      ctx.beginPath();
      ctx.moveTo(-dir * s, 0);
      ctx.lineTo(-dir * (s * 1.8), -s/2 + tailWiggle);
      ctx.lineTo(-dir * (s * 1.8), s/2 + tailWiggle);
      ctx.fill();
    }

    // 선택 시 하이라이트 박스
    if (selectedCreature === this) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.strokeRect(-20, -20, 40, 40);
    }

    // 서식 환경 안 맞을 경우 빨간 경고 오라
    if (this.info.env !== tankEnv) {
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(-18, -18, 36, 36);
    }

    ctx.restore();
  }
}

// 이벤트 제어 (선택, 드래그, 그리기)
let isMouseDown = false;

canvas.addEventListener('mousedown', e => {
  isMouseDown = true;
  const rect = canvas.getBoundingClientRect();
  const mx = Math.floor((e.clientX - rect.left) / SCALE);
  const my = Math.floor((e.clientY - rect.top) / SCALE);

  // 1. 개체 선택펜
  if (currentTool === 'SELECT') {
    selectedCreature = creatures.find(c => Math.abs(c.x - mx) < 15 && Math.abs(c.y - my) < 15);
    const infoBox = document.getElementById('info-box');
    if (selectedCreature) {
      infoBox.style.display = 'flex';
      document.getElementById('info-name').innerText = selectedCreature.info.name;
      document.getElementById('info-hp').innerText = Math.max(0, Math.floor(selectedCreature.health)) + '%';
      document.getElementById('info-food').innerText = Math.floor(selectedCreature.fullness) + '%';
      document.getElementById('info-poop').innerText = selectedCreature.digestTimer > 300 ? '배변 임박' : '양호';
    } else {
      infoBox.style.display = 'none';
    }
    return;
  }

  // 2. 개체 이동펜
  if (currentTool === 'MOVE') {
    draggedCreature = creatures.find(c => Math.abs(c.x - mx) < 15 && Math.abs(c.y - my) < 15);
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

  // 장비 위치 이동
  if (currentTool === 'BUBBLER_MOVE') { equipPos.bubbler = {x: mx, y: my}; return; }
  if (currentTool === 'FILTER_MOVE') { equipPos.filter = {x: mx, y: my}; return; }
  if (currentTool === 'HEATER_MOVE') { equipPos.heater = {x: mx, y: my}; return; }

  // 생물 스폰
  if (SPECIES_DATA[currentTool]) {
    if (e.type === 'mousedown') {
      creatures.push(new Creature(currentTool, mx, my));
    }
    return;
  }

  // 파우더 및 브러시
  for (let dy = -brushSize; dy <= brushSize; dy++) {
    for (let dx = -brushSize; dx <= brushSize; dx++) {
      let nx = mx + dx;
      let ny = my + dy;
      if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
        if (currentTool === 'SAND') grid[ny][nx] = 1;
        else if (currentTool === 'SOIL') grid[ny][nx] = 2;
        else if (currentTool === 'ROCK') grid[ny][nx] = 3;
        else if (currentTool === 'WOOD') grid[ny][nx] = 4;
        else if (currentTool === 'SEED') { if (grid[ny][nx] === 0) grid[ny][nx] = 5; }
        else if (currentTool === 'FOOD') grid[ny][nx] = 7;
        else if (currentTool === 'ERASER_ALL' || currentTool === 'DEL_PIXEL') {
          grid[ny][nx] = 0;
          poopTypeGrid[ny][nx] = 0;
        }
      }
    }
  }
}

// 샌드박스 물리엔진 & 씨앗 성장
function updatePhysics() {
  for (let y = HEIGHT - 2; y >= 0; y--) {
    for (let x = 0; x < WIDTH; x++) {
      let type = grid[y][x];

      // 모래(1), 소일(2), 먹이(7), 똥(8) 중력 낙하
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

      // 수초 씨앗(5) 발아: 모래, 소일, 바위, 유목 위에서 자라남
      if (type === 5) {
        let under = grid[y + 1] ? grid[y + 1][x] : 0;
        if ([1, 2, 3, 4, 6].includes(under)) {
          if (Math.random() < 0.04) {
            grid[y][x] = 6; // 수초 성장
            if (y > 10 && Math.random() < 0.7) grid[y - 1][x] = 5;
          }
        }
      }
    }
  }
}

// 메인 루프
function loop() {
  updatePhysics();

  // 조명 색상 및 어항 배경
  let lightColor = document.getElementById('light-color').value;
  ctx.fillStyle = tankEnv === 'FRESH' ? '#030c1e' : '#010614';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 어항 조명 효과
  ctx.fillStyle = lightColor;
  ctx.globalAlpha = 0.08;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.globalAlpha = 1.0;

  // 1. 기포기 이펙트
  ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
  for (let i = 0; i < 4; i++) {
    let bx = equipPos.bubbler.x + (Math.random() - 0.5) * 8;
    let by = equipPos.bubbler.y - Math.random() * 40;
    ctx.fillRect(bx * SCALE, by * SCALE, 2, 2);
  }
  ctx.fillStyle = '#64748b';
  ctx.fillRect((equipPos.bubbler.x - 6) * SCALE, equipPos.bubbler.y * SCALE, 12 * SCALE, 6 * SCALE);

  // 2. 측면 여과기 이펙트
  ctx.fillStyle = '#334155';
  ctx.fillRect(equipPos.filter.x * SCALE, equipPos.filter.y * SCALE, 14 * SCALE, 30 * SCALE);
  ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
  for (let i = 0; i < 3; i++) {
    ctx.fillRect((equipPos.filter.x - Math.random() * 25) * SCALE, (equipPos.filter.y + 10 + Math.random() * 10) * SCALE, 3, 2);
  }

  // 3. 어항 히터 이펙트
  ctx.fillStyle = '#475569';
  ctx.fillRect(equipPos.heater.x * SCALE, equipPos.heater.y * SCALE, 6 * SCALE, 40 * SCALE);
  ctx.fillStyle = '#ef4444';
  ctx.fillRect((equipPos.heater.x + 1) * SCALE, (equipPos.heater.y + 25) * SCALE, 4 * SCALE, 10 * SCALE);

  // 그리드 파우더 그리기
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      let t = grid[y][x];
      if (t === 0) continue;

      if (t === 1) ctx.fillStyle = '#f59e0b'; // 모래
      else if (t === 2) ctx.fillStyle = '#57534e'; // 소일
      else if (t === 3) ctx.fillStyle = '#475569'; // 암석
      else if (t === 4) ctx.fillStyle = '#78350f'; // 유목
      else if (t === 5) ctx.fillStyle = '#4ade80'; // 씨앗
      else if (t === 6) ctx.fillStyle = '#16a34a'; // 수초
      else if (t === 7) ctx.fillStyle = '#facc15'; // 먹이
      else if (t === 8) {
        let pt = poopTypeGrid[y][x];
        if (pt === 1) ctx.fillStyle = '#451a03';
        else if (pt === 2) ctx.fillStyle = '#78350f';
        else ctx.fillStyle = '#292524';
      }
      ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
    }
  }

  // 생물 업데이트 및 그리기
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
