import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="나만의 픽셀 어항 Sandbox", layout="wide")

st.title("🐠 나만의 픽셀 어항 Sandbox (업그레이드 버전)")
st.caption("담수/해수 구분, 포만감 밸런스, 어종별 맞춤 똥, 수초 씨앗 발아, 기포기 위치 변경 지원")

html_content = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body { background-color: #0b132b; color: #ffffff; font-family: sans-serif; display: flex; height: 100vh; overflow: hidden; }
  
  #sidebar { width: 300px; background-color: #1c2541; padding: 15px; display: flex; flex-direction: column; gap: 12px; overflow-y: auto; border-right: 2px solid #3a506b; }
  h2 { font-size: 14px; color: #4cc9f0; margin-bottom: 6px; border-bottom: 1px solid #3a506b; padding-bottom: 4px; }
  
  .mode-btn-group { display: flex; gap: 4px; }
  .mode-btn { flex: 1; padding: 7px 4px; background-color: #3a506b; border: none; color: white; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 11px; }
  .mode-btn.active { background-color: #4cc9f0; color: #0b132b; }
  
  .tool-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; }
  .tool-btn { padding: 7px 5px; background-color: #0b132b; border: 1px solid #3a506b; color: #e0e1dd; border-radius: 4px; cursor: pointer; font-size: 11px; text-align: left; }
  .tool-btn.active { border-color: #4cc9f0; background-color: #1c2541; color: #4cc9f0; font-weight: bold; }
  
  .setting-item { display: flex; flex-direction: column; gap: 4px; font-size: 12px; }
  input[type="range"] { width: 100%; }
  
  #main-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: #000814; }
  canvas { border: 2px solid #4cc9f0; border-radius: 8px; cursor: crosshair; box-shadow: 0 0 15px rgba(76, 201, 240, 0.2); }
  
  #status-bar { position: absolute; top: 15px; left: 50%; transform: translateX(-50%); background: rgba(11, 19, 43, 0.85); padding: 6px 16px; border-radius: 20px; border: 1px solid #4cc9f0; display: flex; gap: 12px; font-size: 12px; font-weight: bold; }
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
      <button class="mode-btn active" id="cat-powder" onclick="setCategory('POWDER')">파우더</button>
      <button class="mode-btn" id="cat-creature" onclick="setCategory('CREATURE')">생물</button>
      <button class="mode-btn" id="cat-equip" onclick="setCategory('EQUIP')">장비</button>
    </div>
  </div>

  <div id="section-powder">
    <h2>⏳ 파우더 / 씨앗 / 먹이</h2>
    <div class="tool-grid">
      <button class="tool-btn active" onclick="setTool('SAND', this)">🌾 금사 모래</button>
      <button class="tool-btn" onclick="setTool('SOIL', this)">🤎 영양 소일</button>
      <button class="tool-btn" onclick="setTool('ROCK', this)">🪨 고정 암석</button>
      <button class="tool-btn" onclick="setTool('WOOD', this)">🪵 고정 유목</button>
      <button class="tool-btn" onclick="setTool('SEED', this)">🌱 수초 씨앗</button>
      <button class="tool-btn" onclick="setTool('FOOD', this)">🟡 먹이 입자</button>
      <button class="tool-btn" onclick="setTool('ERASER', this)">🧹 청소/지우개</button>
    </div>
  </div>

  <div id="section-creature" style="display:none;">
    <h2>🐟 어종 & 생물</h2>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('GUPPY', this)">🐟 구피 (담수)</button>
      <button class="tool-btn" onclick="setTool('TETRA', this)">💙 네온테트라(담수)</button>
      <button class="tool-btn" onclick="setTool('SHRIMP', this)">🦐 체리새우 (담수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEMI', this)">🐢 반수생거북(담수)</button>
      <button class="tool-btn" onclick="setTool('CLOWN', this)">🧡 크라운피쉬(해수)</button>
      <button class="tool-btn" onclick="setTool('BLUETANG', this)">💙 블루탱 (해수)</button>
      <button class="tool-btn" onclick="setTool('PUFFER', this)">🐡 복어 (해수)</button>
      <button class="tool-btn" onclick="setTool('TURTLE_SEA', this)">🐢 바다거북 (해수)</button>
    </div>
  </div>

  <div id="section-equip" style="display:none;">
    <h2>🫧 어항 장비</h2>
    <div class="tool-grid">
      <button class="tool-btn" onclick="setTool('BUBBLER_MOVE', this)">🫧 기포기 위치 변경</button>
    </div>
  </div>

  <div>
    <h2>⚙️ 브러시 크기</h2>
    <div class="setting-item">
      <input type="range" id="brush-size" min="1" max="8" value="3" onchange="brushSize = parseInt(this.value)">
    </div>
  </div>
  
  <div style="margin-top:auto;">
    <button class="mode-btn" style="background:#e63946; width:100%;" onclick="clearTank()">🗑️ 전체 비우기</button>
  </div>
</div>

<div id="main-container">
  <div id="status-bar">
    <span id="env-badge" class="badge badge-fresh">담수 어항</span>
    <span>🌡️ 수온: 25°C</span>
    <span>💧 수질: 100%</span>
    <span>🐠 생물: <span id="txt-count">0</span>마리</span>
  </div>
  <canvas id="sandCanvas" width="600" height="400"></canvas>
</div>

<script>
var WIDTH = 300;
var HEIGHT = 200;
var SCALE = 2;

var canvas = document.getElementById('sandCanvas');
var ctx = canvas.getContext('2d');

var grid = Array.from({length: HEIGHT}, function() { return new Uint8Array(WIDTH); });
var poopTypeGrid = Array.from({length: HEIGHT}, function() { return new Uint8Array(WIDTH); });

var tankEnv = 'FRESH';
var currentTool = 'SAND';
var brushSize = 3;

var bubblerPos = { x: 150, y: 190 };
var creatures = [];

var SPECIES_DATA = {
  GUPPY: { name: '구피', env: 'FRESH', color: '#ffb703', size: 3, poopType: 1 },
  TETRA: { name: '네온테트라', env: 'FRESH', color: '#00b4d8', size: 3, poopType: 2 },
  SHRIMP: { name: '체리새우', env: 'FRESH', color: '#e63946', size: 2, poopType: 2 },
  TURTLE_SEMI: { name: '반수생거북', env: 'FRESH', color: '#2a9d8f', size: 6, poopType: 3 },
  CLOWN: { name: '크라운피쉬', env: 'SALT', color: '#fb8500', size: 4, poopType: 1 },
  BLUETANG: { name: '블루탱', env: 'SALT', color: '#03045e', size: 4, poopType: 1 },
  PUFFER: { name: '복어', env: 'SALT', color: '#e9c46a', size: 5, poopType: 3 },
  TURTLE_SEA: { name: '바다거북', env: 'SALT', color: '#118ab2', size: 8, poopType: 3 }
};

function setTankEnv(env) {
  tankEnv = env;
  document.getElementById('btn-env-fresh').classList.toggle('active', env==='FRESH');
  document.getElementById('btn-env-salt').classList.toggle('active', env==='SALT');
  
  var badge = document.getElementById('env-badge');
  if(env === 'FRESH') {
    badge.className = 'badge badge-fresh';
    badge.innerText = '담수 어항';
  } else {
    badge.className = 'badge badge-salt';
    badge.innerText = '해수 어항';
  }
}

function setCategory(cat) {
  document.getElementById('cat-powder').classList.toggle('active', cat==='POWDER');
  document.getElementById('cat-creature').classList.toggle('active', cat==='CREATURE');
  document.getElementById('cat-equip').classList.toggle('active', cat==='EQUIP');

  document.getElementById('section-powder').style.display = cat === 'POWDER' ? 'block' : 'none';
  document.getElementById('section-creature').style.display = cat === 'CREATURE' ? 'block' : 'none';
  document.getElementById('section-equip').style.display = cat === 'EQUIP' ? 'block' : 'none';
}

function setTool(tool, btn) {
  currentTool = tool;
  var btns = document.querySelectorAll('.tool-btn');
  btns.forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
}

function clearTank() {
  for(var y=0; y<HEIGHT; !="=" (this.fullness (this.info.env * -="0.008;" 0) 0.5) 0.5; 0.8; < Creature(type, Creature.prototype.update="function()" creatures="[];" function grid[y].fill(0); if poopTypeGrid[y].fill(0); tankEnv) this.digestTimer="0;" this.fullness="0;" this.health this.info="SPECIES_DATA[type];" this.type="type;" this.vx="(Math.random()" this.vy="(Math.random()" this.x="x;" this.y="y;" x, y) y++) { }> 40) {
    this.digestTimer += 1;
    if (this.digestTimer > 500) {
      this.poop();
      this.digestTimer = 0;
      this.fullness -= 8;
    }
  }

  if (this.fullness < 90) {
    this.findFood();
  }

  this.x += this.vx;
  this.y += this.vy;

  if (this.x < 10 || this.x > WIDTH - 10) this.vx *= -1;
  if (this.y < 10 || this.y > HEIGHT - 20) this.vy *= -1;

  if (Math.random() < 0.02) {
    this.vx += (Math.random() - 0.5) * 0.3;
    this.vy += (Math.random() - 0.5) * 0.2;
    this.vx = Math.max(-1, Math.min(1, this.vx));
    this.vy = Math.max(-0.6, Math.min(0.6, this.vy));
  }
};

Creature.prototype.findFood = function() {
  var cx = Math.floor(this.x);
  var cy = Math.floor(this.y);
  for (var dy = -4; dy <= 4; dy++) {
    for (var dx = -4; dx <= 4; dx++) {
      var nx = cx + dx;
      var ny = cy + dy;
      if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
        if (grid[ny][nx] === 7) {
          grid[ny][nx] = 0;
          this.fullness = Math.min(100, this.fullness + 5);
          return;
        }
      }
    }
  }
};

Creature.prototype.poop = function() {
  var px = Math.floor(this.x);
  var py = Math.floor(this.y) + 2;
  if (px >= 0 && px < WIDTH && py >= 0 && py < HEIGHT) {
    grid[py][px] = 8;
    poopTypeGrid[py][px] = this.info.poopType;
  }
};

Creature.prototype.draw = function() {
  ctx.fillStyle = this.info.color;
  var s = this.info.size;

  if (this.type === 'TURTLE_SEMI' || this.type === 'TURTLE_SEA') {
    ctx.fillRect((this.x - s/2)*SCALE, (this.y - s/2)*SCALE, s*SCALE, (s*0.7)*SCALE);
    ctx.fillStyle = '#1b4332';
    var headOffset = this.vx > 0 ? s/3 : -s/2;
    ctx.fillRect((this.x + headOffset)*SCALE, (this.y - s/3)*SCALE, (s/2)*SCALE, (s/2)*SCALE);
  } else {
    ctx.fillRect((this.x - s/2)*SCALE, (this.y - s/2)*SCALE, s*SCALE, (s/2)*SCALE);
  }

  if (this.info.env !== tankEnv) {
    ctx.strokeStyle = '#e63946';
    ctx.lineWidth = 1;
    ctx.strokeRect((this.x - s)*SCALE, (this.y - s)*SCALE, (s*2)*SCALE, (s*2)*SCALE);
  }
};

var isMouseDown = false;

canvas.addEventListener('mousedown', function(e) { isMouseDown = true; handleInput(e); });
canvas.addEventListener('mousemove', function(e) { if(isMouseDown) handleInput(e); });
canvas.addEventListener('mouseup', function() { isMouseDown = false; });

function handleInput(e) {
  var rect = canvas.getBoundingClientRect();
  var mx = Math.floor((e.clientX - rect.left) / SCALE);
  var my = Math.floor((e.clientY - rect.top) / SCALE);

  if (mx < 0 || mx >= WIDTH || my < 0 || my >= HEIGHT) return;

  if (currentTool === 'BUBBLER_MOVE') {
    bubblerPos = { x: mx, y: my };
    return;
  }

  if (SPECIES_DATA[currentTool]) {
    if (isMouseDown && e.type === 'mousedown') {
      creatures.push(new Creature(currentTool, mx, my));
    }
    return;
  }

  for (var dy = -brushSize; dy <= brushSize; dy++) {
    for (var dx = -brushSize; dx <= brushSize; dx++) {
      var nx = mx + dx;
      var ny = my + dy;
      if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT) {
        if (currentTool === 'SAND') grid[ny][nx] = 1;
        else if (currentTool === 'SOIL') grid[ny][nx] = 2;
        else if (currentTool === 'ROCK') grid[ny][nx] = 3;
        else if (currentTool === 'WOOD') grid[ny][nx] = 4;
        else if (currentTool === 'SEED') {
          if (grid[ny][nx] === 0) grid[ny][nx] = 5;
        }
        else if (currentTool === 'FOOD') grid[ny][nx] = 7;
        else if (currentTool === 'ERASER') {
          grid[ny][nx] = 0;
          poopTypeGrid[ny][nx] = 0;
        }
      }
    }
  }
}

function updatePhysics() {
  for (var y = HEIGHT - 2; y >= 0; y--) {
    for (var x = 0; x < WIDTH; x++) {
      var type = grid[y][x];

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
        var under = grid[y + 1] ? grid[y + 1][x] : 0;
        if (under === 1 || under === 2 || under === 3 || under === 4 || under === 6) {
          if (Math.random() < 0.05) {
            grid[y][x] = 6;
            if (y > 10 && Math.random() < 0.7) grid[y - 1][x] = 5;
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

  ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
  for (var i = 0; i < 3; i++) {
    var bx = bubblerPos.x + (Math.random() - 0.5) * 6;
    var by = bubblerPos.y - Math.random() * 20;
    ctx.fillRect(bx * SCALE, by * SCALE, 2, 2);
  }

  ctx.fillStyle = '#8d99ae';
  ctx.fillRect((bubblerPos.x - 4) * SCALE, bubblerPos.y * SCALE, 8 * SCALE, 4 * SCALE);

  for (var y = 0; y < HEIGHT; y++) {
    for (var x = 0; x < WIDTH; x++) {
      var t = grid[y][x];
      if (t === 0) continue;

      if (t === 1) ctx.fillStyle = '#e9c46a';
      else if (t === 2) ctx.fillStyle = '#6b705c';
      else if (t === 3) ctx.fillStyle = '#4a4e69';
      else if (t === 4) ctx.fillStyle = '#a5a58d';
      else if (t === 5) ctx.fillStyle = '#52b788';
      else if (t === 6) ctx.fillStyle = '#2b9348';
      else if (t === 7) ctx.fillStyle = '#ffb703';
      else if (t === 8) {
        var pt = poopTypeGrid[y][x];
        if (pt === 1) ctx.fillStyle = '#3d2612';
        else if (pt === 2) ctx.fillStyle = '#5c3d11';
        else ctx.fillStyle = '#281808';
      }
      ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
    }
  }

  for (var j = creatures.length - 1; j >= 0; j--) {
    var c = creatures[j];
    c.update();
    c.draw();
    if (c.health <= 0) {
      creatures.splice(j, 1);
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

components.html(html_content, height=520)
