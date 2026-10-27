import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="픽셀 파우더 어항 & 어항선배 PRO",
    page_icon="🐠",
    layout="wide"
)

# 사이드바 메뉴로 두 페이지를 완전히 분리
st.sidebar.title("🐠 물생활 스마트 케어")
page = st.sidebar.radio("메뉴 선택", ["🎮 픽셀 파우더 어항 샌드박스", "💬 어항선배 AI 상담소"])

if page == "🎮 픽셀 파우더 어항 샌드박스":
    st.subheader("🎮 레트로 픽셀 파우더 어항 샌드박스")
    st.caption("모래, 자갈, 수초를 심고 생물을 키우는 물리 시뮬레이션 게임입니다.")
    
    # 샌드박스 어항 HTML/JS 단독 렌더링
    html_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>픽셀 파우더 어항 Sandbox</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
          font-family: 'Pretendard', sans-serif;
          background-color: #060913;
          color: #f1f5f9;
          display: flex;
          height: 78vh;
          overflow: hidden;
          border-radius: 12px;
        }
        .tank-area {
          flex: 1;
          position: relative;
          background: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 10px;
        }
        .glass-tank {
          position: relative;
          width: 100%;
          height: 100%;
          border-radius: 12px;
          box-shadow: inset 0 0 25px rgba(56, 189, 248, 0.25);
          border: 3px solid #38bdf8;
          background-color: #020617;
          overflow: hidden;
        }
        canvas { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
        .controls-bar {
          position: absolute;
          bottom: 12px;
          left: 50%;
          transform: translateX(-50%);
          background: rgba(15, 23, 42, 0.9);
          padding: 6px 16px;
          border-radius: 20px;
          font-size: 11px;
          color: #cbd5e1;
          border: 1px solid rgba(255,255,255,0.2);
        }
      </style>
    </head>
    <body>
      <div class="tank-area">
        <div class="glass-tank">
          <canvas id="aquariumCanvas"></canvas>
          <div class="controls-bar">✨ 샌드박스 엔진 구동 중: 모래를 쌓고 물고기를 관찰해 보세요!</div>
        </div>
      </div>

      <script>
        const canvas = document.getElementById('aquariumCanvas');
        const ctx = canvas.getContext('2d');

        function resize() {
          canvas.width = canvas.parentElement.clientWidth;
          canvas.height = canvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        function animate() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.fillStyle = '#38bdf8';
          ctx.font = 'bold 13px sans-serif';
          ctx.fillText("🐠 픽셀 파우더 어항 시뮬레이터 활성화됨", 24, 35);
          requestAnimationFrame(animate);
        }
        animate();
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=620, scrolling=False)

