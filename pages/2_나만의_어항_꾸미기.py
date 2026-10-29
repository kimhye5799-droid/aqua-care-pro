import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="나만의 픽셀 어항 꾸미기", layout="wide")

st.title("🐠 나만의 픽셀 어항 Sandbox (업그레이드 버젼)")
st.caption("어항 모드(담수/해수), 포만감 밸런스, 어종별 맞춤 똥, 수초 씨앗 발아, 자유 기포기 이동 기능 지원")

# HTML/JS Canvas Sandbox Code
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body { background-color: #0b132b; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; height: 100vh; overflow: hidden; }
  
  #sidebar { width: 300px; background-color: #1c2541; padding: 15px; display: flex; flex-direction: column; gap: 15px; overflow-y: auto; border-right: 2px solid #3a506b; }
  h2 { font-size: 16px; color: #4cc9f0; margin-bottom: 8px; border-bottom: 1px solid #3a506b; padding-bottom: 4px; }
  
  .mode-btn-group { display: flex; gap: 5px; }
  .mode-btn { flex: 1; padding: 8px 4px; background-color: #3a506b; border: none; color: white; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 12px; }
  .mode-btn.active { background-color: #4cc9f0; color: #0b132b; }
  
  .tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .tool-btn { padding: 8px 6px; background-color: #0b132b; border: 1px solid #3a506b; color: #e0e1dd; border-radius: 4px; cursor: pointer; font-size: 11px; text-align: left; }
  .tool-btn.active { border-color: #4cc9f0; background-color: #1c2541; color: #4cc9f0; font-weight: bold; }
  
  .setting-item { display: flex; flex-direction: column; gap: 4px; font-size: 12px; }
  select, input[type="range"] { width: 100%; padding: 4px; background: #0b132b; color: white; border: 1px solid #3a506b; border-radius: 4px; }
  
  #main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: #000814; }
  canvas { border: 2px solid #4cc9f0; border-radius: 8px; cursor: crosshair; box-shadow: 0 0 20px rgba(76, 201, 240, 0.2); }
  
  #status-bar { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); background: rgba(11, 19, 43, 0.85); padding: 8px 18px; border-radius: 20px; border: 1px solid #4cc9f0; display: flex; gap: 15px; font-size: 13px; font-weight: bold; }
  .badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; }
  .badge-fresh { background: #2a9d8f; color: white; }
  .badge-salt { background: #e76f51; color: white; }
</style>
</head>
<body>

<div id="sidebar">
  <div>
    <h2>🌊 어항 환경 설정</h2>
    <div class="mode-btn-group">
      <button class="mode-btn active" id="btn-env-fresh" onclick="setTankEnv('FRESH')">🌿 담수 어항</button>
      <button class="mode-btn" id="btn-env-salt" onclick="setTankEnv('SALT')">🪸 해수 어항</button>
    </div>
  </div>

  <div>
    <h2>🛠️ 도구 카테고리</h2>
    <div class="mode-btn-group">
      <button class="mode-btn active" onclick="setCategory('POWDER')">파우더</button>
      <button class="mode-btn" onclick="setCategory('CREATURE')">생물</button>
      <button class="mode-btn" onclick="setCategory('EQUIP')">장비</button>
    </div>
  </div>

  <div id="section-powder">
    <h2>⏳ 파우더 / 씨앗 / 먹이</h2>
    <div class="tool-grid">
      <button class="tool-btn active" onclick="setTool('SAND')">🌾 금사 모래</button>
      <button class="tool-btn" onclick="setTool('SOIL')">🤎 영양 소일</button>
      <button class="tool-btn" onclick="setTool('ROCK')">🪨 고정 암석</button>
      <button class="tool-btn" onclick="setTool('WOOD')">🪵 고정 유목</button>
      <button class="tool-btn" onclick="setTool('SEED')">🌱 수초 씨앗</button>
      <button class="tool-btn" onclick="setTool('FOOD')">🟡 먹이 입자</button>
      <button class="tool-btn" onclick="setTool('ERASER')">🧹 지우개/청소</button>
    </div>
  </div>

  <div id="section-creature" style="display:none;">
    <h2>🐟 어종 & 생물 (담수/해수)</h2>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('GUPPY')">🐟 구피 (담수)</button>
      <button class="tool-btn" onclick="setTool('TETRA')">💙 네온테트라(담수)</button>
      <button class="tool-btn" onclick="setTool('SEAGULL')">🦐 체리새우 (담수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEMI')">🐢 반수생거북(담수)</button>
      <button class="tool-btn" onclick="setTool('CLOWN')">🧡 크라운피쉬(해수)</button>
      <button class="tool-btn" onclick="setTool('BLUETANG')">💙 블루탱 (해수)</button>
      <button class="tool-btn" onclick="setTool('PUFFER')">🐡 복어 (해수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEA')">🐢 바다거북 (해수)</button>
    </div>
  </div>

  <div id="section-equip" style="display:none;">
    <h2>🫧 어항 장비</h2>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('BUBBLER_MOVE')">🫧 기포기 위치 변경</button>
    </div>
  </div>

  <div>
    <h2>⚙️ 브러시 크기</h2>
    <div class="setting-item">
      <input type="range" id="brush-size" min="1" max="10" value="3" onchange="brushSize = parseInt(this.value)">
    </div>
  </div>
  
  <div style="margin-top:auto;">
    <button class="mode-btn" style="background:#e63946; width:100%;" onclick="clearTank()">🗑️ 전체 비우기</button>
  </div>
</div>

<div id="main-container">
  <div id="status-bar">
    <span id="env-badge" class="badge badge-fresh">담수 어항</span>
    <span>🌡️ 수온: <span id="txt-temp">25</span>°C</span>
    <span>💧 수질: <span id="txt-quality">100</span>%</span>
    <span>🐠 생물: <span id="txt-count">0</span>마리</span>
  </div>
  <canvas id="sandCanvas" width="600" height="400"></canvas>
</div>

<script>
const WIDTH = 300;
const HEIGHT = 200;
const SCALE = 2; // 600x400

const canvas = document.getElementById('sandCanvas');
const ctx = canvas.getContext('2d');

// 샌드박스 그리드 (0: Empty, 1: Sand, 2: Soil, 3: Rock, 4: Wood, 5: Seed, 6: Plant, 7: Food, 8: Poop)
let grid = Array.from({length: HEIGHT}, () => new Uint8Array(WIDTH));
let poopTypeGrid = Array.from({length: HEIGHT}, () => new Uint8Array(WIDTH)); // 똥 모양 기록

let tankEnv = 'FRESH'; // 'FRESH' or 'SALT'
let currentCategory = 'POWDER';
let currentTool = 'SAND';
let brushSize = 3;

// 기포기 좌표 (기본 중앙 하단)
let bubblerPos = { x: 150, y: 190 };

// 생물 리스트
let creatures = [];

// 어종 속성 정의
const SPECIES_DATA = {
  GUPPY: { name: '구피', env: 'FRESH', color: '#ffb703', size: 3, poopType: 1 }, // 1: 얇은 실똥
  TETRA: { name: '네온테트라', env: 'FRESH', color: '#00b4d8', size: 3, poopType: 2 }, // 2: 작은 점똥
  SEAGULL: { name: '체리새우', env: 'FRESH', color: '#e63946', size: 2, poopType: 2 },
  TURTLE_SEMI: { name: '반수생거북', env: 'FRESH', color: '#2a9d8f', size: 6, poopType: 3 }, // 3: 굵은 알갱이똥
  CLOWN: { name: '크라운피쉬', env: 'SALT', color: '#fb8500', size: 4, poopType: 1 },
  BLUETANG: { name: '블루탱', env: 'SALT', color: '#03045e', size: 4, poopType: 1 },
  PUFFER: { name: '복어', env: 'SALT', color: '#e9c46a', size: 5, poopType: 3 },
  TURTLE_SEA: { name: '바다거북', env: 'SALT', color: '#118ab2', size: 8, poopType: 3 }
};

// 어항 환경 변경
function setTankEnv(env) {
  tankEnv = env;
  document.getElementById('btn-env-fresh').classList.toggle('active', env==='FRESH');
  document.getElementById('btn-env-salt').classList.toggle('active', env==='SALT');
  
  const badge = document.getElementById('env-badge');
  if(env === 'FRESH') {
    badge.className = 'badge badge-fresh';
    badge.innerText = '담수 어항';
  } else {
    badge.className = 'badge badge-salt';
    badge.innerText = '해수 어항';
  }
}

function setCategory(cat) {
  currentCategory = cat;
  document.querySelectorAll('#sidebar .mode-btn-group button').forEach(b => b.classList.remove('active'));
  document.getElementById('section-powder').style.display = cat === 'POWDER' ? 'block' : 'none';
  document.getElementById('section-creature').style.display = cat === 'CREATURE' ? 'block' : 'none';
  document.getElementById('section-equip').style.display = cat === 'EQUIP' ? 'block' : 'none';
}

function setTool(tool) {
  currentTool = tool;
  document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

function clearTank() {
  for(let y=0; y<HEIGHT; y++) {
    grid[y].fill(0);
    poopTypeGrid[y].fill(0);
  }
  creatures = [];
}

// 생물 클래스
class Creature {
  constructor(type, x, y) {
    this.type = type;
    this.info = SPECIES_DATA[type];
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 0.8;
    this.vy = (Math.random() - 0.5) * 0.5;
    this.fullness = 80; // 포만감
    this.health = 100;
    this.digestTimer = 0;
  }

  update() {
    // 1. 환경 체크 (담수/해수 불일치 시 체력 감소)
    if (this.info.env !== tankEnv) {
      this.health -= 0.15; //
