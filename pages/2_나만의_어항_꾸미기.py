import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="나만의 어항 꾸미기",
    page_icon="🎨",
    layout="wide"
)

st.title("🐠 파우더 피지컬/생태계 어항 시뮬레이터")
st.caption("바닥재, 장치, 수초, 생물 간의 실시간 물리/화학적 상호작용 및 수질 변화를 직접 관찰해보세요!")

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
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }

        .main-container {
            display: flex;
            flex-direction: row;
            gap: 16px;
            width: 100%;
            max-width: 1280px;
            align-items: flex-start;
        }

        /* 왼쪽 도구 & 정보 패널 */
        .sidebar-panel {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 320px;
            flex-shrink: 0;
        }

        .dashboard {
            background-color: #1e293b;
            padding: 12px 14px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
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
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            text-align: center;
            transition: all 0.3s;
        }

        .stat-details {
            font-size: 12px;
            color: #cbd5e1;
            display: flex;
            justify-content: space-around;
            background-color: #0f172a;
            padding: 8px;
            border-radius: 8px;
        }

        .toolbar {
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: #1e293b;
            padding: 14px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
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
            padding-bottom: 3px;
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
            padding: 7px 8px;
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
        }

        .btn:hover {
            background-color: #475569;
            border-color: #38bdf8;
        }

        .btn.active {
            background-color: #0284c7;
            border-color: #38bdf8;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
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

        /* 오른쪽 큰 어항 영역 */
        .aquarium-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .canvas-wrapper {
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            border: 4px solid #334155;
            border-radius: 12px;
            overflow: hidden;
            background-color: #000;
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
        <!-- 1. 왼쪽 컨트롤 사이드바 -->
        <div class="sidebar-panel">
            <!-- 수질 대시보드 -->
            <div class="dashboard">
                <div class="stat-box">
                    <span style="font-size: 13px; font-weight: bold;">💧 수질 지수 (WQI)</span>
                    <div id="wqi-display" class="wqi-badge">100점 (최상)</div>
                </div>
                <div class="stat-details">
                    <span>💩 오염물: <b id="waste-count">0</b></span>
                    <span>🌿 수초: <b id="plant-count">0</b></span>
                    <span>🌀 장치: <b id="equip-count">0</b></span>
                </div>
            </div>

            <!-- 도구 툴바 -->
            <div class="toolbar">
                <!-- ① TERRAIN -->
                <div class="tool-group">
                    <span class="category-label">① 지형 / 바닥재</span>
                    <div class="btn-grid">
                        <button class="btn active" onclick="setTool(this, 'sand_gold')">🏖️ 금사</button>
                        <button class="btn" onclick="setTool(this, 'sand_black')">🖤 흑사</button>
                        <button class="btn" onclick="setTool(this, 'gravel')">🪨 강자갈</button>
                        <button class="btn" onclick="setTool(this, 'volcanic_rock')">🌋 화산석</button>
                        <button class="btn" onclick="setTool(this, 'driftwood')">🪵 유목</button>
                    </div>
                </div>

                <!-- ② PLANT -->
                <div class="tool-group">
                    <span class="category-label">② 수초 / 생장</span>
                    <div class="btn-grid">
                        <button class="btn" onclick="setTool(this, 'plant_weed')">🌿 기본수초</button>
                        <button class="btn" onclick="setTool(this, 'moss')">🟢 이끼</button>
                        <button class="btn" onclick="setTool(this, 'co2_bubble')">🫧 CO2 버블</button>
                    </div>
                </div>

                <!-- ③ EQUIPMENT -->
                <div class="tool-group">
                    <span class="category-label">③ 장치 / 환경</span>
                    <div class="btn-grid">
                        <button class="btn" onclick="setTool(this, 'air_bubble')">🫧 기포기</button>
                        <button class="btn" onclick="setTool(this, 'filter')">🌀 여과기</button>
                        <button class="btn" onclick="setTool(this, 'wave_maker')">💨 수류팬</button>
                        <button class="btn" onclick="setTool(this, 'heater')">🔥 히터</button>
                    </div>
                </div>

                <!-- ④ CREATURE -->
                <div class="tool-group">
                    <span class="category-label">④ 생물 / 먹이</span>
                    <div class="btn-grid">
                        <button class="btn" onclick="setTool(this, 'fish_top')">🐠 상층열대어</button>
                        <button class="btn" onclick="setTool(this, 'fish_bottom')">🐟 코리도라스</button>
                        <button class="btn" onclick="setTool(this, 'shrimp')">🦐 체리새우</button>
                        <button class="btn" onclick="setTool(this, 'fish_food')">🟤 물고기먹이</button>
                    </div>
                </div>

                <!-- ⑤ UTILITY -->
                <div class="tool-group">
                    <span class="category-label">⑤ 관리 / 도구</span>
                    <div class="btn-grid">
                        <button class="btn btn-action" onclick="setTool(this, 'eraser')">🧹 지우개</button>
                        <button class="btn btn-action" onclick="waterChange()">🪣 부분환수</button>
                        <button class="btn btn-action" onclick="useConditioner()">💊 수질정화</button>
                        <button class="btn btn-danger" onclick="resetSimulator()">🔄 전체리셋</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. 오른쪽 크고 선명한 어항 캔버스 -->
        <div class="aquarium-container">
            <div class="canvas-wrapper">
                <canvas id="aquarium" width="840" height="560"></canvas>
            </div>
            <div class="guide-text">💡 마우스로 클릭하거나 드래그하여 어항을 자유롭게 꾸며보세요.</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('aquarium');
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // ID 매핑 테이블
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

        // 색상 정의
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
        let targetWaterColor = [30, 136, 229, 0.25];
        let currentWaterColor = [30, 136, 229, 0.25];

        function setTool(btnElem, tool) {
            currentTool = tool;
            document.querySelectorAll('.btn').forEach(btn => {
                if (!btn.classList.contains('btn-action') && !btn.classList.contains('btn-danger')) {
                    btn.classList.remove('active');
                }
            });
            if (btnElem) btnElem.classList.add('active');
        }

        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) * (canvas.width / rect.width));
            const y = Math.floor((e.clientY - rect.top) * (canvas.height / rect.height));

            if (x < 0 || x >= width || y < 0 || y >= height) return;

            // 생물 직접 클릭 생성
            if (currentTool === 'fish_top') {
                if (isMouseDown && Math.random() < 0.15) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'top', x, y, vx: (Math.random()-0.5)*2, vy: (Math.random()-0.5)*1, emoji: '🐠' });
                }
                return;
            }
            if (currentTool === 'fish_bottom') {
                if (isMouseDown && Math.random() < 0.15) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'bottom', x, y: height - 30, vx: (Math.random()-0.5)*1.5, vy: 0, emoji: '🐟' });
                }
                return;
            }
            if (currentTool === 'shrimp') {
                if (isMouseDown && Math.random() < 0.15) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'shrimp', x, y: height - 20, vx: (Math.random()-0.5)*1.2, vy: 0, emoji: '🦐' });
                }
                return;
            }

            // 고정 장치 설치
            if (['filter', 'air_bubble', 'wave_maker', 'heater'].includes(currentTool)) {
                if (isMouseDown && Math.random() < 0.1) {
                    const emojiMap = { filter: '🌀', air_bubble: '🫧', wave_maker: '💨', heater: '🔥' };
                    equipments.push({ type: currentTool, x, y, emoji: emojiMap[currentTool] });
                }
                return;
            }

            // 일반 입자 브러시
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

        // 물리 엔진 루프
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
                            if (foodAge[idx] > 400) {
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

        // 수질 및 생태계 업데이트
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
                targetWaterColor = [30, 136, 229, 0.25];
                display.style.backgroundColor = '#0284c7';
                display.innerText = `${currentWQI}점 (최상)`;
            } else if (currentWQI >= 60) {
                targetWaterColor = [76, 175, 80, 0.35];
                display.style.backgroundColor = '#15803d';
                display.innerText = `${currentWQI}점 (주의)`;
            } else if (currentWQI >= 30) {
                targetWaterColor = [85, 139, 47, 0.5];
                display.style.backgroundColor = '#a16207';
                display.innerText = `${currentWQI}점 (경고)`;
            } else {
                targetWaterColor = [62, 39, 35, 0.65];
                display.style.backgroundColor = '#b91c1c';
                display.innerText = `${currentWQI}점 (최악)`;
            }

            // 여과기 흡입 작용
            equipments.forEach(eq => {
                if (eq.type === 'filter') {
                    for (let dy = -30; dy <= 30; dy++) {
                        for (let dx = -30; dx <= 30; dx++) {
                            const fx = eq.x + dx;
                            const fy = eq.y + dy;
                            if (fx >= 0 && fx < width && fy >= 0 && fy < height) {
                                const fIdx = fy * width + fx;
                                if (grid[fIdx] === WASTE) {
                                    grid[fIdx] = EMPTY;
                                }
                            }
                        }
                    }
                }
            });
        }

        // 생물 움직임
        function updateCreatures() {
            creatures.forEach(c => {
                const speedFactor = currentWQI < 30 ? 0.4 : 1.0;
                c.x += c.vx * speedFactor;
                c.y += c.vy * speedFactor;

                if (c.x < 15 || c.x > width - 15) c.vx *= -1;
                if (c.y < 25 || c.y > height - 25) c.vy *= -1;

                const cx = Math.floor(c.x);
                const cy = Math.floor(c.y);

                for (let dy = -12; dy <= 12; dy++) {
                    for (let dx = -12; dx <= 12; dx++) {
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

        // 캔버스 그려주기
        function render() {
            ctx.clearRect(0, 0, width, height);

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

            // 장치 그리기
            equipments.forEach(eq => {
                ctx.font = '20px serif';
                ctx.fillText(eq.emoji, eq.x - 10, eq.y + 7);
            });

            // 생물 그리기
            creatures.forEach(c => {
                ctx.font = '24px serif';
                ctx.fillText(c.emoji, c.x - 12, c.y + 8);
            });

            // 물 색상
            ctx.fillStyle = `rgba(${Math.round(currentWaterColor[0])}, ${Math.round(currentWaterColor[1])}, ${Math.round(currentWaterColor[2])}, ${currentWaterColor[3]})`;
            ctx.fillRect(0, 0, width, height);
        }

        function waterChange() {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE && Math.random() < 0.8) {
                    grid[i] = EMPTY;
                }
            }
        }

        function useConditioner() {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE) grid[i] = EMPTY;
            }
        }

        function resetSimulator() {
            grid.fill(EMPTY);
            foodAge.fill(0);
            creatures = [];
            equipments = [];
        }

        let frameCount = 0;
        function mainLoop() {
            updatePhysics();
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

components.html(aquarium_simulation_html, height=680)
