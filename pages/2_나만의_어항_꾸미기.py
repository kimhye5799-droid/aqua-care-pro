import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="나만의 어항 꾸미기",
    page_icon="🐠",
    layout="wide"
)

st.title("🐠 프리미엄 수조 생태계 시뮬레이터")
st.caption("새로운 UI 디자인, 펜 크기 조절, 정교해진 생물 AI 및 물리 엔진으로 완벽한 어항을 꾸며보세요!")

aquarium_simulation_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Pretendard', 'Malgun Gothic', -apple-system, sans-serif;
            background-color: #0b1120;
            color: #f1f5f9;
            margin: 0;
            padding: 12px;
        }

        .app-container {
            display: flex;
            flex-direction: row;
            gap: 18px;
            width: 100%;
            max-width: 1320px;
            margin: 0 auto;
            align-items: flex-start;
        }

        /* 왼쪽 컨트롤 패널 */
        .sidebar-panel {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 320px;
            max-height: 680px;
            overflow-y: auto;
            padding-right: 4px;
            flex-shrink: 0;
        }

        .sidebar-panel::-webkit-scrollbar {
            width: 5px;
        }
        .sidebar-panel::-webkit-scrollbar-track {
            background: #1e293b;
            border-radius: 4px;
        }
        .sidebar-panel::-webkit-scrollbar-thumb {
            background: #38bdf8;
            border-radius: 4px;
        }

        /* 상태 현황판 카드 */
        .dashboard-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 14px;
            border-radius: 14px;
            border: 1px solid #334155;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .stat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }

        .wqi-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: -0.3px;
        }

        .stat-details {
            font-size: 11px;
            color: #94a3b8;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            background-color: rgba(15, 23, 42, 0.6);
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-details b {
            color: #38bdf8;
            display: block;
            font-size: 13px;
            margin-top: 2px;
        }

        /* 도구 상자 */
        .toolbar {
            background-color: #1e293b;
            padding: 14px;
            border-radius: 14px;
            border: 1px solid #334155;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        /* 펜 크기 조절 슬라이더 */
        .brush-control {
            background: #0f172a;
            padding: 10px 12px;
            border-radius: 10px;
            border: 1px solid #334155;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .brush-label {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: 600;
            color: #38bdf8;
        }

        input[type=range] {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #334155;
            accent-color: #38bdf8;
            cursor: pointer;
        }

        .tool-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .category-label {
            font-size: 11px;
            font-weight: 700;
            color: #94a3b8;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border-bottom: 1px solid #334155;
            padding-bottom: 4px;
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
        }

        .btn {
            background-color: #0f172a;
            color: #e2e8f0;
            border: 1px solid #334155;
            padding: 8px 6px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            user-select: none;
        }

        .btn:hover {
            background-color: #334155;
            border-color: #38bdf8;
            color: #ffffff;
        }

        .btn.active {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
            border-color: #38bdf8 !important;
            color: #ffffff !important;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }

        .btn-action {
            background-color: #115e59;
            border-color: #14b8a6;
        }
        .btn-action:hover {
            background-color: #0f766e;
        }

        .btn-danger {
            background-color: #881337;
            border-color: #f43f5e;
        }
        .btn-danger:hover {
            background-color: #9f1239;
        }

        /* 오른쪽 어항 화면 */
        .aquarium-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .canvas-wrapper {
            position: relative;
            box-shadow: 0 20px 35px rgba(0, 0, 0, 0.7);
            border: 4px solid #334155;
            border-radius: 16px;
            overflow: hidden;
            background-color: #020617;
        }

        canvas {
            display: block;
            cursor: crosshair;
        }

        .guide-text {
            margin-top: 10px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="app-container">
        <!-- 1. 왼쪽 컨트롤 사이드바 -->
        <div class="sidebar-panel">
            <div class="dashboard-card">
                <div class="stat-header">
                    <span style="font-size: 13px; font-weight: 700;">💧 수질 종합 지수</span>
                    <div id="wqi-display" class="wqi-badge">100점 (최상)</div>
                </div>
                <div class="stat-details">
                    <div>💩 오염물<b id="waste-count">0</b></div>
                    <div>🌿 수초/이끼<b id="plant-count">0</b></div>
                    <div>🌀 설치 장치<b id="equip-count">0</b></div>
                </div>
            </div>

            <div class="toolbar">
                <!-- 펜 / 지우개 크기 조절 슬라이더 -->
                <div class="brush-control">
                    <div class="brush-label">
                        <span>✏️ 브러시/지우개 크기</span>
                        <span id="brush-val">6px</span>
                    </div>
                    <input type="range" id="brush-size" min="2" max="24" value="6">
                </div>

                <div class="tool-group">
                    <span class="category-label">① 지형 & 레이아웃</span>
                    <div class="btn-grid">
                        <button class="btn active" data-tool="sand_gold">🏖️ 금사</button>
                        <button class="btn" data-tool="sand_black">🖤 흑사</button>
                        <button class="btn" data-tool="gravel">🪨 강자갈</button>
                        <button class="btn" data-tool="volcanic_rock">🌋 화산석</button>
                        <button class="btn" data-tool="driftwood">🪵 유목(선)</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">② 수초 & 생장</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="plant_weed">🌿 기본수초</button>
                        <button class="btn" data-tool="moss">🟢 프리미엄이끼</button>
                        <button class="btn" data-tool="co2_bubble">🫧 CO2 버블</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">③ 생태 장치</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="air_bubble">🫧 산소기포기</button>
                        <button class="btn" data-tool="filter">🌀 걸이식여과기</button>
                        <button class="btn" data-tool="wave_maker">💨 수류생성기</button>
                        <button class="btn" data-tool="heater">🔥 온도조절히터</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">④ 수중 생물</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="guppy">🐠 구피</button>
                        <button class="btn" data-tool="neon_tetra">🐟 네온테트라</button>
                        <button class="btn" data-tool="puffer">🐡 미니복어</button>
                        <button class="btn" data-tool="angelfish">🐠 엔젤피쉬</button>
                        <button class="btn" data-tool="corydoras">🐟 코리도라스</button>
                        <button class="btn" data-tool="shrimp">🦐 체리새우</button>
                        <button class="btn" data-tool="snail">🐌 애플스네일</button>
                        <button class="btn" data-tool="turtle">🐢 미니거북이</button>
                        <button class="btn" data-tool="crab">🦀 체리게</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">⑤ 맞춤 먹이</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="food_fish">🟤 물고기사료</button>
                        <button class="btn" data-tool="food_shrimp">🟡 새우/저서사료</button>
                        <button class="btn" data-tool="food_green">🟢 영양스틱</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">⑥ 어항 관리</span>
                    <div class="btn-grid">
                        <button class="btn btn-action" data-tool="eraser">🧹 지우개</button>
                        <button class="btn btn-action" id="btn-water-change">🪣 환수하기</button>
                        <button class="btn btn-action" id="btn-conditioner">💊 박테리아제</button>
                        <button class="btn btn-danger" id="btn-reset">🔄 초기화</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 어항 메인 캔버스 -->
        <div class="aquarium-container">
            <div class="canvas-wrapper">
                <canvas id="aquarium" width="860" height="600"></canvas>
            </div>
            <div class="guide-text">💡 마우스 클릭 및 드래그로 원하는 지형과 수초를 자유롭게 그려보세요.</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('aquarium');
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // 입자 종류 정의
        const EMPTY = 0;
        const SAND_GOLD = 1;
        const SAND_BLACK = 2;
        const GRAVEL = 3;
        const VOLCANIC = 4;
        const DRIFTWOOD = 5;
        const PLANT = 6;
        const MOSS = 7;
        const CO2 = 8;
        const AIR = 9;
        const FOOD_FISH = 10;
        const FOOD_SHRIMP = 11;
        const FOOD_GREEN = 12;
        const WASTE = 13;

        const colors = {
            [SAND_GOLD]: [234, 179, 8],
            [SAND_BLACK]: [30, 41, 59],
            [GRAVEL]: [148, 163, 184],
            [VOLCANIC]: [120, 53, 15],
            [DRIFTWOOD]: [146, 64, 14],
            [PLANT]: [34, 197, 94],
            [MOSS]: [22, 101, 52],
            [CO2]: [186, 230, 253],
            [AIR]: [224, 242, 254],
            [FOOD_FISH]: [180, 83, 9],
            [FOOD_SHRIMP]: [234, 179, 8],
            [FOOD_GREEN]: [34, 197, 94],
            [WASTE]: [115, 115, 115]
        };

        const grid = new Uint8Array(width * height);
        const foodAge = new Uint16Array(width * height);

        let creatures = [];
        let equipments = [];
        let currentTool = 'sand_gold';
        let brushSize = 6;
        let isMouseDown = false;
        let lastX = null;
        let lastY = null;

        let currentWQI = 100;
        let targetWaterColor = [14, 165, 233, 0.15];
        let currentWaterColor = [14, 165, 233, 0.15];

        // 슬라이더 이벤트
        const brushSlider = document.getElementById('brush-size');
        const brushValDisp = document.getElementById('brush-val');
        brushSlider.addEventListener('input', (e) => {
            brushSize = parseInt(e.target.value);
            brushValDisp.innerText = brushSize + 'px';
        });

        function isSolidTile(x, y) {
            if (x < 0 || x >= width || y < 0 || y >= height) return true;
            const type = grid[Math.floor(y) * width + Math.floor(x)];
            return (type === SAND_GOLD || type === SAND_BLACK || type === GRAVEL || type === VOLCANIC || type === DRIFTWOOD);
        }

        function isLandableTile(x, y) {
            if (x < 0 || x >= width || y < 0 || y >= height) return true;
            const type = grid[Math.floor(y) * width + Math.floor(x)];
            return (type === SAND_GOLD || type === SAND_BLACK || type === GRAVEL || type === VOLCANIC || type === DRIFTWOOD || type === MOSS || type === PLANT);
        }

        document.querySelectorAll('.btn[data-tool]').forEach(btn => {
            btn.addEventListener('click', () => {
                currentTool = btn.getAttribute('data-tool');
                document.querySelectorAll('.btn[data-tool]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        document.getElementById('btn-water-change').addEventListener('click', () => {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE && Math.random() < 0.85) grid[i] = EMPTY;
            }
        });

        document.getElementById('btn-conditioner').addEventListener('click', () => {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE) grid[i] = EMPTY;
            }
        });

        document.getElementById('btn-reset').addEventListener('click', () => {
            grid.fill(EMPTY);
            foodAge.fill(0);
            creatures = [];
            equipments = [];
        });

        function applyBrushAt(cx, cy, toolId) {
            const r = brushSize;
            for (let dx = -r; dx <= r; dx++) {
                for (let dy = -r; dy <= r; dy++) {
                    const px = cx + dx;
                    const py = cy + dy;
                    if (px >= 0 && px < width && py >= 0 && py < height) {
                        if (dx*dx + dy*dy <= r*r) {
                            if (toolId === EMPTY) {
                                grid[py * width + px] = EMPTY;
                                foodAge[py * width + px] = 0;
                            } else {
                                grid[py * width + px] = toolId;
                                foodAge[py * width + px] = 0;
                            }
                        }
                    }
                }
            }
        }

        // 연속 브러시 (유목 선 그리기 지원)
        function drawLine(x0, y0, x1, y1, toolId) {
            const dx = Math.abs(x1 - x0);
            const dy = Math.abs(y1 - y0);
            const steps = Math.max(dx, dy, 1);
            for (let i = 0; i <= steps; i++) {
                const px = Math.round(x0 + (x1 - x0) * (i / steps));
                const py = Math.round(y0 + (y1 - y0) * (i / steps));
                applyBrushAt(px, py, toolId);
            }
        }

        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) * (canvas.width / rect.width));
            const y = Math.floor((e.clientY - rect.top) * (canvas.height / rect.height));

            if (x < 0 || x >= width || y < 0 || y >= height) return;

            // 생물 스폰
            const creatureConfig = {
                'guppy': { type: 'swim', emoji: '🐠', size: 24 },
                'neon_tetra': { type: 'swim', emoji: '🐟', size: 22 },
                'puffer': { type: 'swim', emoji: '🐡', size: 24 },
                'angelfish': { type: 'swim', emoji: '🐠', size: 28 },
                'turtle': { type: 'swim', emoji: '🐢', size: 28 },
                'corydoras': { type: 'bottom', emoji: '🐟', size: 22 },
                'shrimp': { type: 'bottom_climb', emoji: '🦐', size: 15 }, // 작은 크기
                'snail': { type: 'bottom_climb', emoji: '🐌', size: 17 },
                'crab': { type: 'bottom', emoji: '🦀', size: 20 }
            };

            if (creatureConfig[currentTool]) {
                if (isMouseDown && Math.random() < 0.15) {
                    const cfg = creatureConfig[currentTool];
                    creatures.push({
                        id: Date.now() + Math.random(),
                        category: cfg.type,
                        x: x,
                        y: y,
                        vx: (Math.random() - 0.5) * 1.5,
                        vy: (Math.random() - 0.5) * 1.0,
                        facing: 'right',
                        emoji: cfg.emoji,
                        size: cfg.size,
                        targetX: x,
                        targetY: y
                    });
                }
                return;
            }

            // 고정 장치 설치
            if (['filter', 'air_bubble', 'wave_maker', 'heater'].includes(currentTool)) {
                if (isMouseDown && Math.random() < 0.08) {
                    const emojiMap = { filter: '🌀', air_bubble: '🫧', wave_maker: '💨', heater: '🔥' };
                    equipments.push({ type: currentTool, x, y, emoji: emojiMap[currentTool] });
                }
                return;
            }

            const toolId = getToolId(currentTool);

            if (lastX !== null && lastY !== null) {
                drawLine(lastX, lastY, x, y, toolId);
            } else {
                applyBrushAt(x, y, toolId);
            }

            lastX = x;
            lastY = y;
        }

        function getToolId(tool) {
            switch(tool) {
                case 'sand_gold': return SAND_GOLD;
                case 'sand_black': return SAND_BLACK;
                case 'gravel': return GRAVEL;
                case 'volcanic_rock': return VOLCANIC;
                case 'driftwood': return DRIFTWOOD;
                case 'plant_weed': return PLANT;
                case 'moss': return MOSS;
                case 'co2_bubble': return CO2;
                case 'food_fish': return FOOD_FISH;
                case 'food_shrimp': return FOOD_SHRIMP;
                case 'food_green': return FOOD_GREEN;
                default: return EMPTY;
            }
        }

        canvas.addEventListener('mousedown', (e) => { 
            isMouseDown = true; 
            lastX = null; 
            lastY = null; 
            handlePointer(e); 
        });

        canvas.addEventListener('mousemove', (e) => { 
            if (isMouseDown) handlePointer(e); 
        });

        window.addEventListener('mouseup', () => { 
            isMouseDown = false; 
            lastX = null; 
            lastY = null; 
        });

        let deviceTimer = 0;
        function updateDevices() {
            deviceTimer++;
            if (deviceTimer % 6 === 0) {
                equipments.forEach(eq => {
                    if (eq.type === 'air_bubble') {
                        const idx = (eq.y - 10) * width + eq.x;
                        if (eq.y - 10 > 0) grid[idx] = AIR;
                    }
                });
            }
        }

        function updatePhysics() {
            for (let y = height - 2; y >= 0; y--) {
                for (let x = 0; x < width; x++) {
                    const idx = y * width + x;
                    const type = grid[idx];

                    if (type === EMPTY || type === VOLCANIC || type === DRIFTWOOD) continue;

                    if ([SAND_GOLD, SAND_BLACK, GRAVEL, FOOD_FISH, FOOD_SHRIMP, FOOD_GREEN, WASTE].includes(type)) {
                        const below = (y + 1) * width + x;
                        const belowLeft = (y + 1) * width + (x - 1);
                        const belowRight = (y + 1) * width + (x + 1);

                        if (grid[below] === EMPTY) {
                            grid[below] = type;
                            foodAge[below] = foodAge[idx];
                            grid[idx] = EMPTY;
                            foodAge[idx] = 0;
                        } else if (x > 0 && grid[belowLeft] === EMPTY) {
                            grid[belowLeft] = type;
                            foodAge[belowLeft] = foodAge[idx];
                            grid[idx] = EMPTY;
                            foodAge[idx] = 0;
                        } else if (x < width - 1 && grid[belowRight] === EMPTY) {
                            grid[belowRight] = type;
                            foodAge[belowRight] = foodAge[idx];
                            grid[idx] = EMPTY;
                            foodAge[idx] = 0;
                        }

                        if ([FOOD_FISH, FOOD_SHRIMP, FOOD_GREEN].includes(type)) {
                            foodAge[idx]++;
                            if (foodAge[idx] > 800) {
                                grid[idx] = WASTE;
                                foodAge[idx] = 0;
                            }
                        }
                    } else if (type === CO2 || type === AIR) {
                        const above = (y - 1) * width + x;
                        if (y > 0 && grid[above] === EMPTY) {
                            grid[above] = type;
                            grid[idx] = EMPTY;
                        } else {
                            grid[idx] = EMPTY;
                        }
                    }
                }
            }
        }

        function findClosestFood(x, y) {
            let closestDist = 999999;
            let target = null;

            for (let py = 10; py < height; py += 12) {
                for (let px = 10; px < width; px += 12) {
                    const type = grid[py * width + px];
                    if (type === FOOD_FISH || type === FOOD_SHRIMP || type === FOOD_GREEN) {
                        const dist = (px - x)**2 + (py - y)**2;
                        if (dist < closestDist) {
                            closestDist = dist;
                            target = { x: px, y: py };
                        }
                    }
                }
            }
            return target;
        }

        let wasteCount = 0;
        let plantCount = 0;

        function updateEcosystem() {
            wasteCount = 0;
            plantCount = 0;

            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE) wasteCount++;
                if (grid[i] === PLANT || grid[i] === MOSS) plantCount++;
            }

            const filterBonus = equipments.filter(e => e.type === 'filter').length * 15;
            const plantBonus = Math.floor(plantCount * 0.05);
            const wastePenalty = wasteCount * 2;

            let score = 100 - wastePenalty + filterBonus + plantBonus;
            currentWQI = Math.max(0, Math.min(100, score));

            const display = document.getElementById('wqi-display');
            document.getElementById('waste-count').innerText = wasteCount;
            document.getElementById('plant-count').innerText = plantCount;
            document.getElementById('equip-count').innerText = equipments.length;

            if (currentWQI >= 85) {
                targetWaterColor = [14, 165, 233, 0.15];
                display.style.backgroundColor = '#0284c7';
                display.style.color = '#ffffff';
                display.innerText = `${currentWQI}점 (최상)`;
            } else if (currentWQI >= 60) {
                targetWaterColor = [34, 197, 94, 0.25];
                display.style.backgroundColor = '#16a34a';
                display.style.color = '#ffffff';
                display.innerText = `${currentWQI}점 (보통)`;
            } else if (currentWQI >= 30) {
                targetWaterColor = [234, 179, 8, 0.35];
                display.style.backgroundColor = '#ca8a04';
                display.style.color = '#ffffff';
                display.innerText = `${currentWQI}점 (주의)`;
            } else {
                targetWaterColor = [185, 28, 28, 0.5];
                display.style.backgroundColor = '#dc2626';
                display.style.color = '#ffffff';
                display.innerText = `${currentWQI}점 (위험)`;
            }

            equipments.forEach(eq => {
                if (eq.type === 'filter') {
                    for (let dy = -30; dy <= 30; dy++) {
                        for (let dx = -30; dx <= 30; dx++) {
                            const fx = eq.x + dx;
                            const fy = eq.y + dy;
                            if (fx >= 0 && fx < width && fy >= 0 && fy < height) {
                                const fIdx = fy * width + fx;
                                if (grid[fIdx] === WASTE) grid[fIdx] = EMPTY;
                            }
                        }
                    }
                }
            });
        }

        // 생물 이동 및 절대 뒤로 헤엄치지 않는 AI
        function updateCreatures() {
            creatures.forEach(c => {
                const food = findClosestFood(c.x, c.y);

                if (c.category === 'swim') {
                    if (food) {
                        const dx = food.x - c.x;
                        const dy = food.y - c.y;
                        const dist = Math.sqrt(dx*dx + dy*dy);
                        if (dist > 5) {
                            c.vx += (dx / dist) * 0.12;
                            c.vy += (dy / dist) * 0.12;
                        }
                    } else {
                        if (Math.random() < 0.05) {
                            c.vx += (Math.random() - 0.5) * 0.6;
                            c.vy += (Math.random() - 0.5) * 0.4;
                        }
                    }

                    c.vx = Math.max(-2.2, Math.min(2.2, c.vx));
                    c.vy = Math.max(-1.4, Math.min(1.4, c.vy));

                } else if (c.category === 'bottom' || c.category === 'bottom_climb') {
                    // 바닥 생물 활발한 이동 및 정체 방지 AI
                    const onSolid = isLandableTile(c.x, c.y + 10) || c.y >= height - 20;

                    // 정체 방지 - 주기적으로 새로운 목적지 생성
                    if (Math.random() < 0.03 || Math.abs(c.vx) < 0.1) {
                        c.targetX = Math.max(30, Math.min(width - 30, c.x + (Math.random() - 0.5) * 220));
                        c.targetY = Math.max(40, Math.min(height - 30, c.y + (Math.random() - 0.5) * 120));
                    }

                    const tDx = (food ? food.x : c.targetX) - c.x;
                    const tDy = (food ? food.y : c.targetY) - c.y;
                    const tDist = Math.sqrt(tDx*tDx + tDy*tDy);

                    if (tDist > 4) {
                        c.vx += (tDx / tDist) * 0.15;
                        if (c.category === 'bottom_climb' || !onSolid) {
                            c.vy += (tDy / tDist) * 0.1;
                        }
                    }

                    if (!onSolid && c.category === 'bottom') {
                        c.vy += 0.2; // 중력 낙하
                    }

                    c.vx = Math.max(-1.6, Math.min(1.6, c.vx));
                    c.vy = Math.max(-1.2, Math.min(1.2, c.vy));
                }

                // 이동 방향에 따라 바라보는 정면 설정 (뒤로 가지 않음!)
                if (c.vx > 0.15) {
                    c.facing = 'right';
                } else if (c.vx < -0.15) {
                    c.facing = 'left';
                }

                let nextX = c.x + c.vx;
                let nextY = c.y + c.vy;

                // 지형 충돌 박스 (통과 금지)
                if (isSolidTile(nextX, nextY)) {
                    c.vx *= -0.7;
                    c.vy *= -0.7;
                } else {
                    c.x = nextX;
                    c.y = nextY;
                }

                // 벽 충돌
                if (c.x < 20) { c.x = 20; c.vx *= -1; c.facing = 'right'; }
                if (c.x > width - 20) { c.x = width - 20; c.vx *= -1; c.facing = 'left'; }
                if (c.y < 20) { c.y = 20; c.vy *= -1; }
                if (c.y > height - 20) { c.y = height - 20; c.vy = 0; }

                // 먹이 먹기
                const cx = Math.floor(c.x);
                const cy = Math.floor(c.y);
                for (let dy = -12; dy <= 12; dy++) {
                    for (let dx = -12; dx <= 12; dx++) {
                        const px = cx + dx;
                        const py = cy + dy;
                        if (px >= 0 && px < width && py >= 0 && py < height) {
                            const idx = py * width + px;
                            const type = grid[idx];
                            if (type === FOOD_FISH || type === FOOD_SHRIMP || type === FOOD_GREEN) {
                                grid[idx] = EMPTY;
                                foodAge[idx] = 0;
                            }
                        }
                    }
                }
            });
        }

        function lerp(start, end, amt) {
            return (1 - amt) * start + amt * end;
        }

        function updateWaterColor() {
            for (let i = 0; i < 4; i++) {
                currentWaterColor[i] = lerp(currentWaterColor[i], targetWaterColor[i], 0.02);
            }
        }

        function render() {
            ctx.clearRect(0, 0, width, height);

            // 1. 입자 렌더링
            const imgData = ctx.createImageData(width, height);
            const data = imgData.data;

            for (let i = 0; i < grid.length; i++) {
                const type = grid[i];
                if (type !== EMPTY) {
                    const rgb = colors[type];
                    const pixelIdx = i * 4;
                    data[pixelIdx] = rgb[0];
                    data[pixelIdx + 1] = rgb[1];
                    data[pixelIdx + 2] = rgb[2];
                    data[pixelIdx + 3] = 255;
                }
            }
            ctx.putImageData(imgData, 0, 0);

            // 2. 수질 물 레이어
            ctx.fillStyle = `rgba(${Math.round(currentWaterColor[0])}, ${Math.round(currentWaterColor[1])}, ${Math.round(currentWaterColor[2])}, ${currentWaterColor[3]})`;
            ctx.fillRect(0, 0, width, height);

            // 3. 설치된 장치
            equipments.forEach(eq => {
                ctx.font = '22px serif';
                ctx.fillText(eq.emoji, eq.x - 11, eq.y + 8);
            });

            // 4. 선명한 물고기 & 생물 렌더링 (투명도 0%, 또렷한 아웃라인 그림자)
            ctx.save();
            ctx.globalAlpha = 1.0;
            ctx.globalCompositeOperation = 'source-over';

            creatures.forEach(c => {
                ctx.save();
                ctx.translate(c.x, c.y);

                // 뒤로 헤엄치지 않고 정확히 바라보는 방향으로 좌우 반전
                if (c.facing === 'right') {
                    ctx.scale(-1, 1);
                }

                ctx.font = `${c.size}px "Segoe UI Emoji", "Apple Color Emoji", sans-serif`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                // 선명함을 높이는 드롭 섀도우
                ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
                ctx.shadowBlur = 4;
                ctx.shadowOffsetX = 1;
                ctx.shadowOffsetY = 1;

                ctx.fillText(c.emoji, 0, 0);
                ctx.restore();
            });
            ctx.restore();
        }

        let frameCount = 0;
        function mainLoop() {
            updatePhysics();
            updateDevices();
            updateCreatures();

            frameCount++;
            if (frameCount % 12 === 0) {
                updateEcosystem();
            }

            updateWaterColor();
            render();

            requestAnimationFrame(mainLoop);
        }

        mainLoop();
    </script>
</body>
</html>
"""

components.html(aquarium_simulation_html, height=720)
