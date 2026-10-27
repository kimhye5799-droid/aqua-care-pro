<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>어항선배 - 초보 물집사를 위한 AI 수족관 케어 솔루션</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts: Neo Dunggeunmo (Pixel feel) & Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DungGeunMo&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        aqua: {
                            50: '#f0fdfa',
                            100: '#ccfbf1',
                            400: '#2dd4bf',
                            500: '#14b8a6',
                            600: '#0d9488',
                            800: '#115e59',
                            900: '#134e4a',
                            950: '#042f2e',
                        },
                        deepbg: '#08101e',
                        cardbg: 'rgba(15, 23, 42, 0.75)',
                    },
                    fontFamily: {
                        pixel: ['DungGeunMo', 'monospace'],
                        sans: ['Noto Sans KR', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #050b14;
            background-image: 
                radial-gradient(at 20% 20%, rgba(13, 148, 136, 0.25) 0px, transparent 50%),
                radial-gradient(at 80% 80%, rgba(14, 116, 144, 0.2) 0px, transparent 50%),
                radial-gradient(at 50% 0%, rgba(2, 132, 199, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: #f1f5f9;
        }

        .glass-card {
            background: rgba(13, 27, 42, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(45, 212, 191, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .glass-card-hover:hover {
            border-color: rgba(45, 212, 191, 0.5);
            box-shadow: 0 8px 32px 0 rgba(45, 212, 191, 0.2);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(5, 11, 20, 0.8);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(45, 212, 191, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(45, 212, 191, 0.6);
        }

        /* Bubble Animation */
        .bubble {
            position: absolute;
            background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.1));
            border-radius: 50%;
            pointer-events: none;
            animation: floatUp 8s infinite ease-in;
            opacity: 0.6;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(100vh) scale(0.3);
                opacity: 0;
            }
            20% { opacity: 0.6; }
            100% {
                transform: translateY(-10vh) scale(1.2);
                opacity: 0;
            }
        }

        /* Pixel style border */
        .pixel-box {
            box-shadow: 
                -2px 0 0 0 #2dd4bf,
                2px 0 0 0 #2dd4bf,
                0 -2px 0 0 #2dd4bf,
                0 2px 0 0 #2dd4bf;
        }
    </style>
</head>
<body class="font-sans min-h-screen flex flex-col relative overflow-x-hidden">

    <!-- Ambient Floating Bubbles -->
    <div id="bubble-container" class="fixed inset-0 pointer-events-none z-0"></div>

    <!-- Header / Navigation -->
    <header class="sticky top-0 z-50 glass-card border-b border-teal-500/30 px-4 lg:px-8 py-3">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-3 cursor-pointer" onclick="switchTab('chat')">
                <div class="w-10 h-10 rounded-lg bg-teal-500/20 border border-teal-400 flex items-center justify-center text-teal-300 font-pixel text-xl shadow-[0_0_12px_rgba(45,212,191,0.4)]">
                    🐟
                </div>
                <div>
                    <h1 class="font-pixel text-xl lg:text-2xl text-teal-300 tracking-wider flex items-center gap-2">
                        어항선배 <span class="text-xs font-sans px-2 py-0.5 rounded bg-teal-500/20 text-teal-400 border border-teal-500/40">PRO v2.0</span>
                    </h1>
                    <p class="text-xs text-slate-400 hidden sm:block">초보 물집사를 위한 AI 스마트 케어 솔루션</p>
                </div>
            </div>

            <!-- Navigation Tabs -->
            <nav class="flex items-center space-x-1 sm:space-x-2 bg-slate-900/80 p-1 rounded-xl border border-teal-900/60 text-xs sm:text-sm font-medium">
                <button onclick="switchTab('chat')" id="nav-chat" class="tab-btn px-3 py-2 rounded-lg transition-all flex items-center gap-1.5 bg-teal-600 text-white shadow">
                    <i class="fa-solid me-1 fa-comments"></i> AI 상담
                </button>
                <button onclick="switchTab('compatibility')" id="nav-compatibility" class="tab-btn px-3 py-2 rounded-lg transition-all text-slate-400 hover:text-teal-300 flex items-center gap-1.5">
                    <i class="fa-solid fa-code-compare me-1"></i> 합사 진단기
                </button>
                <button onclick="switchTab('calc')" id="nav-calc" class="tab-btn px-3 py-2 rounded-lg transition-all text-slate-400 hover:text-teal-300 flex items-center gap-1.5">
                    <i class="fa-solid fa-calculator me-1"></i> 물용량 계산
                </button>
                <button onclick="switchTab('water')" id="nav-water" class="tab-btn px-3 py-2 rounded-lg transition-all text-slate-400 hover:text-teal-300 flex items-center gap-1.5">
                    <i class="fa-solid fa-list-check me-1"></i> 물잡이 스케줄
                </button>
            </nav>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 z-10 relative">

        <!-- ================= 1. AI 어항선배 Q&A TAB ================= -->
        <section id="tab-chat" class="tab-content grid grid-cols-1 lg:grid-cols-4 gap-6">
            <!-- Left Sidebar: Character Profile & Quick Questions -->
            <div class="lg:col-span-1 space-y-4">
                <!-- Character Profile Card -->
                <div class="glass-card rounded-2xl p-5 border border-teal-500/30 text-center relative overflow-hidden">
                    <div class="absolute -top-10 -right-10 w-28 h-28 bg-teal-500/10 rounded-full blur-2xl"></div>
                    
                    <div class="relative inline-block mb-3">
                        <div class="w-24 h-24 mx-auto rounded-full bg-gradient-to-tr from-teal-600 to-cyan-400 p-1 shadow-[0_0_20px_rgba(45,212,191,0.4)]">
                            <div class="w-full h-full rounded-full bg-slate-900 flex items-center justify-center text-4xl">
                                🧙‍♂️🐠
                            </div>
                        </div>
                        <span class="absolute bottom-0 right-0 bg-emerald-500 text-slate-950 font-bold text-[10px] px-2 py-0.5 rounded-full border border-slate-900 flex items-center gap-1">
                            <span class="w-1.5 h-1.5 rounded-full bg-slate-950 animate-ping"></span> AI ON
                        </span>
                    </div>

                    <h2 class="font-pixel text-xl text-teal-300">어항선배</h2>
                    <p class="text-xs text-teal-400/80 mt-1 font-mono">경력 15년 차 물생활 마스터 AI</p>
                    <p class="text-xs text-slate-300 mt-3 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        "안녕 초보 물집사! 물고기가 용궁 갈까 봐 걱정인가? 물잡이부터 어종 합사, 환수 주기까지 뭐든지 물어보게나!"
                    </p>
                </div>

                <!-- Quick Questions Widget -->
                <div class="glass-card rounded-2xl p-4 border border-slate-800">
                    <h3 class="text-xs font-semibold text-teal-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <i class="fa-solid fa-bolt text-amber-400"></i> 초보 필수 퀵 질문
                    </h3>
                    <div class="space-y-2">
                        <button onclick="askQuickQuestion('어항 물잡이가 뭔가요? 초기 세팅하는 법 알려주세요.')" class="w-full text-left text-xs bg-slate-800/80 hover:bg-teal-950/60 hover:text-teal-300 text-slate-300 p-2.5 rounded-lg border border-slate-700/60 transition duration-200 flex items-center justify-between group">
                            <span>🧪 물잡이란 무엇인가요?</span>
                            <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
                        </button>
                        <button onclick="askQuickQuestion('물고기가 자꾸 수면에 떠서 뻐끔거려요. 이유가 뭔가요?')" class="w-full text-left text-xs bg-slate-800/80 hover:bg-teal-950/60 hover:text-teal-300 text-slate-300 p-2.5 rounded-lg border border-slate-700/60 transition duration-200 flex items-center justify-between group">
                            <span>🫧 수면 뻐끔거림 해결법</span>
                            <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
                        </button>
                        <button onclick="askQuickQuestion('환수는 얼마나 자주, 몇 %씩 해줘야 하나요?')" class="w-full text-left text-xs bg-slate-800/80 hover:bg-teal-950/60 hover:text-teal-300 text-slate-300 p-2.5 rounded-lg border border-slate-700/60 transition duration-200 flex items-center justify-between group">
                            <span>🪣 올바른 환수 주기 및 방법</span>
                            <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
                        </button>
                        <button onclick="askQuickQuestion('어항에 백탁 현상이 왔어요. 어떻게 해야 되나요?')" class="w-full text-left text-xs bg-slate-800/80 hover:bg-teal-950/60 hover:text-teal-300 text-slate-300 p-2.5 rounded-lg border border-slate-700/60 transition duration-200 flex items-center justify-between group">
                            <span>🌫️ 백탁 현상 대처 가이드</span>
                            <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
                        </button>
                        <button onclick="askQuickQuestion('구피와 체리새우 한 어항에서 같이 키워도 되나요?')" class="w-full text-left text-xs bg-slate-800/80 hover:bg-teal-950/60 hover:text-teal-300 text-slate-300 p-2.5 rounded-lg border border-slate-700/60 transition duration-200 flex items-center justify-between group">
                            <span>🦐 구피 x 체리새우 합사 가능 여부</span>
                            <i class="fa-solid fa-chevron-right text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right Area: Chat Window -->
            <div class="lg:col-span-3 flex flex-col h-[650px] glass-card rounded-2xl border border-teal-500/30 overflow-hidden">
                <!-- Chat Header -->
                <div class="bg-slate-900/90 px-5 py-3.5 border-b border-teal-500/20 flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-teal-400 animate-pulse"></span>
                        <span class="text-sm font-semibold text-slate-200">어항선배 1:1 상담실</span>
                    </div>
                    <button onclick="clearChat()" class="text-xs text-slate-400 hover:text-rose-400 transition flex items-center gap-1">
                        <i class="fa-solid fa-trash-can"></i> 대화 초기화
                    </button>
                </div>

                <!-- Chat Scroll Area -->
                <div id="chat-box" class="flex-1 p-4 overflow-y-auto space-y-4">
                    <!-- Welcome Assistant Message -->
                    <div class="flex items-start gap-3">
                        <div class="w-9 h-9 rounded-full bg-teal-500/20 border border-teal-400 flex items-center justify-center text-lg flex-shrink-0">
                            🧙‍♂️
                        </div>
                        <div class="max-w-[80%] bg-slate-800/90 border border-teal-500/20 rounded-2xl rounded-tl-none p-4 text-sm text-slate-200 leading-relaxed shadow">
                            반갑네 물집사! 🐟<br>어항 사이즈, 여과기 종류, 물고기 상태 등 무엇이든 편하게 물어보게나. 친절하고 정확하게 가이드해주지!
                        </div>
                    </div>
                </div>

                <!-- Chat Input Area -->
                <div class="p-3 bg-slate-900/90 border-t border-teal-500/20">
                    <form id="chat-form" onsubmit="handleChatSubmit(event)" class="flex gap-2">
                        <input type="text" id="chat-input" placeholder="어항선배에게 물생활 질문하기... (예: 구피 환수 방법 알려줘)" 
                            class="flex-1 bg-slate-950/80 border border-slate-700 focus:border-teal-400 text-slate-100 text-sm rounded-xl px-4 py-3 outline-none transition placeholder:text-slate-500">
                        <button type="submit" id="send-btn" class="bg-teal-600 hover:bg-teal-500 text-white px-5 py-3 rounded-xl font-medium text-sm transition flex items-center gap-2 shadow-[0_0_15px_rgba(45,212,191,0.3)]">
                            <span>전송</span>
                            <i class="fa-solid fa-paper-plane text-xs"></i>
                        </button>
                    </form>
                </div>
            </div>
        </section>


        <!-- ================= 2. COMPATIBILITY CHECKER TAB ================= -->
        <section id="tab-compatibility" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-2xl p-6 border border-teal-500/30">
                <div class="max-w-2xl">
                    <h2 class="font-pixel text-2xl text-teal-300 flex items-center gap-2">
                        <i class="fa-solid fa-heart-circle-bolt text-teal-400"></i> 어종/생물 합사 가능 여부 진단기
                    </h2>
                    <p class="text-sm text-slate-400 mt-1">
                        어항에 함께 키우고 싶은 생물 2종을 선택하세요. 공격성, 수온, 수질, 크기 차이를 분석하여 궁합을 진단합니다.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                    <!-- Fish 1 Selection -->
                    <div class="bg-slate-900/70 p-5 rounded-xl border border-slate-800">
                        <label class="block text-xs font-semibold text-teal-400 uppercase tracking-wider mb-2">첫 번째 생물 선택</label>
                        <select id="fish1" onchange="checkCompatibility()" class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-sm rounded-lg p-3 outline-none focus:border-teal-400">
                            <!-- Populated by JS -->
                        </select>
                        <div id="fish1-info" class="mt-4 p-3 bg-slate-950/60 rounded-lg text-xs text-slate-400 space-y-1"></div>
                    </div>

                    <!-- Fish 2 Selection -->
                    <div class="bg-slate-900/70 p-5 rounded-xl border border-slate-800">
                        <label class="block text-xs font-semibold text-teal-400 uppercase tracking-wider mb-2">두 번째 생물 선택</label>
                        <select id="fish2" onchange="checkCompatibility()" class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-sm rounded-lg p-3 outline-none focus:border-teal-400">
                            <!-- Populated by JS -->
                        </select>
                        <div id="fish2-info" class="mt-4 p-3 bg-slate-950/60 rounded-lg text-xs text-slate-400 space-y-1"></div>
                    </div>
                </div>

                <!-- Compatibility Result Box -->
                <div id="compatibility-result" class="mt-6 p-6 rounded-xl bg-slate-900/90 border border-teal-500/30 text-center transition-all">
                    <div class="text-slate-400 text-sm">생물 두 종류를 선택하시면 진단 결과가 표시됩니다.</div>
                </div>
            </div>
        </section>


        <!-- ================= 3. WATER VOLUME & CAPACITY CALCULATOR TAB ================= -->
        <section id="tab-calc" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Inputs Section -->
                <div class="lg:col-span-1 glass-card rounded-2xl p-6 border border-teal-500/30 space-y-5">
                    <h2 class="font-pixel text-xl text-teal-300 flex items-center gap-2">
                        <i class="fa-solid fa-calculator"></i> 어항 치수 입력
                    </h2>

                    <div>
                        <label class="block text-xs text-slate-400 mb-1">어항 가로 (cm)</label>
                        <input type="number" id="tank-w" value="45" oninput="calculateWaterVolume()" class="w-full bg-slate-950 border border-slate-700 text-teal-300 font-mono text-lg rounded-xl p-3 outline-none focus:border-teal-400">
                    </div>

                    <div>
                        <label class="block text-xs text-slate-400 mb-1">어항 세로 (폭) (cm)</label>
                        <input type="number" id="tank-d" value="30" oninput="calculateWaterVolume()" class="w-full bg-slate-950 border border-slate-700 text-teal-300 font-mono text-lg rounded-xl p-3 outline-none focus:border-teal-400">
                    </div>

                    <div>
                        <label class="block text-xs text-slate-400 mb-1">어항 높이 (cm)</label>
                        <input type="number" id="tank-h" value="30" oninput="calculateWaterVolume()" class="w-full bg-slate-950 border border-slate-700 text-teal-300 font-mono text-lg rounded-xl p-3 outline-none focus:border-teal-400">
                    </div>

                    <div>
                        <label class="block text-xs text-slate-400 mb-1">바닥재 두께 (cm)</label>
                        <input type="number" id="substrate-h" value="3" oninput="calculateWaterVolume()" class="w-full bg-slate-950 border border-slate-700 text-teal-300 font-mono text-lg rounded-xl p-3 outline-none focus:border-teal-400">
                    </div>
                </div>

                <!-- Results Output Section -->
                <div class="lg:col-span-2 glass-card rounded-2xl p-6 border border-teal-500/30 flex flex-col justify-between">
                    <div>
                        <h2 class="font-pixel text-xl text-teal-300 mb-4 flex items-center gap-2">
                            <i class="fa-solid fa-chart-pie"></i> 계산 진단 결과
                        </h2>

                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                            <!-- Total Water -->
                            <div class="bg-slate-900/80 p-4 rounded-xl border border-teal-500/20 text-center">
                                <span class="text-xs text-slate-400">실제 총 물용량</span>
                                <div class="text-2xl sm:text-3xl font-bold font-mono text-cyan-300 mt-1" id="res-volume">0 L</div>
                                <span class="text-[11px] text-slate-500">바닥재/상단 여유공간 차감</span>
                            </div>

                            <!-- Recommended Fish Count -->
                            <div class="bg-slate-900/80 p-4 rounded-xl border border-teal-500/20 text-center">
                                <span class="text-xs text-slate-400">적정 물고기 마릿수</span>
                                <div class="text-2xl sm:text-3xl font-bold font-mono text-emerald-300 mt-1" id="res-fish">0 마리</div>
                                <span class="text-[11px] text-slate-500">소형종 (3~4cm) 기준</span>
                            </div>

                            <!-- Weekly Water Change -->
                            <div class="bg-slate-900/80 p-4 rounded-xl border border-teal-500/20 text-center">
                                <span class="text-xs text-slate-400">주간 환수 권장량 (30%)</span>
                                <div class="text-2xl sm:text-3xl font-bold font-mono text-amber-300 mt-1" id="res-waterchange">0 L</div>
                                <span class="text-[11px] text-slate-500">주 1회 기준</span>
                            </div>
                        </div>

                        <!-- Extra Advice Banner -->
                        <div class="bg-teal-950/40 p-4 rounded-xl border border-teal-500/30 text-xs sm:text-sm text-slate-300 space-y-2">
                            <div class="font-semibold text-teal-300 flex items-center gap-1.5">
                                <i class="fa-solid fa-circle-info"></i> 어항선배의 수용량 꿀팁
                            </div>
                            <ul class="list-disc list-inside space-y-1 text-slate-400 text-xs">
                                <li>어항 입수 초기에는 권장 마릿수의 **30~50%만 먼저 입수**시켜 여과 cycle을 잡는 것이 안전합니다.</li>
                                <li>체리새우나 소형 가재 등 갑각류는 오염원이 적어 물고기 대비 더 여유 있게 합사 가능합니다.</li>
                                <li>여과기 성능(스펀지, 걸이식, 외부여과기)에 따라 과밀 사육 시 환수 주기를 2~3일에 1회로 늘려주세요.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="mt-4 pt-4 border-t border-slate-800 text-right">
                        <button onclick="askQuickQuestion(`제 어항 물용량이 ${document.getElementById('res-volume').innerText}인데 추천하는 여과기와 생물 조합 알려주세요.`)" class="text-xs bg-teal-600 hover:bg-teal-500 text-white font-medium px-4 py-2.5 rounded-lg transition inline-flex items-center gap-1.5">
                            <i class="fa-solid fa-comments"></i> 이 용량에 맞는 추천 여과기 AI에 물어보기
                        </button>
                    </div>
                </div>
            </div>
        </section>


        <!-- ================= 4. WATER CYCLING SCHEDULER TAB ================= -->
        <section id="tab-water" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Scheduler Timeline -->
                <div class="lg:col-span-2 glass-card rounded-2xl p-6 border border-teal-500/30 space-y-4">
                    <h2 class="font-pixel text-2xl text-teal-300 flex items-center gap-2">
                        <i class="fa-solid fa-calendar-check text-teal-400"></i> 초기 30일 물잡이(여과) 스케줄러
                    </h2>
                    <p class="text-xs text-slate-400">
                        물고기가 생존할 수 있는 유익균(박테리아) 생태계를 형성하는 30일 코스 가이드입니다.
                    </p>

                    <div class="space-y-3 mt-4">
                        <!-- Step 1 -->
                        <div class="p-4 rounded-xl bg-slate-900/80 border border-teal-500/30 flex items-start gap-4">
                            <div class="w-12 h-12 rounded-lg bg-teal-500/20 border border-teal-400 font-pixel text-teal-300 text-sm flex items-center justify-center flex-shrink-0">
                                1~3일
                            </div>
                            <div class="space-y-1">
                                <h3 class="text-sm font-bold text-slate-200">1단계: 어항 세팅 및 박테리아제 투여</h3>
                                <p class="text-xs text-slate-400 leading-relaxed">
                                    바닥재 wash, 여과기 설치, 염소 제거된 물 채우기. 생박테리아제를 용량에 맞춰 투여하고 24시간 여과기를 연속 가동합니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 2 -->
                        <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-4">
                            <div class="w-12 h-12 rounded-lg bg-cyan-500/20 border border-cyan-400 font-pixel text-cyan-300 text-sm flex items-center justify-center flex-shrink-0">
                                4~7일
                            </div>
                            <div class="space-y-1">
                                <h3 class="text-sm font-bold text-slate-200">2단계: 박테리아 먹이 공급 (암모니아 발생)</h3>
                                <p class="text-xs text-slate-400 leading-relaxed">
                                    물고기 사료를 극소량 투여하여 암모니아 발생 유도. 물이 뿌옇게 흐려지는 **백탁 현상**이 올 수 있으나 박테리아 번식 과정이므로 정상입니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 3 -->
                        <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-4">
                            <div class="w-12 h-12 rounded-lg bg-amber-500/20 border border-amber-400 font-pixel text-amber-300 text-sm flex items-center justify-center flex-shrink-0">
                                8~14일
                            </div>
                            <div class="space-y-1">
                                <h3 class="text-sm font-bold text-slate-200">3단계: 아질산염 피크 및 첫 물잡이 고기 입수</h3>
                                <p class="text-xs text-slate-400 leading-relaxed">
                                    백탁이 맑게 걷히는 시기. 강인한 주노에 해당하는 '물잡이 특공대(제브라다니오 1~2마리)'를 입수하여 여과 생태계를 가속화합니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 4 -->
                        <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-4">
                            <div class="w-12 h-12 rounded-lg bg-emerald-500/20 border border-emerald-400 font-pixel text-emerald-300 text-sm flex items-center justify-center flex-shrink-0">
                                15~30일
                            </div>
                            <div class="space-y-1">
                                <h3 class="text-sm font-bold text-slate-200">4단계: 질산염 전환 & 메인 생물 단계적 입수</h3>
                                <p class="text-xs text-slate-400 leading-relaxed">
                                    여과 사이클 완결 단계. 주 1회 20~30% 환수를 시작하며, 키우고 싶은 메인 어종을 3~4일 간격으로 조금씩 나누어 입수합니다.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Interactive Checklist & State Diagnostic -->
                <div class="lg:col-span-1 glass-card rounded-2xl p-6 border border-teal-500/30 space-y-4">
                    <h2 class="font-pixel text-xl text-teal-300 flex items-center gap-2">
                        <i class="fa-solid fa-square-check"></i> 어항 상태 진단 체크
                    </h2>
                    <p class="text-xs text-slate-400">현재 어항 증상을 체크해 보세요.</p>

                    <div class="space-y-2 text-xs">
                        <label class="flex items-center gap-2.5 p-3 bg-slate-900/80 rounded-xl cursor-pointer border border-slate-800 hover:border-teal-500/40">
                            <input type="checkbox" id="chk-cloudy" onchange="diagnoseChecklist()" class="rounded accent-teal-400 w-4 h-4">
                            <span class="text-slate-300">물이 뿌옇고 불투명함 (백탁)</span>
                        </label>
                        <label class="flex items-center gap-2.5 p-3 bg-slate-900/80 rounded-xl cursor-pointer border border-slate-800 hover:border-teal-500/40">
                            <input type="checkbox" id="chk-foam" onchange="diagnoseChecklist()" class="rounded accent-teal-400 w-4 h-4">
                            <span class="text-slate-300">수면에 거품이 안 사라짐</span>
                        </label>
                        <label class="flex items-center gap-2.5 p-3 bg-slate-900/80 rounded-xl cursor-pointer border border-slate-800 hover:border-teal-500/40">
                            <input type="checkbox" id="chk-gasping" onchange="diagnoseChecklist()" class="rounded accent-teal-400 w-4 h-4">
                            <span class="text-slate-300">물고기가 수면에서 뻐끔거림</span>
                        </label>
                        <label class="flex items-center gap-2.5 p-3 bg-slate-900/80 rounded-xl cursor-pointer border border-slate-800 hover:border-teal-500/40">
                            <input type="checkbox" id="chk-algae" onchange="diagnoseChecklist()" class="rounded accent-teal-400 w-4 h-4">
                            <span class="text-slate-300">유리창/이끼에 녹조/갈조 발생</span>
                        </label>
                    </div>

                    <!-- Diagnostic Response Box -->
                    <div id="checklist-diagnosis" class="p-4 rounded-xl bg-slate-950/80 border border-teal-500/30 text-xs text-slate-300 min-h-[140px] leading-relaxed">
                        증상을 선택하시면 어항선배의 맞춤 처방법이 표시됩니다.
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-slate-800/80 bg-slate-950/80 py-4 px-6 text-center text-xs text-slate-500">
        <p>© 2026 어항선배 PRO — 초보 물집사를 위한 AI 통합 수족관 케어 스위트</p>
    </footer>

    <!-- JavaScript Application Logic -->
    <script>
        /* ================= 1. BUBBLE ANIMATION GENERATOR ================= */
        function createBubbles() {
            const container = document.getElementById('bubble-container');
            const bubbleCount = 15;
            for (let i = 0; i < bubbleCount; i++) {
                const bubble = document.createElement('div');
                bubble.className = 'bubble';
                const size = Math.random() * 16 + 6;
                bubble.style.width = `${size}px`;
                bubble.style.height = `${size}px`;
                bubble.style.left = `${Math.random() * 100}%`;
                bubble.style.animationDelay = `${Math.random() * 8}s`;
                bubble.style.animationDuration = `${Math.random() * 6 + 6}s`;
                container.appendChild(bubble);
            }
        }

        /* ================= 2. TAB NAVIGATION ================= */
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-teal-600', 'text-white', 'shadow');
                btn.classList.add('text-slate-400');
            });

            document.getElementById(`tab-${tabId}`).classList.remove('hidden');
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if (activeBtn) {
                activeBtn.classList.add('bg-teal-600', 'text-white', 'shadow');
                activeBtn.classList.remove('text-slate-400');
            }
        }

        /* ================= 3. AI CHATBOT LOGIC (Gemini API) ================= */
        let chatHistory = [];

        function appendMessage(role, text) {
            const chatBox = document.getElementById('chat-box');
            const wrapper = document.createElement('div');
            wrapper.className = role === 'user' ? 'flex items-start justify-end gap-3' : 'flex items-start gap-3';

            if (role === 'user') {
                wrapper.innerHTML = `
                    <div class="max-w-[80%] bg-teal-600 text-white rounded-2xl rounded-tr-none p-3.5 text-sm leading-relaxed shadow">
                        ${escapeHtml(text)}
                    </div>
                `;
            } else {
                wrapper.innerHTML = `
                    <div class="w-9 h-9 rounded-full bg-teal-500/20 border border-teal-400 flex items-center justify-center text-lg flex-shrink-0">
                        🧙‍♂️
                    </div>
                    <div class="max-w-[80%] bg-slate-800/90 border border-teal-500/20 rounded-2xl rounded-tl-none p-4 text-sm text-slate-200 leading-relaxed shadow whitespace-pre-wrap">
                        ${text}
                    </div>
                `;
            }

            chatBox.appendChild(wrapper);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        function askQuickQuestion(questionText) {
            switchTab('chat');
            document.getElementById('chat-input').value = questionText;
            handleChatSubmit(new Event('submit'));
        }

        function clearChat() {
            chatHistory = [];
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = `
                <div class="flex items-start gap-3">
                    <div class="w-9 h-9 rounded-full bg-teal-500/20 border border-teal-400 flex items-center justify-center text-lg flex-shrink-0">
                        🧙‍♂️
                    </div>
                    <div class="max-w-[80%] bg-slate-800/90 border border-teal-500/20 rounded-2xl rounded-tl-none p-4 text-sm text-slate-200 leading-relaxed shadow">
                        대화가 초기화되었네! 물생활에 대해 또 궁금한 점이 있다면 언제든 물어보게나. 🐟
                    </div>
                </div>
            `;
        }

        async function handleChatSubmit(e) {
            e.preventDefault();
            const inputEl = document.getElementById('chat-input');
            const prompt = inputEl.value.trim();
            if (!prompt) return;

            // UI user message
            appendMessage('user', prompt);
            inputEl.value = '';

            // Loading indicator
            const chatBox = document.getElementById('chat-box');
            const loadingId = 'loading-' + Date.now();
            const loadingEl = document.createElement('div');
            loadingEl.id = loadingId;
            loadingEl.className = 'flex items-start gap-3';
            loadingEl.innerHTML = `
                <div class="w-9 h-9 rounded-full bg-teal-500/20 border border-teal-400 flex items-center justify-center text-lg flex-shrink-0 animate-spin">
                    🌀
                </div>
                <div class="bg-slate-800/60 border border-teal-500/20 rounded-2xl p-3 text-xs text-teal-300 font-mono flex items-center gap-2">
                    어항선배가 답을 생각 중입니다...
                </div>
            `;
            chatBox.appendChild(loadingEl);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Prepare Gemini Request
            const systemPrompt = `당신은 경력 15년 차 열대어 및 수족관 물잡이 전문가 캐릭터 '어항선배'입니다. 
말투는 다정하고 친근한 반말 말투("~라네", "~하게나", "알겠지?")를 사용하며, 초보 물집사(사용자)가 이해하기 쉽도록 핵심을 정확하게 설명해주세요. 
물고기 건강, 수질 관리, 여과기 추천, 환수 방법, 이끼 대처법 등 물생활 제반 지식에 답변해주세요. 이모지를 적절히 활용하세요.`;

            chatHistory.push({ role: 'user', parts: [{ text: prompt }] });

            try {
                const apiKey = ""; // Built-in environment key
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: chatHistory,
                        systemInstruction: { parts: [{ text: systemPrompt }] }
                    })
                });

                const data = await response.json();
                document.getElementById(loadingId)?.remove();

                if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
                    const aiReply = data.candidates[0].content.parts[0].text;
                    chatHistory.push({ role: 'model', parts: [{ text: aiReply }] });
                    appendMessage('model', aiReply);
                } else {
                    appendMessage('model', '어라라, 수중 통신에 잠깐 문제가 생긴 것 같네! 다시 한번 물어봐줄 수 있겠나?');
                }
            } catch (err) {
                document.getElementById(loadingId)?.remove();
                appendMessage('model', '오류가 발생했네! 네트워크 연결을 확인하고 다시 시도해보게나.');
            }
        }


        /* ================= 4. FISH COMPATIBILITY DATABASE & LOGIC ================= */
        const fishDatabase = {
            neon: { name: "네온테트라", temp: "22~26°C", size: "3~4cm", aggression: "순함 (소형 군영어)", icon: "🐟" },
            angel: { name: "엔젤피쉬", temp: "24~28°C", size: "12~15cm", aggression: "중간 (성어 시 입에 들어가는 유어 포식)", icon: "🐠" },
            cherry: { name: "체리새우", temp: "20~25°C", size: "2~3cm", aggression: "완전 순함 (먹이사슬 최하위)", icon: "🦐" },
            puffer: { name: "초록복어", temp: "24~28°C", size: "6~10cm", aggression: "매우 강함 (지느러미 뜯음, 새우/달팽이 사냥)", icon: "🐡" },
            turtle: { name: "거북이 (수생)", temp: "25~29°C", size: "15~25cm", aggression: "잡식/포식성 (물고기 잡아먹음)", icon: "🐢" },
            guppy: { name: "구피", temp: "22~27°C", size: "3~5cm", aggression: "순함 (번식력 왕)", icon: "🐠" },
            cory: { name: "코리도라스", temp: "22~26°C", size: "4~6cm", aggression: "매우 순함 (바닥재 청소)", icon: "🐟" }
        };

        // Specific rules: key "fish1-fish2"
        const compatibilityRules = {
            "neon-angel": { score: "주의", color: "text-amber-400", bg: "border-amber-500/40 bg-amber-950/20", text: "엔젤피쉬가 어릴 때는 합사가 가능하지만, 성어가 되면 커진 입으로 소형 네온테트라를 삼킬 위험이 높습니다!" },
            "neon-cherry": { score: "가능 (수초 필수)", color: "text-emerald-400", bg: "border-emerald-500/40 bg-emerald-950/20", text: "성체 새우와는 잘 지내지만, 치새우(새끼 새우)는 수초나 모스 같은 숨을 공간이 없으면 네온테트라의 먹이가 될 수 있습니다." },
            "neon-puffer": { score: "불가 ❌", color: "text-rose-400", bg: "border-rose-500/40 bg-rose-950/20", text: "복어는 공격성이 강해 네온테트라의 지느러미를 입으로 물어뜯고 공격합니다. 절대 같이 합사하지 마세요." },
            "cherry-puffer": { score: "절대 불가 ❌", color: "text-rose-500", bg: "border-rose-500/50 bg-rose-950/30", text: "복어에게 체리새우는 가장 좋아하는 최고급 특식입니다. 입수하는 즉시 모두 잡아먹힙니다." },
            "turtle-neon": { score: "불가 ❌", color: "text-rose-400", bg: "border-rose-500/40 bg-rose-950/20", text: "거북이는 빠른 물고기도 자는 동안이나 구석에 몰아서 잡아먹습니다." },
            "guppy-cherry": { score: "최상 🟢", color: "text-emerald-300", bg: "border-emerald-500/40 bg-emerald-950/20", text: "대표적인 평화로운 온순 조합입니다! 수초를 풍성하게 해주면 치새우 번식도 문제없이 가능합니다." },
            "cory-neon": { score: "최상 🟢", color: "text-emerald-300", bg: "border-emerald-500/40 bg-emerald-950/20", text: "상층/중층(네온)과 하층(코리) 서식층이 달라 완벽한 조합을 이룹니다." }
        };

        function initCompatibility() {
            const f1 = document.getElementById('fish1');
            const f2 = document.getElementById('fish2');
            f1.innerHTML = ''; f2.innerHTML = '';

            Object.keys(fishDatabase).forEach(key => {
                const item = fishDatabase[key];
                f1.innerHTML += `<option value="${key}">${item.icon} ${item.name}</option>`;
                f2.innerHTML += `<option value="${key}">${item.icon} ${item.name}</option>`;
            });

            f1.value = "neon";
            f2.value = "cherry";
            checkCompatibility();
        }

        function checkCompatibility() {
            const k1 = document.getElementById('fish1').value;
            const k2 = document.getElementById('fish2').value;

            const info1 = fishDatabase[k1];
            const info2 = fishDatabase[k2];

            document.getElementById('fish1-info').innerHTML = `적정수온: ${info1.temp} | 성체크기: ${info1.size}<br>성향: ${info1.aggression}`;
            document.getElementById('fish2-info').innerHTML = `적정수온: ${info2.temp} | 성체크기: ${info2.size}<br>성향: ${info2.aggression}`;

            const resultBox = document.getElementById('compatibility-result');

            if (k1 === k2) {
                resultBox.className = "mt-6 p-6 rounded-xl bg-slate-900/90 border border-teal-500/30 text-center";
                resultBox.innerHTML = `<div class="text-teal-300 font-bold text-lg">동종 합사</div><p class="text-xs text-slate-400 mt-1">같은 종끼리는 수용량만 넘지 않는다면 문제없이 무리 생활이 가능합니다.</p>`;
                return;
            }

            const ruleKey1 = `${k1}-${k2}`;
            const ruleKey2 = `${k2}-${k1}`;
            const match = compatibilityRules[ruleKey1] || compatibilityRules[ruleKey2];

            if (match) {
                resultBox.className = `mt-6 p-6 rounded-xl border ${match.bg} text-center`;
                resultBox.innerHTML = `
                    <div class="text-xs text-slate-400 font-mono">합사 진단 결과</div>
                    <div class="text-2xl font-bold ${match.color} mt-1">${match.score}</div>
                    <p class="text-xs sm:text-sm text-slate-200 mt-2 max-w-xl mx-auto leading-relaxed">${match.text}</p>
                `;
            } else {
                resultBox.className = "mt-6 p-6 rounded-xl bg-slate-900/90 border border-slate-700 text-center";
                resultBox.innerHTML = `
                    <div class="text-teal-300 font-bold text-base">일반적인 합사 가능 (관찰 필요)</div>
                    <p class="text-xs text-slate-400 mt-1">특별한 극상성 보고는 없으나, 수온 range와 생물 크기 차이를 고려하여 초기에 공격성을 유심히 관찰하세요.</p>
                `;
            }
        }


        /* ================= 5. WATER VOLUME CALCULATOR ================= */
        function calculateWaterVolume() {
            const w = parseFloat(document.getElementById('tank-w').value) || 0;
            const d = parseFloat(document.getElementById('tank-d').value) || 0;
            const h = parseFloat(document.getElementById('tank-h').value) || 0;
            const subH = parseFloat(document.getElementById('substrate-h').value) || 0;

            // Net water height = total height - substrate height - top glass gap (approx 3cm)
            const netH = Math.max(0, h - subH - 3);
            const volumeLiters = (w * d * netH) / 1000;

            // Approx rule: ~1.5 Liters per 3cm small fish
            const recommendedFish = Math.floor(volumeLiters / 1.5);
            const weeklyWaterChange = (volumeLiters * 0.3).toFixed(1);

            document.getElementById('res-volume').innerText = `${volumeLiters.toFixed(1)} L`;
            document.getElementById('res-fish').innerText = `${recommendedFish} 마리`;
            document.getElementById('res-waterchange').innerText = `${weeklyWaterChange} L`;
        }


        /* ================= 6. CHECKLIST DIAGNOSTIC LOGIC ================= */
        function diagnoseChecklist() {
            const cloudy = document.getElementById('chk-cloudy').checked;
            const foam = document.getElementById('chk-foam').checked;
            const gasping = document.getElementById('chk-gasping').checked;
            const algae = document.getElementById('chk-algae').checked;

            const box = document.getElementById('checklist-diagnosis');

            if (!cloudy && !foam && !gasping && !algae) {
                box.innerHTML = `<span class="text-slate-400">증상을 선택하시면 어항선배의 맞춤 처방법이 표시됩니다.</span>`;
                return;
            }

            let advice = [];

            if (cloudy) {
                advice.push(`• <b>백탁 현상:</b> 신규 어항의 경우 유익균 박테리아의 폭번 과정입니다. 며칠간 사료 투여를 줄이고 여과기를 끄지 마세요. 박테리아제 보충이 도움 됩니다.`);
            }
            if (foam) {
                advice.push(`• <b>수면 거품:</b> 유기물(단백질) 농도가 높거나 여과력이 부족할 때 발생합니다. 즉시 20% 환수 후 에어레이션(기포기)을 강화하세요.`);
            }
            if (gasping) {
                advice.push(`• <b>뻐끔거림 (용존산소 부족/아질산 중독):</b> 긴급 상황입니다! 즉시 환수를 실시하고 기포기를 켜 산소를 공급하세요.`);
            }
            if (algae) {
                advice.push(`• <b>이끼 발생:</b> 조명 시간을 하루 6시간 이하로 줄이고 직사광선을 차단하세요. 체리새우나 오토싱, 안시를 투입하면 효과적입니다.`);
            }

            box.innerHTML = `<div class="space-y-2 text-teal-200">${advice.join('<br><br>')}</div>`;
        }


        /* ================= 7. INITIALIZATION ================= */
        window.onload = function() {
            createBubbles();
            initCompatibility();
            calculateWaterVolume();
        };
    </script>
</body>
</html>
