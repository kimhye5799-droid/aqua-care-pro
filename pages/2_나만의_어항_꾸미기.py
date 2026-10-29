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
  body { background-color: #050a14; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; height: 100vh; overflow: hidden; }
  
  /* 왼쪽 패널 */
  #sidebar { width: 280px; background-color: #0b1528; padding: 12px; display: flex; flex-direction: column; gap: 10px; overflow-y: auto; border-right: 1px solid #1e2d42; }
  .panel-title { font-size: 13px; font-weight: bold; color: #4cc9f0; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
  
  .mode-btn-group { display: flex; gap: 4px; }
  .mode-btn { flex: 1; padding: 8px 4px; background-color: #121f35; border: 1px solid #1e2d42; color: #8d99ae; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: bold; }
  .mode-btn.active { background-color: #0077b6; color: #ffffff; border-color: #4cc9f0; }
  
  .tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .tool-btn { padding: 8px 6px; background-color: #121f35; border: 1px solid #1e2d42; color: #d8f3dc; border-radius: 4px; cursor: pointer; font-size: 11px; text-align: left; display: flex; align-items: center; gap: 4px; }
  .tool-btn.active { border-color: #4cc9f0; background-color: #1e2d42; color: #4cc9f0; font-weight: bold; box-shadow: 0 0 5px rgba(76,201,240,0.3); }
  
  .slider-box { display: flex; flex-direction: column; gap: 4px; background: #121f35; padding: 8px; border-radius: 4px; border: 1px solid #1e2d42; }
  .slider-label { font-size: 11px; color: #a8dadc; display: flex; justify-content: space-between; }
  input[type="range"] { width: 100%; accent-color: #4cc9f0; cursor: pointer; }
  
  /* 중앙 어항 및 상단 바 */
  #main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: #02050b; padding: 10px; }
  canvas { border: 2px solid #00b4d8; border-radius: 12px; cursor: crosshair; box-shadow: 0 0 25px rgba(0, 180, 216, 0.25); background: #000814; }
  
  #status-bar { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); background: rgba(11, 21, 40, 0.9); padding: 6px 18px; border-radius: 20px; border: 1px solid #00b4d8; display: flex; gap: 15px; font-size: 12px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
  
  /* 오른쪽 패널 (휴지통/풀어주기) */
  #right-panel { width: 100px; background-color: #0b1528; padding: 12px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; border-left: 1px solid #1e2d42; }
  .trash-box { width: 100%; height: 120px; border: 2px dashed #e63946; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #e63946; font-size: 11px; gap: 6px; cursor: pointer; }
  .trash-box:hover { background: rgba(230, 57, 70, 0.1); }
  
  .bottom-actions { display: flex; gap: 6px; margin-top: auto; }
  .act-btn { padding: 8px; border: none; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer; color: white; }
  .btn-reset { background: #e63946; }
  .btn-clean { background: #457b9d; }
</style>
</head>
<body>

<!-- 왼쪽 제어판 -->
<div id="sidebar">
  <div>
    <div class="panel-title">🌊 어항 서식 환경 선택</div>
    <div class="mode-btn-group">
      <button class="mode-btn active" id="btn-fresh" onclick="setTankEnv('FRESH')">🌿 담수 어항</button>
      <button class="mode-btn" id="btn-salt" onclick="setTankEnv('SALT')">🪸 해수 어항</button>
    </div>
  </div>

  <div>
    <div class="panel-title">🛠️ 도구 카테고리</div>
    <div class="mode-btn-group">
      <button class="mode-btn active" id="tab-powder" onclick="setCategory('POWDER')">파우더 모드</button>
      <button class="mode-btn" id="tab-creature" onclick="setCategory('CREATURE')">생물 모드</button>
      <button class="mode-btn" id="tab-equip" onclick="setCategory('EQUIP')">장비 모드</button>
    </div>
  </div>

  <div class="slider-box">
    <div class="slider-label"><span>✏️ 브러시 크기</span><span id="brush-val">3 px</span></div>
    <input type="range" id="brush-size" min="1" max="10" value="3" oninput="brushSize=parseInt(this.value); document.getElementById('brush-val').innerText=this.value+' px';">
  </div>

  <!-- 파우더 모드 메뉴 -->
  <div id="sec-powder">
    <div class="panel-title">🧪 상호작용 펜 & 바닥재</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('SELECT', this)">🔍 개체 선택펜</button>
      <button class="tool-btn" onclick="setTool('ERASER_ALL', this)">🧹 만능 지우개</button>
      <button class="tool-btn" onclick="setTool('DEL_PIXEL', this)">🧹 픽셀 삭제펜</button>
      <button class="tool-btn" onclick="setTool('MOVE', this)">✋ 개체 이동펜</button>
      <button class="tool-btn active" onclick="setTool('SAND', this)">🟨 금사 모래</button>
      <button class="tool-btn" onclick="setTool('SOIL', this)">🤎 영양 소일</button>
      <button class="tool-btn" onclick="setTool('ROCK', this)">🪨 고정 암석</button>
      <button class="tool-btn" onclick="setTool('WOOD', this)">🪵 고정 유목</button>
      <button class="tool-btn" onclick="setTool('SEED', this)">🌱 수초 씨앗</button>
      <button class="tool-btn" onclick="setTool('FOOD', this)">🟡 먹이 입자</button>
    </div>
  </div>

  <!-- 생물 모드 메뉴 -->
  <div id="sec-creature" style="display:none;">
    <div class="panel-title">🐟 어종 및 생물 선택</div>
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

  <!-- 장비 모드 메뉴 -->
  <div id="sec-equip" style="display:none;">
    <div class="panel-title">🫧 어항 장비 설치</div>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('BUBBLER_MOVE', this)">🫧 기포기 위치 이동</button>
    </div>
  </div>

  <div class="slider-box">
    <div class="panel-title">🌡️ 수온 설정</div>
    <div class="slider-label"><span>어항 온도</span><span id="temp-val">24°C</span></div>
    <input type="range" min="18" max="32" value="24" oninput="document.getElementById('temp-val').innerText=this.value+'°C'; document.getElementById('txt-temp').innerText=this.value;">
  </div>

  <div class="bottom-actions">
    <button class="act-btn btn-clean" style="flex:1;" onclick="cleanPoop()">🧹 똥 청소</button>
    <button class="act-btn btn-reset" style="flex:1;" onclick="clearTank()">🔄 전체 비우기</button>
  </div>
</div>

<!-- 중앙 대형 어항 메인 -->
<div id="main-container">
  <div id="status-bar">
    <span id="txt-env" style="color:#4cc9f0;">🌿 담수 어항</span>
    <span>🌡️ 수온: <span id="txt-temp">24</span>°C</span>
    <span>💧 수질: <span id="txt-quality">100</span>%</span>
    <span>🐠 개체수: <span id="txt-count">0</span></span>
  </div>
  <!-- 1000x650 대형 어항 Canvas -->
  <canvas id="sandCanvas" width="1000" height="650"></canvas>
</div>

<!-- 오른쪽 패널 -->
<div id="right-panel">
  <div class="trash-box" onclick="clearTank()">
    <span style="font-size:24px;">🗑️</span>
    <span>물체 버리기</span>
    <span style="font-size:9px; color:#8d99ae;">(클릭시 전체)</span>
  </div>
  <button class="act-btn" style="background:#0077b6; width:100%; padding:10px 4px;" onclick="addRandomCreature()">🔄 풀어주기</button>
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

let bubblerPos = { x: 250, y: 310 };
let creatures = [];

const SPECIES_DATA = {
  GUPPY: { name: '구피', env: 'FRESH', color: '#ffb703', size: 6, poopType: 1 },
  TETRA: { name: '네온테트라', env: 'FRESH', color: '#00b4d8', size: 5, poopType: 2 },
  SHRIMP: { name: '체리새우', env: 'FRESH', color: '#e63946', size: 4, poopType: 2 },
  TURTLE_SEMI: { name: '반수생거북', env: 'FRESH', color: '#2a9d8f', size: 12, poopType: 3 },
  CLOWN: { name: '크라운피쉬', env: 'SALT', color: '#fb8500', size: 7, poopType: 1 },
  BLUETANG: { name: '블루탱', env: 'SALT', color: '#03045e', size: 8, poopType: 1 },
  PUFFER: { name: '복어', env: 'SALT', color: '#e9c46a', size: 9, poopType: 3 },
  TURTLE_SEA: { name: '바다거북', env: 'SALT', color: '#118ab2', size: 16, poopType: 3 }
};

function setTankEnv(env) {
  tankEnv = env;
  document.getElementById('btn-fresh').classList.toggle('active', env === 'FRESH');
  document.getElementById('btn-salt').classList.toggle('active', env === 'SALT');
  document.getElementById('txt-env').innerText = env === 'FRESH' ? '🌿 담수 어항' : '🪸 해수 어항';
  document.getElementById('txt-env').style.color = env === 'FRESH' ? '#2a9d8f' : '#e76f51';
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
  creatures.push(new Creature(randomKey, Math.random() * (WIDTH - 40) + 20, Math.random() * (HEIGHT - 60) + 20));
}

class Creature {
  constructor(type, x, y) {
    this.type = type;
    this.info = SPECIES_DATA[type];
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 1.2;
    this.vy = (Math.random() - 0.5) * 0.8;
    this.fullness = 80;
    this.health = 100;
    this.digestTimer = 0;
  }

  update() {
    if (this.info.env !== tankEnv) {
      this.health -= 0.12;
    }

    this.fullness -= 0.005;
    if (this.fullness < 0) this.fullness = 0;

    if (this.fullness > 40) {
      this.digestTimer += 1;
      if (this.digestTimer > 600) {
        this.poop();
        this.digestTimer = 0;
        this.fullness -= 6;
      }
    }

    if (this.fullness < 90) {
      this.findFood();
    }

    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 15 || this.x > WIDTH - 15) this.vx *= -1;
    if (this.y < 15 || this.y > HEIGHT - 30) this.vy *= -1;

    if (Math.random() < 0.02) {
      this.vx += (Math.random() - 0.5) * 0.4;
      this.vy += (Math.random() - 0.5) * 0.3;
      this.vx = Math.max(-1.5, Math.min(1.5, this.vx));
      this.vy = Math.max(-1.0, Math.min(1.0, this.vy));
    }
  }

  findFood() {
    let cx = Math.floor(this.x);
    let cy = Math.floor(this.y);
    for (let dy = -6; dy <= 6; dy++) {
      for (let dx = -6; dx <= 6; dx++) {
        let nx = cx + dx;
        let ny = cy + dy;
        if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
          if (grid[ny][nx] === 7) {
            grid[ny][nx] = 0;
            this.fullness = Math.min(100, this.fullness + 4);
            return;
          }
        }
      }
    }
  }

  poop() {
    let px = Math.floor(this.x);
    let py = Math.floor(this.y) + 3;
    if (px >= 0 && px < WIDTH && py >= 0 && py < HEIGHT) {
      grid[py][px] = 8;
      poopTypeGrid[py][px] = this.info.poopType;
    }
  }

  draw() {
    ctx.fillStyle = this.info.color;
    let s = this.info.size;

    if (this.type === 'TURTLE_SEMI' || this.type === 'TURTLE_SEA') {
      ctx.fillRect((this.x - s/2)*SCALE, (this.y - s/2)*SCALE, s*SCALE, (s*0.6)*SCALE);
      ctx.fillStyle = '#1b4332';
      let hx = this.vx > 0 ? (this.x + s/3) : (this.x - s/1.5);
      ctx.fillRect(hx*SCALE, (this.y - s/3)*SCALE, (s/2)*SCALE, (s/2)*SCALE);
    } else {
      ctx.fillRect((this.x - s/2)*SCALE, (this.y - s/2)*SCALE, s*SCALE, (s/2)*SCALE);
    }

    if (this.info.env !== tankEnv) {
      ctx.strokeStyle = '#e63946';
      ctx.lineWidth = 1.5;
      ctx.strokeRect((this.x - s)*SCALE, (this.y - s)*SCALE, (s*2)*SCALE, (s*2)*SCALE);
    }
  }
}

let isMouseDown = false;

canvas.addEventListener('mousedown', e => { isMouseDown = true; handleInput(e); });
canvas.addEventListener('mousemove', e => { if (isMouseDown) handleInput(e); });
canvas.addEventListener('mouseup', () => isMouseDown = false);

function handleInput(e) {
  const rect = canvas.getBoundingClientRect();
  const mx = Math.floor((e.clientX - rect.left) / SCALE);
  const my = Math.floor((e.clientY - rect.top) / SCALE);

  if (mx < 0 || mx >= WIDTH || my < 0 || my >= HEIGHT) return;

  if (currentTool === 'BUBBLER_MOVE') {
    bubblerPos = { x: mx, y: my };
    return;
  }

  if (SPECIES_DATA[currentTool]) {
    if (e.type === 'mousedown') {
      creatures.push(new Creature(currentTool, mx, my));
    }
    return;
  }

  for (let dy = -brushSize; dy <= brushSize; dy++) {
    for (let dx = -brushSize; dx <= brushSize; dx++) {
      let nx = mx + dx;
      let ny = my + dy;
      if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
        if (currentTool === 'SAND') grid[ny][nx] = 1;
        else if (currentTool === 'SOIL') grid[ny][nx] = 2;
        else if (currentTool === 'ROCK') grid[ny][nx] = 3;
        else if (currentTool === 'WOOD') grid[ny][nx] = 4;
        else if (currentTool === 'SEED') {
          if (grid[ny][nx] === 0) grid[ny][nx] = 5;
        }
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

      if (type === 5) {
        let under = grid[y + 1] ? grid[y + 1][x] : 0;
        if ([1, 2, 3, 4, 6].includes(under)) {
          if (Math.random() < 0.04) {
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

  ctx.fillStyle = tankEnv === 'FRESH' ? '#001829' : '#000b1e';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
  for (let i = 0; i < 4; i++) {
    let bx = bubblerPos.x + (Math.random() - 0.5) * 8;
    let by = bubblerPos.y - Math.random() * 30;
    ctx.fillRect(bx * SCALE, by * SCALE, 2, 2);
  }

  ctx.fillStyle = '#8d99ae';
  ctx.fillRect((bubblerPos.x - 6) * SCALE, bubblerPos.y * SCALE, 12 * SCALE, 6 * SCALE);

  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      let t = grid[y][x];
      if (t === 0) continue;

      if (t === 1) ctx.fillStyle = '#e9c46a';
      else if (t === 2) ctx.fillStyle = '#6b705c';
      else if (t === 3) ctx.fillStyle = '#4a4e69';
      else if (t === 4) ctx.fillStyle = '#a5a58d';
      else if (t === 5) ctx.fillStyle = '#52b788';
      else if (t === 6) ctx.fillStyle = '#2b9348';
      else if (t === 7) ctx.fillStyle = '#ffb703';
      else if (t === 8) {
        let pt = poopTypeGrid[y][x];
        if (pt === 1) ctx.fillStyle = '#3d2612';
        else if (pt === 2) ctx.fillStyle = '#5c3d11';
        else ctx.fillStyle = '#281808';
      }
      ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
    }
  }

  for (let i = creatures.length - 1; i >= 0; i--) {
    let c = creatures[i];
    c.update();
    c.draw();
    if (c.health <= 0) {
      creatures.splice(i, 1);
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
