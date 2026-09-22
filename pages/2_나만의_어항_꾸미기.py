import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="나만의 어항 꾸미기",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 파우더 게임 스타일 나만의 어항 꾸미기")
st.caption("원하는 바닥재, 돌, 수초, 생물을 선택하고 어항 화면을 클릭하거나 드래그하여 나만의 어항을 완성해보세요!")

# HTML/JS 기반의 파우더 게임 스타일 어항 캔버스
sandbox_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            background-color: #1a1a2e;
            color: #ffffff;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
            justify-content: center;
            background-color: #16213e;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .btn {
            background-color: #0f3460;
            color: white;
            border: 2px solid #e94560;
            padding: 8px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
        }
        .btn:hover {
            background-color: #e94560;
        }
        .btn.active {
            background-color: #e94560;
            box-shadow: 0 0 10px #e94560;
        }
        .canvas-container {
            position: relative;
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
            border: 4px solid #0f3460;
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            background: linear-gradient(180deg, #184e77 0%, #1e6091 60%, #1a4d6e 100%);
            cursor: crosshair;
            display: block;
        }
        .info {
            margin-top: 8px;
            font-size: 13px;
            color: #a0a0a0;
        }
    </style>
</head>
<body>

    <div class="toolbar">
        <button class="btn active" onclick="setTool('sand')">🏖️ 금사 모래</button>
        <button class="btn" onclick="setTool('blacksand')">🖤 흑사 모래</button>
        <button class="btn" onclick="setTool('gravel')">🪨 강자갈</button>
        <button class="btn" onclick="setTool('rock')">🌋 화산석</button>
        <button class="btn" onclick="setTool('wood')">🪵 유목</button>
        <button class="btn" onclick="setTool('plant')">🌿 수초</button>
        <button class="btn" onclick="setTool('water')">💧 물 입자</button>
        <button class="btn" onclick="setTool('eraser')">🧹 지우개</button>
        <button class="btn" style="border-color:#ff4b4b; background-color:#8b0000;" onclick="clearCanvas()">🔄 전체 리셋</button>
    </div>

    <div class="canvas-container">
        <canvas id="aquarium" width="700" height="420"></canvas>
    </div>

    <div class="info">💡 어항 화면을 클릭하거나 마우스로 드래그하면 선택한 모래와 물질들이 싸악 쌓입니다!</div>

    <script>
        const canvas = document.getElementById('aquarium');
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // 시뮬레이션 격자 (0: 공기/물, 1: 모래, 2: 흑사, 3: 자갈, 4: 화산석, 5: 유목, 6: 수초, 7: 물)
        const grid = new Uint8Array(width * height);
        const colors = {
            0: null,
            1: '#e0c068', // 모래
            2: '#333333', // 흑사
            3: '#8d99ae', // 자갈
            4: '#4a3b32', // 화산석
            5: '#5c4033', // 유목
            6: '#2a9d8f', // 수초
            7: '#48cae4'  // 물
        };

        let currentTool = 'sand';
        let isMouseDown = false;

        function setTool(tool) {
            currentTool = tool;
            document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }

        function clearCanvas() {
            grid.fill(0);
        }

        function getToolId(tool) {
            switch(tool) {
                case 'sand': return 1;
                case 'blacksand': return 2;
                case 'gravel': return 3;
                case 'rock': return 4;
                case 'wood': return 5;
                case 'plant': return 6;
                case 'water': return 7;
                case 'eraser': return 0;
                default: return 1;
            }
        }

        function placeParticle(x, y, tool) {
            const radius = (tool === 'rock' || tool === 'wood') ? 6 : 3;
            const toolId = getToolId(tool);

            for (let dx = -radius; dx <= radius; dx++) {
                for (let dy = -radius; dy <= radius; dy++) {
                    const px = x + dx;
                    const py = y + dy;
                    if (px >= 0 && px < width && py >= 0 && py < height) {
                        if (dx*dx + dy*dy <= radius*radius) {
                            if (Math.random() > 0.15 || tool === 'rock' || tool === 'wood' || tool === 'eraser') {
                                grid[py * width + px] = toolId;
                            }
                        }
                    }
                }
            }
        }

        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor(e.clientX - rect.left);
            const y = Math.floor(e.clientY - rect.top);
            placeParticle(x, y, currentTool);
        }

        canvas.addEventListener('mousedown', (e) => {
            isMouseDown = true;
            handlePointer(e);
        });

        canvas.addEventListener('mousemove', (e) => {
            if (isMouseDown) handlePointer(e);
        });

        window.addEventListener('mouseup', () => isMouseDown = false);

        // 파우더 물리엔진 업데이트 루프
        function update() {
            // 아래에서 위로 스캔 (중력 효과)
            for (let y = height - 2; y >= 0; y--) {
                for (let x = 0; x < width; x++) {
                    const idx = y * width + x;
                    const type = grid[idx];

                    // 모래, 흑사, 자갈 중력 물리 법칙
                    if (type === 1 || type === 2 || type === 3) {
                        const below = (y + 1) * width + x;
                        const belowLeft = (y + 1) * width + (x - 1);
                        const belowRight = (y + 1) * width + (x + 1);

                        if (grid[below] === 0 || grid[below] === 7) {
                            grid[below] = type;
                            grid[idx] = 0;
                        } else if (x > 0 && (grid[belowLeft] === 0 || grid[belowLeft] === 7)) {
                            grid[belowLeft] = type;
                            grid[idx] = 0;
                        } else if (x < width - 1 && (grid[belowRight] === 0 || grid[belowRight] === 7)) {
                            grid[belowRight] = type;
                            grid[idx] = 0;
                        }
                    }
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, width, height);

            // 그리드 렌더링
            const imgData = ctx.createImageData(width, height);
            const data = imgData.data;

            for (let i = 0; i < grid.length; i++) {
                const type = grid[i];
                if (type !== 0) {
                    const colorHex = colors[type];
                    const r = parseInt(colorHex.slice(1, 3), 16);
                    const g = parseInt(colorHex.slice(3, 5), 16);
                    const b = parseInt(colorHex.slice(5, 7), 16);

                    const pixelIdx = i * 4;
                    data[pixelIdx] = r;
                    data[pixelIdx + 1] = g;
                    data[pixelIdx + 2] = b;
                    data[pixelIdx + 3] = type === 7 ? 180 : 255;
                }
            }

            ctx.putImageData(imgData, 0, 0);

            // 간단한 물고기 유영 애니메이션 효과
            drawFish();
        }

        let fishX = 100;
        let fishY = 150;
        let fishSpeed = 1.2;

        function drawFish() {
            fishX += fishSpeed;
            if (fishX > width + 30) fishX = -30;

            ctx.font = '24px serif';
            ctx.fillText('🐠', fishX, fishY);
            ctx.fillText('🐟', (fishX * 0.7) % width, fishY + 80);
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

components.html(sandbox_html, height=580)
