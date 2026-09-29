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
            padding: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .dashboard {
            display: flex;
            gap: 15px;
            width: 100%;
            max-width: 900px;
            justify-content: space-between;
            align-items: center;
            background-color: #1e293b;
            padding: 12px 20px;
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            border: 1px solid #334155;
        }

        .stat-box {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .wqi-badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 15px;
            transition: all 0.3s;
        }

        .toolbar {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
            max-width: 900px;
            background-color: #1e293b;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            border: 1px solid #334155;
        }

        .tool-group {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }

        .category-label {
            font-size: 12px;
            font-weight: bold;
            color: #94a3b8;
            min-width: 80px;
        }

        .btn {
            background-color: #334155;
            color: #f8fafc;
            border: 1px solid #475569;
            padding: 6px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 4px;
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
            color: #64748b;
        }
    </style>
</head>
<body>

    <!-- 대시보드 (수질 정보 및 유틸리티) -->
    <div class="dashboard">
        <div class="stat-box">
            <span>💧 수질 지수 (WQI):</span>
            <div id="wqi-display" class="wqi-badge">100점 (최상)</div>
        </div>
        <div class="stat-box" style="font-size: 13px; color: #cbd5e1;">
            <span>💩 오염물: <b id="waste-count">0</b></span> |
            <span>🌿 수초: <b id="plant-count">0</b></span> |
            <span>🌀 여과기: <b id="filter-count">0</b></span>
        </div>
    </div>

    <!-- 툴바 (카테고리별 규격 구현) -->
    <div class="toolbar">
        <!-- 1. TERRAIN -->
        <div class="tool-group">
            <span class="category-label">① 지형/바닥재</span>
            <button class="btn active" onclick="setTool('sand_gold')">🏖️ 금사 (#E5C158)</button>
            <button class="btn" onclick="setTool('sand_black')">🖤 흑사 (#333333)</button>
            <button class="btn" onclick="setTool('gravel')">🪨 강자갈 (#787276)</button>
            <button class="btn" onclick="setTool('volcanic_rock')">🌋 화산석</button>
            <button class="btn" onclick="setTool('driftwood')">🪵 유목</button>
        </div>
        <!-- 2. PLANT -->
        <div class="tool-group">
            <span class="category-label">② 수초/생장</span>
            <button class="btn" onclick="setTool('plant_weed')">🌿 기본수초</button>
            <button class="btn" onclick="setTool('moss')">🟢 이끼</button>
            <button class="btn" onclick="setTool('co2_bubble')">🫧 CO2 버블</button>
        </div>
        <!-- 3. EQUIPMENT -->
        <div class="tool-group">
            <span class="category-label">③ 장치/환경</span>
            <button class="btn" onclick="setTool('air_bubble')">🫧 기포기</button>
            <button class="btn" onclick="setTool('filter')">🌀 여과기</button>
            <button class="btn" onclick="setTool('wave_maker')">💨 수류팬</button>
            <button class="btn" onclick="setTool('heater')">🔥 히터</button>
        </div>
        <!-- 4. CREATURE -->
        <div class="tool-group">
            <span class="category-label">④ 생물/먹이</span>
            <button class="btn" onclick="setTool('fish_top')">🐠 상층 열대어</button>
            <button class="btn" onclick="setTool('fish_bottom')">🐟 코리도라스</button>
            <button class="btn" onclick="setTool('shrimp')">🦐 체리새우</button>
            <button class="btn" onclick="setTool('fish_food')">🟤 물고기 먹이</button>
        </div>
        <!-- 5. UTILITY -->
        <div class="tool-group">
            <span class="category-label">⑤ 관리/도구</span>
            <button class="btn btn-action" onclick="setTool('eraser')">🧹 지우개</button>
            <button class="btn btn-action" onclick="waterChange()">🪣 부분 환수</button>
            <button class="btn btn-action" onclick="useConditioner()">💊 수질정화제</button>
            <button class="btn btn-danger" onclick="resetSimulator()">🔄 전체 리셋</button>
        </div>
    </div>

    <!-- 캔버스 영역 -->
    <div class="canvas-wrapper">
        <canvas id="aquarium" width="800" height="460"></canvas>
    </div>

    <div class="guide-text">💡 마우스로 클릭하거나 드래그하여 입자와 오브젝트를 설치하세요. 생물은 자동으로 먹이를 찾고 수질에 반응합니다.</div>

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
        const FILTER = 10;
        const FISH_FOOD = 11;
        const WASTE = 12;

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
            [FILTER]: [2, 132, 199],
            [FISH_FOOD]: [160, 82, 45],
            [WASTE]: [101, 67, 33]
        };

        // 입자 그리드 및 먹이 타이머
        const grid = new Uint8Array(width * height);
        const foodAge = new Uint16Array(width * height);

        // 객체 데이터 (생물, 장치 등)
        let creatures = [];
        let equipments = [];
        let currentTool = 'sand_gold';
        let isMouseDown = false;

        // 수질 지수 & 물 색상 보간 (Lerp)
        let currentWQI = 100;
        let targetWaterColor = [30, 136, 229, 0.3]; // RGBA
        let currentWaterColor = [30, 136, 229, 0.3];

        function setTool(tool) {
            currentTool = tool;
            document.querySelectorAll('.btn').forEach(btn => {
                if (!btn.classList.contains('btn-action') && !btn.classList.contains('btn-danger')) {
                    btn.classList.remove('active');
                }
            });
            event.currentTarget.classList.add('active');
        }

        // 툴 사용 (입자 및 생물 배치)
        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor(e.clientX - rect.left);
            const y = Math.floor(e.clientY - rect.top);

            if (x < 0 || x >= width || y < 0 || y >= height) return;

            // 생물 직접 설치
            if (currentTool === 'fish_top') {
                if (isMouseDown && Math.random() < 0.1) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'top', x, y, vx: (Math.random()-0.5)*2, vy: (Math.random()-0.5)*1, emoji: '🐠' });
                }
                return;
            }
            if (currentTool === 'fish_bottom') {
                if (isMouseDown && Math.random() < 0.1) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'bottom', x, y: height - 20, vx: (Math.random()-0.5)*1.5, vy: 0, emoji: '🐟' });
                }
                return;
            }
            if (currentTool === 'shrimp') {
                if (isMouseDown && Math.random() < 0.1) {
                    creatures.push({ id: Date.now() + Math.random(), type: 'shrimp', x, y: height - 15, vx: (Math.random()-0.5)*1.2, vy: 0, emoji: '🦐' });
                }
                return;
            }

            // 고정 장치 설치
            if (currentTool === 'filter') {
                if (isMouseDown && Math.random() < 0.05) {
                    equipments.push({ type: 'filter', x, y, range: 60 });
                }
            }

            // 일반 입자 브러시
            const radius = (currentTool === 'volcanic_rock' || currentTool === 'driftwood') ? 8 : 4;
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
                            } else if (Math.random() > 0.2 || currentTool === 'volcanic_rock' || currentTool === 'driftwood') {
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
                case 'air_bubble': return AIR;
                case 'fish_food': return FISH_FOOD;
                default: return EMPTY;
            }
        }

        canvas.addEventListener('mousedown', (e) => { isMouseDown = true; handlePointer(e); });
        canvas.addEventListener('mousemove', (e) => { if (isMouseDown) handlePointer(e); });
        window.addEventListener('mouseup', () => isMouseDown = false);

        // 1. 물리 시뮬레이션 루프 (Particle Physics & Repose Angle)
        function updatePhysics() {
            for (let y = height - 2; y >= 0; y--) {
                for (let x = 0; x < width; x++) {
                    const idx = y * width + x;
                    const type = grid[idx];

                    if (type === EMPTY || type === VOLCANIC || type === DRIFTWOOD) continue;

                    // 모래, 강자갈, 먹이, 오염물 (중력 및 안식각 슬라이딩)
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

                        // 먹이 부패 규칙 (일정 시간 미섭취 시 오염물로 변함)
                        if (type === FISH_FOOD) {
                            foodAge[idx]++;
                            if (foodAge[idx] > 350) { // 약 6초 후 변환
                                grid[idx] = WASTE;
                                foodAge[idx] = 0;
                            }
                        }
                    }

                    // CO2 버블 & 기포기 (위로 상승)
                    else if (type === CO2 || type === AIR) {
                        const above = (y - 1) * width + x;
                        if (y > 0 && grid[above] === EMPTY) {
                            grid[above] = type;
                            grid[idx] = EMPTY;
                        } else {
                            grid[idx] = EMPTY; // 수면에 도달하면 소멸
                        }
                    }
                }
            }
        }

        // 2. 생태계 및 WQI 계산 (Ecosystem & Water Quality)
        let wasteCount = 0;
        let plantCount = 0;

        function updateEcosystem() {
            wasteCount = 0;
            plantCount = 0;

            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE) wasteCount++;
                if (grid[i] === PLANT || grid[i] === MOSS) plantCount++;
            }

            const filterBonus = equipments.length * 15;
            const plantBonus = Math.floor(plantCount * 0.05);
            const wastePenalty = wasteCount * 2;

            let score = 100 - wastePenalty + filterBonus + plantBonus;
            currentWQI = Math.max(0, Math.min(100, score));

            // WQI 별 목표 물 색상 및UI 업데이트
            const display = document.getElementById('wqi-display');
            document.getElementById('waste-count').innerText = wasteCount;
            document.getElementById('plant-count').innerText = plantCount;
            document.getElementById('filter-count').innerText = equipments.length;

            if (currentWQI >= 85) {
                targetWaterColor = [30, 136, 229, 0.25]; // 1단계: 맑은 푸른빛
                display.className = 'wqi-badge';
                display.style.backgroundColor = '#0284c7';
                display.innerText = `${currentWQI}점 (1단계: 최상)`;
            } else if (currentWQI >= 60) {
                targetWaterColor = [76, 175, 80, 0.35]; // 2단계: 연한 연두색 (녹조 초기)
                display.className = 'wqi-badge';
                display.style.backgroundColor = '#15803d';
                display.innerText = `${currentWQI}점 (2단계: 주의)`;
            } else if (currentWQI >= 30) {
                targetWaterColor = [85, 139, 47, 0.5]; // 3단계: 탁한 녹색 (백탁)
                display.className = 'wqi-badge';
                display.style.backgroundColor = '#a16207';
                display.innerText = `${currentWQI}점 (3단계: 경고)`;
            } else {
                targetWaterColor = [62, 39, 35, 0.65]; // 4단계: 탁한 갈색 (슬러지)
                display.className = 'wqi-badge';
                display.style.backgroundColor = '#b91c1c';
                display.innerText = `${currentWQI}점 (4단계: 최악)`;
            }

            // 여과기 흡입 로직 (주변 오염물 스캔 후 제거)
            equipments.forEach(eq => {
                if (eq.type === 'filter') {
                    for (let dy = -25; dy <= 25; dy++) {
                        for (let dx = -25; dx <= 25; dx++) {
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

        // 3. 생물 AI 및 먹이 감지 (Creature AI)
        function updateCreatures() {
            creatures.forEach(c => {
                // 수질 악화 시 이동 속도 저하
                const speedFactor = currentWQI < 30 ? 0.4 : 1.0;

                c.x += c.vx * speedFactor;
                c.y += c.vy * speedFactor;

                // 어항 벽 충돌 처리
                if (c.x < 10 || c.x > width - 10) c.vx *= -1;
                if (c.y < 20 || c.y > height - 20) c.vy *= -1;

                // 주위 먹이 탐지 및 섭취
                const cx = Math.floor(c.x);
                const cy = Math.floor(c.y);

                for (let dy = -10; dy <= 10; dy++) {
                    for (let dx = -10; dx <= 10; dx++) {
                        const px = cx + dx;
                        const py = cy + dy;
                        if (px >= 0 && px < width && py >= 0 && py < height) {
                            const idx = py * width + px;
                            if (grid[idx] === FISH_FOOD) {
                                grid[idx] = EMPTY; // 먹이 섭취!
                                foodAge[idx] = 0;
                            }
                        }
                    }
                }
            });
        }

        // 4. 자연스러운 색상 보간 (Lerp Function)
        function lerp(start, end, amt) {
            return (1 - amt) * start + amt * end;
        }

        function updateWaterColor() {
            for (let i = 0; i < 4; i++) {
                currentWaterColor[i] = lerp(currentWaterColor[i], targetWaterColor[i], 0.02);
            }
        }

        // 5. 렌더링 루프 (Render)
        function render() {
            ctx.clearRect(0, 0, width, height);

            // 입자 그리드 그리기
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

            // 여과기 및 장치 그리기
            equipments.forEach(eq => {
                ctx.fillStyle = '#0284c7';
                ctx.beginPath();
                ctx.arc(eq.x, eq.y, 12, 0, Math.PI * 2);
                ctx.fill();
                ctx.font = '12px serif';
                ctx.fillText('🌀', eq.x - 6, eq.y + 4);
            });

            // 생물 그리기
            creatures.forEach(c => {
                ctx.font = '22px serif';
                ctx.fillText(c.emoji, c.x - 10, c.y + 8);
            });

            // 오버레이 물 색상 적용 (Lerp 보간된 수색)
            ctx.fillStyle = `rgba(${Math.round(currentWaterColor[0])}, ${Math.round(currentWaterColor[1])}, ${Math.round(currentWaterColor[2])}, ${currentWaterColor[3]})`;
            ctx.fillRect(0, 0, width, height);
        }

        // 유틸리티 버튼 기능
        function waterChange() {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === WASTE && Math.random() < 0.7) {
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

        // 메인 프레임 진행 루프
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

components.html(aquarium_simulation_html, height=720)