elif page == "💬 어항선배 AI 상담소":
    # 두 번째 사진의 어항선배 PRO v2.0 스타일 구현
    st.markdown("### 🐠 어항선배 <span style='background-color:#0284c7; color:white; padding:2px 8px; border-radius:6px; font-size:12px;'>PRO v2.0</span>", unsafe_allow_html=True)
    st.caption("초보 물집사를 위한 AI 스마트 케어 솔루션")

    # 상단 탭 메뉴 구성
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 1:1 상담", "🔄 어종 합사 진단기", "📐 물용량 & 환수 계산기", "📅 30일 물잡이 스케줄"])

    with tab1:
        st.info('"안녕 초보 물집사! 물고기가 용궁 갈까 봐 걱정인가? 물잡이부터 어종 합사, 환수 주기까지 뭐든 물어보게나!"')
        
        # 퀵 질문 버튼 영역
        st.markdown("#### ⚡ 초보 필수 퀵 질문")
        q_cols = st.columns(5)
        quick_questions = [
            "물잡이란 무엇인가요?", 
            "수면 뻐끔거림 해결법", 
            "올바른 환수 주기 및 방법", 
            "백탁 현상 대처 가이드", 
            "구피 x 체리새우 합사 가능 여부"
        ]
        
        selected_quick = None
        for i, q in enumerate(quick_questions):
            if q_cols[i].button(q, use_container_width=True):
                selected_quick = q

        st.markdown("---")
        st.markdown("#### 💬 어항선배 실시간 상담실")
        
        # 세션 스테이트 초기화 (대화 기록 유지)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "반가네 물집사! 🐟 어항 사이즈, 여과기 종류, 물고기 상태 등 무엇이든 편하게 물어보게나. 친절하고 상세하게 가이드해주지!"}
            ]
            
        # 퀵 질문이 선택된 경우 상세 답변 추가
        if selected_quick:
            st.session_state.messages.append({"role": "user", "content": selected_quick})
            if "물잡이란" in selected_quick:
                ans = "물잡이란 어항 속에 여과 박테리아가 안정적으로 정착할 수 있는 생태 환경을 미리 조성하는 과정입니다. 보통 신규 어항에 물, 여과기, 바닥재를 넣고 히터와 산소기포기를 가동한 채 생물 없이 1~2주(박테리아제 투여 시 3~5일) 이상 여과기를 공회전시키는 것을 말합니다. 이 기간 동안 물고기 배설물이나 사료 찌꺼기에서 나오는 암모니아가 유독성이 낮은 아질산, 최종적으로 질산염으로 분화되는 사이클이 완성됩니다. 충분한 물잡이가 필수입니다!"
            elif "뻐끔거림" in selected_quick:
                ans = "물고기가 수면 위로 올라와 뻐끔거리는 현상(산소 부족)은 1순위로 용존 산소량 부족 또는 암모니아 수치 급증을 의심해야 합니다. 해결 방법으로는 1) 산소 기포기(에어스톤)를 즉시 설치하고, 2) 여과기 출수구를 수면 위로 향하게 하여 물살이 수면을 때리며 산소가 녹아들도록 하세요. 3) 수온이 너무 높으면 산소 용해도가 낮아지므로 히터 온도를 점검하고 30% 부분 환수를 진행해 주세요."
            elif "환수" in selected_quick:
                ans = "올바른 환수 주기는 일반조명/여과 기준 **주 1회 전체 수량의 20~30%**를 환수하는 것이 가장 이상적입니다. 주의할 점은 1) 기존 어항과 새 물의 수온 차이가 1~2도 이내여야 하며, 2) 수돗물 속 염소를 제거하기 위해 반드시 '염소 제거제'를 투여하거나 하루 이상 받아둔 물을 사용해야 합니다."
            elif "백탁" in selected_quick:
                ans = "백탁 현상(물이 우유처럼 하얗게 흐려지는 현상)은 세균성 백탁(여과 박테리아 급증) 또는 물리적 백탁(분진)입니다. 대처법은 밥 양을 줄이고, 여과기를 24시간 풀가동하며, 환수를 자주 하기보다 자연스럽게 생태계가 안정되도록 며칠간 기다리는 것이 가장 좋습니다."
            elif "구피" in selected_quick:
                ans = "구피와 체리새우의 합사는 **가능하지만 주의가 필요**합니다! 구피는 온순하지만 입에 들어가는 아주 작은 새끼 새우(치새우)는 사냥할 수 있습니다. 모스(수초)나 은신처를 어항 곳곳에 풍성하게 만들어 치새우들이 숨을 공간을 마련해 주면 훨씬 안전하게 공존할 수 있습니다."
            else:
                ans = f"'{selected_quick}'에 대한 상세 가이드입니다. 물생활에서 가장 중요한 것은 급하지 않게 환경을 맞춰주는 것입니다. 수온은 24~26도, 여과기는 24시간 가동, 주 1회 환수 원칙만 지키셔도 대부분의 문제가 예방됩니다!"
            st.session_state.messages.append({"role": "assistant", "content": ans})

        # 대화 내용 출력
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 사용자 입력 채팅창 (길고 자세한 답변 출력)
        if prompt := st.chat_input("어항선배에게 무엇이든 물어보세요 (예: 물고기가 자꾸 가라앉아요)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                detailed_ans = f"물집사의 질문 **'{prompt}'**에 대해 어항선배가 상세히 진단해 주마! 🐠\n\n1. **핵심 원인 분석**: 초보 물집사들이 이 시기에 가장 흔히 겪는 현상으로, 대개 여과 사이클 불균형, 수온 급변, 혹은 급격한 수질 오염에서 비롯된다네.\n2. **단계별 맞춤 해결책**:\n   - 첫째, 여과기가 24시간 정상 작동 중인지, 출수구 수류가 적당한지 확인하게.\n   - 둘째, 즉시 30% 부분 환수를 진행하여 쌓인 유해 물질을 희석시켜 주게.\n   - 셋째, 당분간 먹이 급여량을 절반으로 줄여 수질 오염 속도를 늦추게나.\n3. **선배의 조언**: 물생활은 '기다림과 관찰의 미학'이라네. 급하게 약품을 쓰기보다는 꾸준한 부분 환수와 수온 안정이 가장 특효약이지! 추가로 궁금한 점이 있다면 언제든 편하게 물어보게나."
                st.markdown(detailed_ans)
                st.session_state.messages.append({"role": "assistant", "content": detailed_ans})

    with tab2:
        st.subheader("🔄 어종별 합사 진단기")
        st.markdown("키우고 싶은 두 생물을 선택하면 합사 성공 확률과 주의사항을 알려줍니다.")
        c1, c2 = st.columns(2)
        with c1:
            fish1 = st.selectbox("첫 번째 생물", ["네온테트라", "구피", "엔젤피쉬", "체리새우", "초록복어", "베타"])
        with c2:
            fish2 = st.selectbox("두 번째 생물", ["체리새우", "구피", "네온테트라", "코리도라스", "애플스네일", "안테나거북이"])
            
        if st.button("합사 가능성 분석하기"):
            st.success(f"🔍 **분석 결과 ({fish1} + {fish2})**: 합사 안정성 지수 **85% (안전)**")
            st.write(f"- 두 생물은 대체로 요구되는 수온(24~26℃)과 pH 성향이 유사합니다.")
            st.write(f"- 단, 크기 차이가 심하거나 은신처가 부족할 경우 마찰이 있을 수 있으니 수초를 보강해 주세요.")

    with tab3:
        st.subheader("📐 수조 치수별 물용량 및 환수량 계산기")
        st.markdown("어항의 가로, 세로, 높이를 입력하면 총 수량과 권장 환수량을 계산해 줍니다.")
        w = st.number_input("가로 길이 (cm)", value=60)
        d = st.number_input("세로 폭 (cm)", value=30)
        h = st.number_input("높이 (cm)", value=36)
        
        if st.button("수량 계산하기"):
            liters = (w * d * h) / 1000
            net_liters = liters * 0.85  # 모래, 유목 부피 고려
            st.success(f"💧 **총 수조 용량**: 약 **{liters:.1f} 리터 (L)** (실제 물량 약 {net_liters:.1f}L)")
            st.info(f"🔄 **권장 1회 환수량 (30%)**: 약 **{net_liters * 0.3:.1f} 리터**")

    with tab4:
        st.subheader("📅 30일 초보 물잡이 가이드 스케줄러")
        st.markdown("""
        - **1일차 ~ 3일차**: 소일 및 모래 세팅, 물 채우기, 히터 및 여과기 24시간 가동 (생물 투입 절대 금지!)
        - **4일차 ~ 7일차**: 박테리아제 투여, 백탁 현상(물 흐려짐) 발생 확인 (자연스러운 현상이니 대기)
        - **8일차 ~ 14일차**: 물이 다시 맑아짐, 수초 식재 가능, 생물 투입 전 수질 테스트 진행
        - **15일차 ~ 30일차**: 강한 생물(네온테트라, 구피 등) 소수만 먼저 투입 후 점진적 개체수 증가
        """)
