<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>픽셀 파우더 어항 Sandbox Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
            background-color: #0d1117;
            color: #c9d1d9;
        }
        canvas {
            image-rendering: pixelated;
            cursor: crosshair;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #161b22;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 3px;
        }
        .btn-active {
            border-color: #38bdf8 !important;
            background-color: #1e293b !important;
            color: #38bdf8 !important;
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col overflow-hidden bg-slate-950 text-slate-100">

    <!-- 상단 헤더 /어항 환경 설정 -->
    <header class="h-14 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-4 shrink-0">
        <div class="flex items-center space-x-3">
            <i class="fa-solid font-bold text-cyan-400 text-xl flex items-center gap-2">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                픽셀 파우더 어항 Sandbox Pro
            </i>
        </div>

        <!-- 어항 수질/타입 설정 -->
        <div class="flex items-center space-x-6 text-sm">
            <div class="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400 font-medium">어항 모드:</span>
                <button id="tankTypeFresh" onclick="setTankType('fresh')" class="px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-emerald-600 text-white shadow">
                    🌿 담수어 어항
                </button>
                <button id="tankTypeMarine" onclick="setTankType('marine')" class="px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-slate-700 text-slate-300 hover:bg-slate-600">
                    🌊 해수어 어항
                </button>
            </div>

            <div class="flex items-center space-x-4 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/50">
                <span>🌡️ 수온: <strong id="tempDisp" class="text-cyan-400">24°C</strong></span>
                <span>💧 수질: <strong id="waterQualityDisp" class="text-emerald-400">100%</strong></span>
                <span>🐟 개체수: <strong id="fishCountDisp" class="text-amber-400">0</strong></span>
            </div>
        </div>
    </header>

    <!-- 메인 메인 구역 -->
    <div class="flex-1 flex overflow-hidden">
        
        <!-- 좌측 도구 패널 -->
        <aside class="w-80 bg-slate-900 border-r border-slate-800 flex flex-col shrink-0 custom-scrollbar overflow-y-auto">
            
            <!-- 모드 탭 -->
            <div class="grid grid-cols-3 bg-slate-950 p-1.5 gap-1 border-b border-slate-800">
                <button id="tabPowder" onclick="switchTab('powder')" class="py-2 text-xs font-semibold rounded text-cyan-400 bg-slate-800 border border-cyan-500/30">
                    🧪 파우더 모드
                </button>
                <button id="tabCreature" onclick="switchTab('creature')" class="py-2 text-xs font-semibold rounded text-slate-400 hover:text-slate-200">
                    🐟 생물 모드
                </button>
                <button id="tabEquip" onclick="switchTab('equip')" class="py-2 text-xs font-semibold rounded text-slate-400 hover:text-slate-200">
                    💡 장비 모드
                </button>
            </div>

            <div class="p-4 space-y-6">

                <!-- 1. 파우더 모드 옵션 -->
                <div id="panelPowder" class="space-y-4">
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-2">🖌️ 펜 크기: <span id="brushSizeDisp" class="text-cyan-400">3px</span></label>
                        <input type="range" id="brushSize" min="1" max="15" value="3" oninput="updateBrushSize(this.value)" class="w-full accent-cyan-500">
                    </div>

                    <div class="space-y-2">
                        <span class="text-xs text-slate-400 font-bold block">특수 상호작용 펜</span>
                        <div class="grid grid-cols-2 gap-2">
                            <button onclick="selectTool('eraser')" id="tool_eraser" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-2">
                                🧹 픽셀 삭제펜
                            </button>
                            <button onclick="selectTool('cleaner')" id="tool_cleaner" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-2">
                                ✨ 똥/오염 청소펜
                            </button>
                        </div>
                    </div>

                    <div class="space-y-2">
                        <span class="text-xs text-slate-400 font-bold block">바닥재 & 샌드박스 원소</span>
                        <div class="grid grid-cols-2 gap-2">
                            <button onclick="selectTool('sand')" id="tool_sand" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-amber-400 rounded-full inline-block"></span> 금사 모래
                            </button>
                            <button onclick="selectTool('soil')" id="tool_soil" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-amber-900 rounded-full inline-block"></span> 영양 소일
                            </button>
                            <button onclick="selectTool('rock')" id="tool_rock" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-gray-500 rounded-full inline-block"></span> 고정 암석
                            </button>
                            <button onclick="selectTool('wood')" id="tool_wood" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-amber-800 rounded-full inline-block"></span> 고정 유목
                            </button>
                            <button onclick="selectTool('seed')" id="tool_seed" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-emerald-400 rounded-full inline-block"></span> 수초 씨앗
                            </button>
                            <button onclick="selectTool('food')" id="tool_food" class="tool-btn border border-slate-700 bg-slate-800 p-2 rounded text-xs text-left hover:bg-slate-700 flex items-center gap-1.5">
                                <span class="w-3 h-3 bg-orange-400 rounded-full inline-block"></span> 먹이 입자
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 2. 생물 모드 옵션 -->
                <div id="panelCreature" class="space-y-4 hidden">
                    <div class="text-xs text-amber-300/80 bg-amber-950/40 p-2.5 rounded border border-amber-800/40">
                        ⚠️ 어항 타입(담수/해수)에 안 맞는 생물을 넣으면 체력이 깎여 사망할 수 있습니다!
                    </div>

                    <!-- 담수 생물 목록 -->
                    <div class="space-y-2">
                        <span class="text-xs text-emerald-400 font-bold flex items-center justify-between">
                            🌿 담수어 & 생물
                            <span class="text-[10px] text-slate-500">담수 어항 추천</span>
                        </span>
                        <div class="grid grid-cols-2 gap-2">
                            <button onclick="spawnCreature('guppy')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐟 구피
                            </button>
                            <button onclick="spawnCreature('neon')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐟 네온테트라
                            </button>
                            <button onclick="spawnCreature('shrimp')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🦐 체리새우
                            </button>
                            <button onclick="spawnCreature('freshTurtle')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐢 반수생 거북이
                            </button>
                        </div>
                    </div>

                    <!-- 해수 생물 목록 -->
                    <div class="space-y-2">
                        <span class="text-xs text-cyan-400 font-bold flex items-center justify-between">
                            🌊 해수어 & 생물
                            <span class="text-[10px] text-slate-500">해수 어항 추천</span>
                        </span>
                        <div class="grid grid-cols-2 gap-2">
                            <button onclick="spawnCreature('clownfish')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐠 크라운피쉬
                            </button>
                            <button onclick="spawnCreature('blueTang')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐠 블루탱
                            </button>
                            <button onclick="spawnCreature('puffer')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐡 복어
                            </button>
                            <button onclick="spawnCreature('seaTurtle')" class="p-2 border border-slate-700 bg-slate-800 rounded text-xs hover:bg-slate-700 text-left flex items-center gap-2">
                                🐢 바다거북이
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 3. 장비 모드 옵션 -->
                <div id="panelEquip" class="space-y-4 hidden">
                    <div class="space-y-2">
                        <span class="text-xs text-slate-400 font-bold block">🫧 기포기(산소 공급기) 배치</span>
                        <p class="text-xs text-slate-500">기포기 배치 버튼을 누른 후 어항 바닥 위치를 클릭하여 기포기 위치를 자유롭게 이동하세요.</p>
                        <button onclick="selectTool('moveAerator')" id="tool_moveAerator" class="w-full tool-btn p-2.5 border border-cyan-500/40 bg-cyan-950/30 text-cyan-300 rounded text-xs hover:bg-cyan-900/40 flex items-center justify-center gap-2 font-bold">
                            🫧 기포기 위치 재지정/배치
                        </button>
                    </div>

                    <div class="space-y-2 pt-2 border-t border-slate-800">
                        <label class="text-xs text-slate-400 font-bold block">🌡️ 수온 설정</label>
                        <input type="range" id="tempSlider" min="15" max="32" value="24" oninput="updateTemp(this.value)" class="w-full accent-cyan-500">
                        <div class="flex justify-between text-[10px] text-slate-500">
                            <span>15°C (차가움)</span>
                            <span>24°C (적정)</span>
                            <span>32°C (고온)</span>
                        </div>
                    </div>

                    <div class="space-y-2 pt-2 border-t border-slate-800">
                        <label class="text-xs text-slate-400 font-bold block">💡 조명 필터 색상</label>
                        <div class="flex items-center space-x-3">
                            <input type="color" id="lightColor" value="#00ffff" onchange="updateLightColor(this.value)" class="w-10 h-8 bg-transparent cursor-pointer rounded">
                            <span id="lightColorDisp" class="text-xs text-slate-400">네온 블루조명</span>
                        </div>
                    </div>
                </div>

                <!-- 하단 초기화 및 액션 버튼 -->
                <div class="pt-4 border-t border-slate-800 space-y-2">
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="cleanAllPoop()" class="p-2 bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-bold rounded flex items-center justify-center gap-1">
                            ✨ 똥/오염 전체 청소
                        </button>
                        <button onclick="clearAll()" class="p-2 bg-rose-700 hover:bg-rose-600 text-white text-xs font-bold rounded flex items-center justify-center gap-1">
                            🔄 어항 전체 초기화
                        </button>
                    </div>
                </div>

            </div>
        </aside>

        <!-- 우측 메인 어항 캔버스 영역 -->
        <main class="flex-1 bg-slate-950 p-4 flex flex-col items-center justify-center relative overflow-hidden">
            
            <div id="tankContainer" class="relative rounded-2xl overflow-hidden border-4 border-slate-700 shadow-2xl bg-gradient-to-b from-sky-900 via-blue-950 to-slate-950">
                <!-- 캔버스 Layer -->
                <canvas id="aquariumCanvas" width="800" height="500" class="block"></canvas>

                <!-- 캔버스 오버레이 팁/안내 -->
                <div class="absolute bottom-3 left-4 pointer-events-none bg-slate-900/80 px-3 py-1 rounded text-xs text-slate-300 backdrop-blur-sm border border-slate-700/50">
                    💡 <span id="toolTip">파우더 원소: 드래그하여 모래/소일/수초 씨앗을 배치하세요.</span>
                </div>
            </div>

        </main>
    </div>

    <script>
        // --- 글로벌 변수 및 설정 ---
        const canvas = document.getElementById('aquariumCanvas');
        const ctx = canvas.getContext('2d');

        const WIDTH = 800;
        const HEIGHT = 500;
        const SCALE = 2; // 픽셀 스케일
        const GRID_W = WIDTH / SCALE; // 400
        const GRID_H = HEIGHT / SCALE; // 250

        // 파우더 입자 격자 (0: 공기/물, 1: 모래, 2: 소일, 3: 암석, 4: 유목, 5: 씨앗, 6: 먹이, 7: 똥, 8: 수초줄기)
        const grid = new Uint8Array(GRID_W * GRID_H);
        const colorGrid = new Uint32Array(GRID_W * GRID_H);

        // 어항 관리 상태
        let tankType = 'fresh'; // 'fresh' | 'marine'
        let currentTool = 'sand';
        let brushSize = 3;
        let waterTemperature = 24;
        let lightingColor = '#00ffff';
        let waterQuality = 100;

        // 기포기 위치 (기본값)
        let aeratorX = 200;
        let aeratorY = 240;

        // 생물 및 기포 파티클 목록
        let creatures = [];
        let bubbles = [];
        let plantSeeds = []; // 자라나는 수초 관리 {x, y, height, maxHeight}

        // 색상 정의
        const COLORS = {
            EMPTY: 0x00000000,
            SAND: 0xFF38BDF8, // ABGR 포맷 (리틀엔디안)
            SAND_HEX: [0xeab308, 0xd97706, 0xfacc15],
            SOIL_HEX: [0x3f2314, 0x54311c, 0x2b170c],
            ROCK_HEX: [0x64748b, 0x475569, 0x334155],
            WOOD_HEX: [0x78350f, 0x92400e, 0x451a03],
            SEED_HEX: [0x4ade80, 0x22c55e],
            FOOD_HEX: [0xf97316, 0xfb923c],
            POOP_GUPPY: 0x422006,  // 실똥
            POOP_TURTLE: 0x1c1917, // 둥근 똥
            PLANT_GREEN: [0x15803d, 0x16a34a, 0x22c55e]
        };

        // --- 초기화 및 실행 ---
        window.onload = () => {
            initSandGrid();
            spawnDefaultCreatures();
            requestAnimationFrame(gameLoop);
        };

        function setTankType(type) {
            tankType = type;
            const btnFresh = document.getElementById('tankTypeFresh');
            const btnMarine = document.getElementById('tankTypeMarine');
            
            if (type === 'fresh') {
                btnFresh.className = "px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-emerald-600 text-white shadow";
                btnMarine.className = "px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-slate-700 text-slate-300 hover:bg-slate-600";
            } else {
                btnMarine.className = "px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-cyan-600 text-white shadow";
                btnFresh.className = "px-2.5 py-0.5 rounded text-xs font-bold transition-all bg-slate-700 text-slate-300 hover:bg-slate-600";
            }
        }

        function switchTab(tab) {
            document.getElementById('panelPowder').classList.add('hidden');
            document.getElementById('panelCreature').classList.add('hidden');
            document.getElementById('panelEquip').classList.add('hidden');

            document.getElementById('tabPowder').className = "py-2 text-xs font-semibold rounded text-slate-400 hover:text-slate-200";
            document.getElementById('tabCreature').className = "py-2 text-xs font-semibold rounded text-slate-400 hover:text-slate-200";
            document.getElementById('tabEquip').className = "py-2 text-xs font-semibold rounded text-slate-400 hover:text-slate-200";

            if (tab === 'powder') {
                document.getElementById('panelPowder').classList.remove('hidden');
                document.getElementById('tabPowder').className = "py-2 text-xs font-semibold rounded text-cyan-400 bg-slate-800 border border-cyan-500/30";
            } else if (tab === 'creature') {
                document.getElementById('panelCreature').classList.remove('hidden');
                document.getElementById('tabCreature').className = "py-2 text-xs font-semibold rounded text-cyan-400 bg-slate-800 border border-cyan-500/30";
            } else if (tab === 'equip') {
                document.getElementById('panelEquip').classList.remove('hidden');
                document.getElementById('tabEquip').className = "py-2 text-xs font-semibold rounded text-cyan-400 bg-slate-800 border border-cyan-500/30";
            }
        }

        function selectTool(tool) {
            currentTool = tool;
            document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('btn-active'));
            const activeBtn = document.getElementById(`tool_${tool}`);
            if (activeBtn) activeBtn.classList.add('btn-active');

            const tipMap = {
                'sand': '금사 모래: 흐르는 모래 입자로 바닥을 채웁니다.',
                'soil': '영양 소일: 수초가 아주 잘 자라는 바닥재입니다.',
                'rock': '고정 암석: 물고기들의 안식처나 수초 발아 거치대가 됩니다.',
                'wood': '고정 유목: 자연스러운 어항 유목 구조물입니다.',
                'seed': '수초 씨앗: 모래/소일/암석/유목 위에 뿌리면 발아하여 수초가 자랍니다.',
                'food': '먹이 입자: 생물들이 먹고 느리게 포만감을 채웁니다.',
                'eraser': '픽셀 삭제펜: 지우고 싶은 구조물을 지웁니다.',
                'cleaner': '똥 청소펜: 똥과 오염물질을 깨끗이 청소합니다.',
                'moveAerator': '기포기 배치: 어항 내 원하는 바닥 위치를 클릭하여 기포기를 이동하세요.'
            };
            document.getElementById('toolTip').innerText = tipMap[tool] || '원하는 작업을 선택하세요.';
        }

        function updateBrushSize(val) {
            brushSize = parseInt(val);
            document.getElementById('brushSizeDisp').innerText = `${val}px`;
        }

        function updateTemp(val) {
            waterTemperature = parseInt(val);
            document.getElementById('tempDisp').innerText = `${val}°C`;
        }

        function updateLightColor(color) {
            lightingColor = color;
            document.getElementById('lightColorDisp').innerText = color;
        }

        function initSandGrid() {
            grid.fill(0);
            colorGrid.fill(0);
            // 언덕 모양 초기 모래 바닥 생성
            for (let x = 0; x < GRID_W; x++) {
                let h = Math.floor(Math.sin(x * 0.02) * 15 + Math.cos(x * 0.05) * 8 + 35);
                for (let y = GRID_H - h; y < GRID_H; y++) {
                    let idx = y * GRID_W + x;
                    grid[idx] = 1; // Sand
                    colorGrid[idx] = COLORS.SAND_HEX[Math.floor(Math.random() * COLORS.SAND_HEX.length)];
                }
            }
        }

        function spawnDefaultCreatures() {
            creatures = [];
            spawnCreature('guppy');
            spawnCreature('neon');
            spawnCreature('freshTurtle');
        }

        // --- 생물 클래스 정의 ---
        class Creature {
            constructor(type, x, y) {
                this.type = type; // guppy, neon, shrimp, freshTurtle, clownfish, blueTang, puffer, seaTurtle
                this.x = x;
                this.y = y;
                this.vx = (Math.random() - 0.5) * 1.2;
                this.vy = (Math.random() - 0.5) * 0.8;
                this.facingRight = this.vx > 0;
                
                // 포만감 및 상태
                this.satiety = 70; // 0~100 (포만감 천천히 차고 천천히 줄어듦)
                this.health = 100; // 0~100 (서식지 불일치 시 감염/사망)
                this.poopTimer = 0; // 먹이를 먹은 후 똥 누는 타이머

                // 생물별 속성 정의
                this.initProperties();
            }

            initProperties() {
                const props = {
                    'guppy': { isMarine: false, name: '구피', size: 10, speed: 0.8, color: '#f43f5e' },
                    'neon': { isMarine: false, name: '네온테트라', size: 8, speed: 1.1, color: '#06b6d4' },
                    'shrimp': { isMarine: false, name: '체리새우', size: 7, speed: 0.4, color: '#ef4444' },
                    'freshTurtle': { isMarine: false, name: '반수생거북이', size: 18, speed: 0.5, color: '#15803d' },
                    
                    'clownfish': { isMarine: true, name: '크라운피쉬', size: 10, speed: 0.9, color: '#f97316' },
                    'blueTang': { isMarine: true, name: '블루탱', size: 11, speed: 1.0, color: '#3b82f6' },
                    'puffer': { isMarine: true, name: '복어', size: 12, speed: 0.6, color: '#eab308' },
                    'seaTurtle': { isMarine: true, name: '바다거북이', size: 22, speed: 0.7, color: '#047857' }
                };
                Object.assign(this, props[this.type]);
            }

            update() {
                // 서식 환경(담수/해수) 체크
                const isEnvironmentMatch = (tankType === 'marine' && this.isMarine) || (tankType === 'fresh' && !this.isMarine);
                if (!isEnvironmentMatch) {
                    this.health -= 0.08; // 서식지 안 맞으면 체력 감소
                } else if (this.health < 100) {
                    this.health += 0.02;
                }

                // 포만감 지속 소비 (매우 천천히 감소)
                this.satiety -= 0.008;
                if (this.satiety < 0) this.satiety = 0;

                // 먹이 탐색 AI
                if (this.satiety < 80) {
                    this.searchFood();
                }

                // 이동 및 벽 충돌
                this.x += this.vx;
                this.y += this.vy;

                if (this.vx !== 0) this.facingRight = this.vx > 0;

                const margin = 20;
                if (this.x < margin) { this.x = margin; this.vx *= -1; }
                if (this.x > GRID_W - margin) { this.x = GRID_W - margin; this.vx *= -1; }
                if (this.y < margin) { this.y = margin; this.vy *= -1; }
                if (this.y > GRID_H - 40) { this.y = GRID_H - 40; this.vy *= -1; }

                // 무작위 방향 전환
                if (Math.random() < 0.02) {
                    this.vx += (Math.random() - 0.5) * 0.3;
                    this.vy += (Math.random() - 0.5) * 0.2;
                    // 속도 제한
                    const currentSpeed = Math.hypot(this.vx, this.vy);
                    if (currentSpeed > this.speed) {
                        this.vx = (this.vx / currentSpeed) * this.speed;
                        this.vy = (this.vy / currentSpeed) * this.speed;
                    }
                }

                // 소화 후 똥 배출 파이프라인
                if (this.poopTimer > 0) {
                    this.poopTimer--;
                    if (this.poopTimer === 0) {
                        this.producePoop();
                    }
                }
            }

            searchFood() {
                // 주변 픽셀 내 먹이(타입 6) 검색
                const gx = Math.floor(this.x);
                const gy = Math.floor(this.y);
                const searchRadius = 25;

                for (let dy = -searchRadius; dy <= searchRadius; dy += 2) {
                    for (let dx = -searchRadius; dx <= searchRadius; dx += 2) {
                        let nx = gx + dx;
                        let ny = gy + dy;
                        if (nx >= 0 && nx < GRID_W && ny >= 0 && ny < GRID_H) {
                            let idx = ny * GRID_W + nx;
                            if (grid[idx] === 6) { // 먹이 발견
                                // 먹이 쪽으로 약간 이동
                                this.vx += dx > 0 ? 0.05 : -0.05;
                                this.vy += dy > 0 ? 0.05 : -0.05;

                                // 먹이 섭취
                                if (Math.abs(dx) <= 3 && Math.abs(dy) <= 3) {
                                    grid[idx] = 0; // 먹이 제거
                                    colorGrid[idx] = 0;
                                    this.satiety = Math.min(100, this.satiety + 6); // 먹었을 때 느리게 참 (6씩 증가)
                                    this.poopTimer = 300 + Math.floor(Math.random() * 200); // 일정 후 똥 누기
                                    return;
                                }
                            }
                        }
                    }
                }
            }

            producePoop() {
                const gx = Math.floor(this.x);
                const gy = Math.floor(this.y);
                const idx = gy * GRID_W + gx;

                // 어종별 똥 형태 다르게 생성
                if (grid[idx] === 0) {
                    grid[idx] = 7; // Poop
                    if (this.type.includes('Turtle')) {
                        colorGrid[idx] = COLORS.POOP_TURTLE;
                    } else {
                        colorGrid[idx] = COLORS.POOP_GUPPY;
                    }
                }
            }

            draw() {
                ctx.save();
                ctx.translate(this.x * SCALE, this.y * SCALE);
                if (!this.facingRight) ctx.scale(-1, 1);

                // 사망/병듦 오라 효과
                if (this.health < 60) {
                    ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
                    ctx.beginPath();
                    ctx.arc(0, 0, this.size * 0.8, 0, Math.PI * 2);
                    ctx.fill();
                }

                // 개체별 픽셀 아트 렌더링
                this.drawPixelArt();

                // 포만감 / 체력 바 (선택적 시각화)
                ctx.restore();
            }

            drawPixelArt() {
                const s = 1.2; // 픽셀 배율
                ctx.fillStyle = this.color;

                if (this.type === 'freshTurtle' || this.type === 'seaTurtle') {
                    // 거북이 픽셀 등껍질 및 지느러미
                    ctx.fillStyle = this.type === 'seaTurtle' ? '#047857' : '#15803d';
                    ctx.fillRect(-8 * s, -6 * s, 16 * s, 12 * s); // 등껍질
                    ctx.fillStyle = '#a3e635';
                    ctx.fillRect(8 * s, -3 * s, 5 * s, 6 * s); // 머리
                    // 지느러미 / 발
                    ctx.fillStyle = '#166534';
                    ctx.fillRect(-6 * s, -9 * s, 5 * s, 4 * s);
                    ctx.fillRect(-6 * s, 5 * s, 5 * s, 4 * s);
                    ctx.fillRect(3 * s, -9 * s, 6 * s, 4 * s);
                    ctx.fillRect(3 * s, 5 * s, 6 * s, 4 * s);
                } else if (this.type === 'clownfish') {
                    // 흰동가리 (주황 + 흰 줄무늬)
                    ctx.fillRect(-6 * s, -4 * s, 12 * s, 8 * s);
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(-2 * s, -4 * s, 3 * s, 8 * s);
                    ctx.fillRect(3 * s, -3 * s, 2 * s, 6 * s);
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(4 * s, -2 * s, 1.5 * s, 1.5 * s); // 눈
                } else if (this.type === 'blueTang') {
                    // 블루탱 (파랑 + 노랑 꼬리)
                    ctx.fillRect(-6 * s, -4 * s, 10 * s, 8 * s);
                    ctx.fillStyle = '#facc15'; // 노란 꼬리
                    ctx.fillRect(-10 * s, -3 * s, 4 * s, 6 * s);
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(-2 * s, -2 * s, 5 * s, 4 * s); // 검은 무늬
                } else {
                    // 일반 물고기 형태 (구피, 네온, 등)
                    ctx.fillRect(-5 * s, -3 * s, 10 * s, 6 * s);
                    ctx.fillStyle = '#fef08a'; // 꼬리
                    ctx.fillRect(-9 * s, -4 * s, 4 * s, 8 * s);
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(3 * s, -2 * s, 2 * s, 2 * s); // 눈
                }
            }
        }

        function spawnCreature(type) {
            const x = Math.random() * (GRID_W - 80) + 40;
            const y = Math.random() * (GRID_H - 120) + 40;
            creatures.push(new Creature(type, x, y));
        }

        // --- 물리 시뮬레이션 및 샌드박스 업데이트 ---
        function updatePhysics() {
            // 아래에서부터 파우더 격자 물리 업데이트
            for (let y = GRID_H - 2; y >= 0; y--) {
                for (let x = 0; x < GRID_W; x++) {
                    let idx = y * GRID_W + x;
                    let type = grid[idx];

                    if (type === 1 || type === 2 || type === 6 || type === 7) { 
                        // 모래(1), 소일(2), 먹이(6), 똥(7) 중력 및 흐름
                        let below = (y + 1) * GRID_W + x;
                        let belowLeft = (y + 1) * GRID_W + (x - 1);
                        let belowRight = (y + 1) * GRID_W + (x + 1);

                        if (grid[below] === 0) {
                            grid[below] = type;
                            colorGrid[below] = colorGrid[idx];
                            grid[idx] = 0;
                            colorGrid[idx] = 0;
                        } else if (x > 0 && grid[belowLeft] === 0) {
                            grid[belowLeft] = type;
                            colorGrid[belowLeft] = colorGrid[idx];
                            grid[idx] = 0;
                            colorGrid[idx] = 0;
                        } else if (x < GRID_W - 1 && grid[belowRight] === 0) {
                            grid[belowRight] = type;
                            colorGrid[belowRight] = colorGrid[idx];
                            grid[idx] = 0;
                            colorGrid[idx] = 0;
                        }
                    } else if (type === 5) {
                        // 수초 씨앗(5): 모래/소일/암석/유목 표면에 닿으면 수초로 발아
                        let below = (y + 1) * GRID_W + x;
                        let bType = grid[below];
                        if (bType >= 1 && bType <= 4) {
                            // 발아 시작
                            plantSeeds.push({ x: x, y: y, height: 0, maxHeight: 15 + Math.floor(Math.random() * 20) });
                            grid[idx] = 8; // 수초 줄기
                            colorGrid[idx] = COLORS.PLANT_GREEN[Math.floor(Math.random() * COLORS.PLANT_GREEN.length)];
                        } else if (grid[below] === 0) {
                            // 떨어짐
                            grid[below] = 5;
                            colorGrid[below] = colorGrid[idx];
                            grid[idx] = 0;
                            colorGrid[idx] = 0;
                        }
                    }
                }
            }

            // 수초 성장의 업데이트
            if (Math.random() < 0.2) {
                plantSeeds.forEach((plant, pIdx) => {
                    if (plant.height < plant.maxHeight) {
                        let topY = plant.y - plant.height;
                        if (topY - 1 >= 0) {
                            let upIdx = (topY - 1) * GRID_W + plant.x;
                            if (grid[upIdx] === 0) {
                                grid[upIdx] = 8; // 수초 계속 성장
                                colorGrid[upIdx] = COLORS.PLANT_GREEN[Math.floor(Math.random() * COLORS.PLANT_GREEN.length)];
                                plant.height++;
                            }
                        }
                    }
                });
            }

            // 기포기 산소 방출 시뮬레이션
            if (Math.random() < 0.6) {
                bubbles.push({
                    x: aeratorX + (Math.random() * 8 - 4),
                    y: aeratorY,
                    vy: 0.8 + Math.random() * 0.8,
                    size: 1 + Math.random() * 2
                });
            }

            // 기포 올라가기
            for (let i = bubbles.length - 1; i >= 0; i--) {
                let b = bubbles[i];
                b.y -= b.vy;
                b.x += Math.sin(b.y * 0.05) * 0.3;
                if (b.y <= 10) {
                    bubbles.splice(i, 1);
                }
            }
        }

        // --- 마우스 및 툴 입력을 사용한 파우더 그리기 ---
        let isDrawing = false;

        canvas.addEventListener('mousedown', (e) => {
            isDrawing = true;
            handlePointer(e);
        });
        canvas.addEventListener('mousemove', (e) => {
            if (isDrawing) handlePointer(e);
        });
        window.addEventListener('mouseup', () => isDrawing = false);

        function handlePointer(e) {
            const rect = canvas.getBoundingClientRect();
            const mx = Math.floor((e.clientX - rect.left) / SCALE);
            const my = Math.floor((e.clientY - rect.top) / SCALE);

            if (currentTool === 'moveAerator') {
                aeratorX = Math.max(20, Math.min(GRID_W - 20, mx));
                aeratorY = Math.max(50, Math.min(GRID_H - 20, my));
                return;
            }

            const r = brushSize;
            for (let dy = -r; dy <= r; dy++) {
                for (let dx = -r; dx <= r; dx++) {
                    if (dx*dx + dy*dy <= r*r) {
                        let gx = mx + dx;
                        let gy = my + dy;
                        if (gx >= 0 && gx < GRID_W && gy >= 0 && gy < GRID_H) {
                            let idx = gy * GRID_W + gx;

                            if (currentTool === 'eraser') {
                                grid[idx] = 0;
                                colorGrid[idx] = 0;
                            } else if (currentTool === 'cleaner') {
                                if (grid[idx] === 7) { // 똥만 청소
                                    grid[idx] = 0;
                                    colorGrid[idx] = 0;
                                }
                            } else if (currentTool === 'sand') {
                                grid[idx] = 1;
                                colorGrid[idx] = COLORS.SAND_HEX[Math.floor(Math.random() * COLORS.SAND_HEX.length)];
                            } else if (currentTool === 'soil') {
                                grid[idx] = 2;
                                colorGrid[idx] = COLORS.SOIL_HEX[Math.floor(Math.random() * COLORS.SOIL_HEX.length)];
                            } else if (currentTool === 'rock') {
                                grid[idx] = 3;
                                colorGrid[idx] = COLORS.ROCK_HEX[Math.floor(Math.random() * COLORS.ROCK_HEX.length)];
                            } else if (currentTool === 'wood') {
                                grid[idx] = 4;
                                colorGrid[idx] = COLORS.WOOD_HEX[Math.floor(Math.random() * COLORS.WOOD_HEX.length)];
                            } else if (currentTool === 'seed') {
                                if (grid[idx] === 0) {
                                    grid[idx] = 5;
                                    colorGrid[idx] = COLORS.SEED_HEX[Math.floor(Math.random() * COLORS.SEED_HEX.length)];
                                }
                            } else if (currentTool === 'food') {
                                if (grid[idx] === 0 && Math.random() < 0.3) {
                                    grid[idx] = 6;
                                    colorGrid[idx] = COLORS.FOOD_HEX[Math.floor(Math.random() * COLORS.FOOD_HEX.length)];
                                }
                            }
                        }
                    }
                }
            }
        }

        function cleanAllPoop() {
            for (let i = 0; i < grid.length; i++) {
                if (grid[i] === 7) {
                    grid[i] = 0;
                    colorGrid[i] = 0;
                }
            }
        }

        function clearAll() {
            grid.fill(0);
            colorGrid.fill(0);
            creatures = [];
            plantSeeds = [];
            bubbles = [];
        }

        // --- 메인 게임 루프 & 프레임 렌더링 ---
        function gameLoop() {
            updatePhysics();

            // 생물 업데이트 및 사망 관리
            for (let i = creatures.length - 1; i >= 0; i--) {
                let c = creatures[i];
                c.update();
                if (c.health <= 0) {
                    creatures.splice(i, 1); // 체력 고갈 시 사망
                }
            }

            // 렌더링 시작
            ctx.clearRect(0, 0, WIDTH, HEIGHT);

            // 1. 파우더 입자 격자 그리기
            const imgData = ctx.createImageData(WIDTH, HEIGHT);
            const data = imgData.data;

            for (let gy = 0; gy < GRID_H; gy++) {
                for (let gx = 0; gx < GRID_W; gx++) {
                    let gIdx = gy * GRID_W + gx;
                    let type = grid[gIdx];

                    if (type !== 0) {
                        let color = colorGrid[gIdx];
                        let r = (color >> 16) & 0xFF;
                        let g = (color >> 8) & 0xFF;
                        let b = color & 0xFF;

                        // 스케일 확대 (SCALE x SCALE 픽셀로 변환)
                        for (let dy = 0; dy < SCALE; dy++) {
                            for (let dx = 0; dx < SCALE; dx++) {
                                let px = gx * SCALE + dx;
                                let py = gy * SCALE + dy;
                                let pIdx = (py * WIDTH + px) * 4;

                                data[pIdx] = r;
                                data[pIdx + 1] = g;
                                data[pIdx + 2] = b;
                                data[pIdx + 3] = 255;
                            }
                        }
                    }
                }
            }
            ctx.putImageData(imgData, 0, 0);

            // 2. 기포기 기계 및 bubble 파티클 그리기
            // 기포기 몸체
            ctx.fillStyle = '#475569';
            ctx.fillRect((aeratorX - 6) * SCALE, (aeratorY - 4) * SCALE, 12 * SCALE, 8 * SCALE);
            ctx.fillStyle = '#38bdf8';
            ctx.fillRect((aeratorX - 2) * SCALE, (aeratorY - 6) * SCALE, 4 * SCALE, 3 * SCALE);

            // 기포 방출
            ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
            bubbles.forEach(b => {
                ctx.beginPath();
                ctx.arc(b.x * SCALE, b.y * SCALE, b.size, 0, Math.PI * 2);
                ctx.fill();
            });

            // 3. 생물 객체 그리기
            creatures.forEach(c => c.draw());

            // 4. 수질 오염 및 조명 필터 효과
            ctx.fillStyle = lightingColor;
            ctx.globalCompositeOperation = 'overlay';
            ctx.globalAlpha = 0.15;
            ctx.fillRect(0, 0, WIDTH, HEIGHT);
            ctx.globalCompositeOperation = 'source-over';
            ctx.globalAlpha = 1.0;

            // UI 통계 업데이트
            document.getElementById('fishCountDisp').innerText = creatures.length;

            requestAnimationFrame(gameLoop);
        }
    </script>
</body>
</html>
