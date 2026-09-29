import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="나만의 어항 꾸미기",
    page_icon="🐠",
    layout="wide"
)

st.title("🐠 파우더 피지컬/생태계 어항 시뮬레이터")
st.caption("바닥재, 장치, 수초, 다양한 생물 간의 실시간 물리/화학적 상호작용 및 수질 변화를 직접 관찰해보세요!")

aquarium_simulation_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 10px;
        }

        .main-container {
            display: flex;
            flex-direction: row;
            gap: 16px;
            width: 100%;
            max-width: 1280px;
            margin: 0 auto;
            align-items: flex-start;
        }

        /* 왼쪽 스크롤 가능 사이드 패널 */
        .sidebar-panel {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 310px;
            max-height: 660px;
            overflow-y: auto;
            padding-right: 6px;
            flex-shrink: 0;
        }

        .sidebar-panel::-webkit-scrollbar {
            width: 6px;
        }
        .sidebar-panel::-webkit-scrollbar-track {
            background: #1e293b;
            border-radius: 4px;
        }
        .sidebar-panel::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }

        .dashboard {
            background-color: #1e293b;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #334155;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .stat-box {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .wqi-badge {
            padding: 5px 10px;
            border-radius: 16px;
            font-weight: bold;
            font-size: 12px;
            text-align: center;
        }

        .stat-details {
            font-size: 11px;
            color: #cbd5e1;
            display: flex;
            justify-content: space-around;
            background-color: #0f172a;
            padding: 6px;
            border-radius: 6px;
        }

        .toolbar {
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: #1e293b;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #334155;
        }

        .tool-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .category-label {
            font-size: 12px;
            font-weight: bold;
            color: #38bdf8;
            border-bottom: 1px solid #334155;
            padding-bottom: 4px;
        }

        .btn-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
        }

        .btn {
            background-color: #334155;
            color: #f8fafc;
            border: 1px solid #475569;
            padding: 8px 6px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            text-align: center;
            user-select: none;
        }

        .btn:hover {
            background-color: #475569;
            border-color: #38bdf8;
        }

        .btn.active {
            background-color: #0284c7 !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.5);
            font-weight: bold;
        }

        .btn-action {
            background-color: #0f766e;
            border-color: #14b8a6;
        }
        .btn-action:hover {
            background-color: #115e59;
        }

        .btn-danger {
            background-color: #991b1b;
            border-color: #ef4444;
        }
        .btn-danger:hover {
            background-color: #7f1d1d;
        }

        .aquarium-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .canvas-wrapper {
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            border: 3px solid #334155;
            border-radius: 12px;
            overflow: hidden;
            background-color: #030712;
        }

        canvas {
            display: block;
            cursor: crosshair;
        }

        .guide-text {
            margin-top: 8px;
            font-size: 12px;
            color: #94a3b8;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="main-container">
        <!-- 1. 왼쪽 사이드바 -->
        <div class="sidebar-panel">
            <div class="dashboard">
                <div class="stat-box">
                    <span style="font-size: 12px; font-weight: bold;">💧 수질 지수 (WQI)</span>
                    <div id="wqi-display" class="wqi-badge">100점 (최상)</div>
                </div>
                <div class="stat-details">
                    <span>💩 오염물: <b id="waste-count">0</b></span>
                    <span>🌿 수초: <b id="plant-count">0</b></span>
                    <span>🌀 장치: <b id="equip-count">0</b></span>
                </div>
            </div>

            <div class="toolbar">
                <div class="tool-group">
                    <span class="category-label">① 지형 / 바닥재</span>
                    <div class="btn-grid">
                        <button class="btn active" data-tool="sand_gold">🏖️ 금사</button>
                        <button class="btn" data-tool="sand_black">🖤 흑사</button>
                        <button class="btn" data-tool="gravel">🪨 강자갈</button>
                        <button class="btn" data-tool="volcanic_rock">🌋 화산석</button>
                        <button class="btn" data-tool="driftwood">🪵 유목</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">② 수초 / 생장</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="plant_weed">🌿 기본수초</button>
                        <button class="btn" data-tool="moss">🟢 이끼</button>
                        <button class="btn" data-tool="co2_bubble">🫧 CO2 버블</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">③ 장치 / 환경</span>
                    <div class="btn-grid">
                        <button class="btn" data-tool="air_bubble">🫧 기포기</button>
                        <button class="btn" data-tool="co2_diffuser">🫧 CO2 디퓨저</button>
                        <button class="btn" data-tool="filter">🌀 여과기</button>
                        <button class="btn" data-tool="wave_maker">💨 수류팬</button>
                        <button class="btn" data-tool="heater">🔥 히터</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">④ 어류 및 생물</span>
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
                        <button class="btn" data-tool="fish_food">🟤 물고기먹이</button>
                    </div>
                </div>

                <div class="tool-group">
                    <span class="category-label">⑤ 관리 / 도구</span>
                    <div class="btn-grid">
                        <button class="btn btn-action" data-tool="eraser">🧹 지우개</button>
                        <button class="btn btn-action" id="btn-water-change">🪣 부분환수</button>
                        <button class="btn btn-action" id="btn-conditioner">💊 수질정화</button>
                        <button class="btn btn-danger" id="btn-reset">🔄 전체리셋</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 어항 캔버스 -->
        <div class="aquarium-container">
            <div class="canvas-wrapper">
                <canvas id="aquarium" width="860" height="600"></canvas>
            </div>
            <div class="guide-text">💡 마우스로 클릭하거나 드래그하여 어항을 꾸미고 먹이를 주어보세요.</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('aquarium');
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

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
        const FISH_FOOD = 10;
        const WASTE = 11;

        const colors = {
            [SAND_GOLD]: [229, 193, 88],
            [SAND_BLACK]: [51, 51, 51],
            [GRAVEL]: [120, 114, 118],
            [VOLCANIC]: [74, 59, 50],
            [DRIFTWOOD]: [92, 64, 51],
            [PLANT]: [76, 175, 80],
            [MOSS]: [46, 125, 50],
            [CO2]: [129, 212, 250],
            [AIR]: [224, 247, 250],
            [FISH_FOOD]: [160, 82, 45],
            [WASTE]: [101, 67, 33]
        };

        const grid = new Uint8Array(width * height);
        const foodAge = new Uint16Array(width * height);

        let creatures = [];
        let equipments = [];
        let currentTool = 'sand_gold';
        let isMouseDown = false;

        let currentWQI = 100;
        let targetWaterColor = [30, 136, 229, 0.2];
        let currentWaterColor = [30, 136, 229, 0.2];

        // 지형 충돌 여부 체크 (단단한 지형)
        function isSolidTile(x, y) {
            if (x < 0 || x >= width || y < 0 || y >= height) return true;
            const type = grid[Math.floor(y) * width + Math.floor(x)];
            return (type === SAND_GOLD || type === SAND_BLACK || type === GRAVEL || type === VOLCANIC || type === DRIFTWOOD);
        }

        // 수초/이끼/지형 상단 착지 가능 여부 체크
        function isLandableTile(x, y) {
            if (x < 0 || x >= width || y < 0 || y >= height) return true;
            const type = grid[Math.floor(y) * width + Math.floor(x)];
            return (type === SAND_GOLD || type === SAND_BLACK || type === GRAVEL || type === VOLCANIC || type === DRIFTWOOD || type === MOSS || type === PLANT);
        }

        // 버튼 클릭 이벤트 처리
        document.querySelectorAll('.btn[data-tool]').forEach(btn => {
            btn.addEventListener('click', () => {
                currentTool = btn.getAttribute('data-tool');
                document.querySelectorAll('.btn[data-tool]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        document.getElementById('btn-water-change').addEventListener('click', () => {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE && Math.random() < 0.8) grid[i] = EMPTY;
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

        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) * (canvas.width / rect.width));
            const y = Math.floor((e.clientY - rect.top) * (canvas.height / rect.height));

            if (x < 0 || x >= width || y < 0 || y >= height) return;

            // 생물 스폰 설정
            const creatureConfig = {
                'guppy': { type: 'swim', emoji: '🐠' },
                'neon_tetra': { type: 'swim', emoji: '🐟' },
                'puffer': { type: 'swim', emoji: '🐡' },
                'angelfish': { type: 'swim', emoji: '🐠' },
                'turtle': { type: 'swim', emoji: '🐢' },
                'corydoras': { type: 'land', emoji: '🐟' },
                'shrimp': { type: 'land_climb', emoji: '🦐' },
                'snail': { type: 'land_climb', emoji: '🐌' },
                'crab': { type: 'land', emoji: '🦀' }
            };

            if (creatureConfig[currentTool]) {
                if (isMouseDown && Math.random() < 0.2) {
                    const cfg = creatureConfig[currentTool];
                    creatures.push({
                        id: Date.now() + Math.random(),
                        category: cfg.type,
                        x: x,
                        y: y,
                        vx: (Math.random() - 0.5) * 1.5,
                        vy: (Math.random() - 0.5) * 1.2,
                        emoji: cfg.emoji
                    });
                }
                return;
            }

            // 고정 장치 설치
            if (['filter', 'air_bubble', 'co2_diffuser', 'wave_maker', 'heater'].includes(currentTool)) {
                if (isMouseDown && Math.random() < 0.1) {
                    const emojiMap = { filter: '🌀', air_bubble: '🫧', co2_diffuser: '🫧', wave_maker: '💨', heater: '🔥' };
                    equipments.push({ type: currentTool, x, y, emoji: emojiMap[currentTool] });
                }
                return;
            }

            const radius = (currentTool === 'volcanic_rock' || currentTool === 'driftwood') ? 9 : 5;
            const toolId = getToolId(currentTool);

            for (let dx = -radius; dx <= radius; dx++) {
                for (let dy = -radius; dy <= radius; dy++) {
                    const px = x + dx;
                    const py = y + dy;
                    if (px >= 0 && px < width && py >= 0 && py < height) {
                        if (dx*dx + dy*dy <= radius*radius) {
                            if (currentTool === 'eraser') {
                                grid[py * width + px] = EMPTY;
                                foodAge[py * width + px] = 0;
                            } else if (Math.random() > 0.15 || currentTool === 'volcanic_rock' || currentTool === 'driftwood') {
                                grid[py * width + px] = toolId;
                                foodAge[py * width + px] = 0;
                            }
                        }
                    }
                }
            }
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
                case 'fish_food': return FISH_FOOD;
                default: return EMPTY;
            }
        }

        canvas.addEventListener('mousedown', (e) => { isMouseDown = true; handlePointer(e); });
        canvas.addEventListener('mousemove', (e) => { if (isMouseDown) handlePointer(e); });
        window.addEventListener('mouseup', () => isMouseDown = false);

        // 오토 생성 기포 및 디퓨저 동작
        let deviceTimer = 0;
        function updateDevices() {
            deviceTimer++;
            if (deviceTimer % 8 === 0) {
                equipments.forEach(eq => {
                    if (eq.type === 'air_bubble') {
                        const idx = (eq.y - 12) * width + eq.x;
                        if (eq.y - 12 > 0) grid[idx] = AIR;
                    } else if (eq.type === 'co2_diffuser') {
                        const idx = (eq.y - 12) * width + eq.x;
                        if (eq.y - 12 > 0) grid[idx] = CO2;
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

                    if (type === SAND_GOLD || type === SAND_BLACK || type === GRAVEL || type === FISH_FOOD || type === WASTE) {
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

                        if (type === FISH_FOOD) {
                            foodAge[idx]++;
                            if (foodAge[idx] > 600) {
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

            for (let py = 10; py < height; py += 10) {
                for (let px = 10; px < width; px += 10) {
                    if (grid[py * width + px] === FISH_FOOD) {
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
            const plantBonus = Math.floor(plantCount * 0.04);
            const wastePenalty = wasteCount * 2;

            let score = 100 - wastePenalty + filterBonus + plantBonus;
            currentWQI = Math.max(0, Math.min(100, score));

            const display = document.getElementById('wqi-display');
            document.getElementById('waste-count').innerText = wasteCount;
            document.getElementById('plant-count').innerText = plantCount;
            document.getElementById('equip-count').innerText = equipments.length;

            if (currentWQI >= 85) {
                targetWaterColor = [30, 136, 229, 0.2];
                display.style.backgroundColor = '#0284c7';
                display.innerText = `${currentWQI}점 (최상)`;
            } else if (currentWQI >= 60) {
                targetWaterColor = [76, 175, 80, 0.3];
                display.style.backgroundColor = '#15803d';
                display.innerText = `${currentWQI}점 (주의)`;
            } else if (currentWQI >= 30) {
                targetWaterColor = [85, 139, 47, 0.45];
                display.style.backgroundColor = '#a16207';
                display.innerText = `${currentWQI}점 (경고)`;
            } else {
                targetWaterColor = [62, 39, 35, 0.6];
                display.style.backgroundColor = '#b91c1c';
                display.innerText = `${currentWQI}점 (최악)`;
            }

            equipments.forEach(eq => {
                if (eq.type === 'filter') {
                    for (let dy = -25; dy <= 25; dy++) {
                        for (let dx = -25; dx <= 25; dx++) {
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

        // 지형 통과 방지 및 고유 행동 알고리즘
        function updateCreatures() {
            creatures.forEach(c => {
                const food = findClosestFood(c.x, c.y);

                if (c.category === 'swim') {
                    // 유영 어류 AI (구피, 테트라, 복어, 엔젤피쉬, 거북이)
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

                    c.vx = Math.max(-2.0, Math.min(2.0, c.vx));
                    c.vy = Math.max(-1.2, Math.min(1.2, c.vy));

                    let nextX = c.x + c.vx;
                    let nextY = c.y + c.vy;

                    // 지형지물 충돌 반사 (통과 금지)
                    if (isSolidTile(nextX, nextY)) {
                        c.vx *= -0.8;
                        c.vy *= -0.8;
                    } else {
                        c.x = nextX;
                        c.y = nextY;
                    }

                } else if (c.category === 'land' || c.category === 'land_climb') {
                    // 저서 생물 AI (코리도라스, 게, 새우, 애플스네일)
                    // 바닥/공중 돌/이끼 위에 서있는지 감지
                    const onSolid = isLandableTile(c.x, c.y + 12) || c.y >= height - 25;

                    if (!onSolid) {
                        c.vy += 0.25; // 중력 낙하 (공중 돌이나 바닥으로 착지)
                    } else {
                        c.vy = 0;
                        if (Math.random() < 0.08) {
                            c.vx = (Math.random() - 0.5) * 1.5;
                        }
                    }

                    if (food && c.category === 'land_climb') {
                        const dx = food.x - c.x;
                        const dy = food.y - c.y;
                        if (Math.abs(dx) > 3) c.vx = (dx > 0 ? 1 : -1) * 1.2;
                        if (dy < -5) c.vy = -1.0; // 수초/이끼 타고 위로 이동
                    }

                    let nextX = c.x + c.vx;
                    let nextY = c.y + c.vy;

                    if (isSolidTile(nextX, nextY)) {
                        c.vx *= -1;
                    } else {
                        c.x = nextX;
                        c.y = nextY;
                    }
                }

                // 벽 충돌
                if (c.x < 25) { c.x = 25; c.vx *= -1; }
                if (c.x > width - 25) { c.x = width - 25; c.vx *= -1; }
                if (c.y < 25) { c.y = 25; c.vy *= -1; }
                if (c.y > height - 25) { c.y = height - 25; c.vy = 0; }

                // 먹이 섭취
                const cx = Math.floor(c.x);
                const cy = Math.floor(c.y);
                for (let dy = -15; dy <= 15; dy++) {
                    for (let dx = -15; dx <= 15; dx++) {
                        const px = cx + dx;
                        const py = cy + dy;
                        if (px >= 0 && px < width && py >= 0 && py < height) {
                            const idx = py * width + px;
                            if (grid[idx] === FISH_FOOD) {
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

            // 1. 파우더 입자 렌더링
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

            // 2. 수질 물 색상 덮어씌우기 (어항 물의 투명도 느낌 표현)
            ctx.fillStyle = `rgba(${Math.round(currentWaterColor[0])}, ${Math.round(currentWaterColor[1])}, ${Math.round(currentWaterColor[2])}, ${currentWaterColor[3]})`;
            ctx.fillRect(0, 0, width, height);

            // 3. 고정 장치 렌더링
            equipments.forEach(eq => {
                ctx.font = '22px serif';
                ctx.fillText(eq.emoji, eq.x - 11, eq.y + 8);
            });

            // 4. 생물 렌더링 (물 색상 레이어 위에 그려 선명하고 흐리지 않음!)
            ctx.globalAlpha = 1.0;
            creatures.forEach(c => {
                ctx.save();
                ctx.translate(c.x, c.y);

                // 좌우 이동에 따른 자연스러운 반전
                if (c.vx < 0) {
                    ctx.scale(-1, 1);
                }

                ctx.font = '28px serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(c.emoji, 0, 0);
                ctx.restore();
            });
        }

        let frameCount = 0;
        function mainLoop() {
            updatePhysics();
            updateDevices();
            updateCreatures();

            frameCount++;
            if (frameCount % 15 === 0) {
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
