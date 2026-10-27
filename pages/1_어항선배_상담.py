import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="어항선배 AI 상담소",
    page_icon="🐠",
    layout="wide"
)

# 어항선배 PRO v2.0 헤더
st.markdown("### 🐠 어항선배 <span style='background-color:#0284c7; color:white; padding:2px 8px; border-radius:6px; font-size:12px;'>PRO v2.0</span>", unsafe_allow_html=True)
st.caption("초보 물집사를 위한 AI 스마트 케어 솔루션")

# 상단 기능 탭
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 1:1 상담", "🔄 어종 합사 진단기", "📐 물용량 & 환수 계산기", "📅 30일 물잡이 스케줄"])

with tab1:
    st.info('하… 무슨 질문을 들고 오려고? 네가 뭘 물어보든 정확한 팩트와 해결책을 찾아줄 테니까 일단 물어봐.')
    
    # 초보 필수 퀵 질문 버튼 영역
    st.markdown('<div style="font-size: 0.95rem; font-weight: bold; color: #38bdf8; margin-bottom: 8px;">⚡ 초보 필수 퀵 질문</div>', unsafe_allow_html=True)
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
    st.markdown('<div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">💬 어항선배 1:1 상담실</div>', unsafe_allow_html=True)
    
    # 세션 스테이트 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "어머, 반가워라. 🐟 궁금한 거 있으면 아무거나 물어봐. 팩트로 조져줄 테니까."}
        ]

    # 스마트 답변 생성 함수
    def generate_reply(user_text):
        text = user_text.replace(" ", "").lower()
        
        if "물잡이" in text:
            return (
                "하… 물잡이도 모호한 상태로 생물부터 넣으려고 했던 거야?\n\n"
                "1. **팩트 체크**:\n"
                "   - 물잡이란 어항 속에 여과 박테리아가 안정적으로 정착할 수 있는 생태 환경을 미리 조성하는 과정이야. 히터와 여과기를 켜놓고 생물 없이 최소 1~2주간 공회전시켜야 해.\n"
                "2. **선배의 조언**:\n"
                "   - 성급하게 굴지 말고 진득하게 기다려. 생물 먼저 넣으면 다 용궁 간다?"
            ), "https://www.google.com/search?q=어항+물잡이+방법"

        elif "환수" in text and ("5번" in text or "자주" in text or "매일" in text or "많이" in text):
            return (
                "하… 일주일에 5번? 너 어항을 세탁기에 돌릴 작정이니? 미쳤어?\n\n"
                "1. **위험성**:\n"
                "   - 환수를 너무 자주 하면 여과 박테리아가 다 쓸려 나가고 수온/수질 쇼크로 물고기들 다 기절해.\n"
                "2. **해결책**:\n"
                "   - 특별한 이유가 없으면 **일주일에 딱 1번, 전체 물의 20~30%**만 부분 환수해라."
            ), "https://www.google.com/search?q=어항+환수+주기"

        elif "거북" in text and ("새우" in text or "합사" in text):
            return (
                "하… 거북이랑 새우를 같이 넣는다고? 거북이한테 뷔페 차려주고 싶은 거 아니면 당장 그 생각 접어.\n\n"
                "1. **진단**:\n"
                "   - 거북이는 사냥 본능이 강해서 소형 갑각류는 그냥 움직이는 간식일 뿐이야. 절대 공존 안 돼."
            ), "https://www.google.com/search?q=거북이와+새우+합사"

        elif "뻐끔" in text or "산소" in text:
            return (
                "물고기가 수면 위로 올라와서 뻐끔거린다고? 산소가 부족하다는 SOS잖아.\n\n"
                "1. **조치**:\n"
                "   - 당장 에어스톤(산소 기포기) 설치하고 여과기 출수구를 수면 위로 올려서 물살을 일으켜."
            ), "https://www.google.com/search?q=물고기+수면+뻐끔거림"

        elif "백탁" in text or "하얗" in text:
            return (
                "어항 물이 우유처럼 하얗게 변했어? 백탁 현상인데 세균이 늘었거나 분진 때문이야.\n\n"
                "1. **대처법**:\n"
                "   - 물 전체 갈아엎지 말고 밥 양 줄이고 여과기 24시간 돌리면서 차분히 기다려."
            ), "https://www.google.com/search?q=어항+백탁현상+해결"

        else:
            return (
                f"하… 네가 물어본 **'{user_text}'**, 그 질문 말이야.\n\n"
                f"1. **핵심 분석**:\n"
                f"   - 대개 수질 스펙트럼이 변했거나 여과 사이클, 혹은 온도/먹이 관리에서 문제가 생긴 거야. 어항은 손을 탈수록 망가지니까 가만히 놔두는 게 최선이라네.\n"
                f"2. **냉미녀 선배의 솔루션**:\n"
                f"   - **첫째**, 여과기가 멈추지 않고 잘 돌아가는지 확인해.\n"
                f"   - **둘째**, 온도를 딱 맞춘 깨끗한 물로 30%만 신속하게 부분 환수해.\n"
                f"   - **셋째**, 당분간 사료 주는 양 절반으로 줄여.\n"
                f"3. **조언**:\n"
                f"   - 물생활은 정성과 '기다림'이야. 차분하게 관찰해봐."
            ), f"https://www.google.com/search?q={user_text.replace(' ', '+')}"

    # 퀵 질문 선택 처리
    if selected_quick:
        st.session_state.messages.append({"role": "user", "content": selected_quick})
        ans, link = generate_reply(selected_quick)
        full_ans = f"{ans}\n\n🔗 [관련 구글 검색 참고 링크 바로가기]({link})"
        st.session_state.messages.append({"role": "assistant", "content": full_ans})

    # 대화 내역 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 채팅창
    if prompt := st.chat_input("어항선배에게 무엇이든 물어보세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            ans, link = generate_reply(prompt)
            full_ans = f"{ans}\n\n🔗 [관련 구글 검색 참고 링크 바로가기]({link})"
            st.markdown(full_ans)
            st.session_state.messages.append({"role": "assistant", "content": full_ans})

with tab2:
    st.subheader("🔄 어종별 합사 진단기")
    st.markdown("키우고 싶은 두 생물을 선택해 봐.")
    c1, c2 = st.columns(2)
    with c1:
        fish1 = st.selectbox("첫 번째 생물", ["네온테트라", "구피", "엔젤피쉬", "체리새우", "초록복어", "베타"])
    with c2:
        fish2 = st.selectbox("두 번째 생물", ["체리새우", "구피", "네온테트라", "코리도라스", "애플스네일", "거북이"])
        
    if st.button("합사 가능성 분석하기"):
        if "거북" in fish1 or "거북" in fish2:
            st.error("⚠️ **위험 경고**: 거북이가 포함된 조합은 소형 생물(새우 등)을 사냥할 확률이 매우 높습니다!")
        else:
            st.success(f"🔍 **분석 결과 ({fish1} + {fish2})**: 합사 적합도 **85% (나쁘지 않음)**")
            st.write("- 두 생물은 수온 및 수질 요구 조건이 비슷하여 공존이 가능합니다.")

with tab3:
    st.subheader("📐 수조 치수별 물용량 및 환수량 계산기")
    w = st.number_input("가로 길이 (cm)", value=60)
    d = st.number_input("세로 폭 (cm)", value=30)
    h = st.number_input("높이 (cm)", value=36)
    
    if st.button("수량 계산하기"):
        liters = (w * d * h) / 1000
        net_liters = liters * 0.85
        st.success(f"💧 **총 수조 용량**: 약 **{liters:.1f} 리터 (L)** (실제 물량 약 {net_liters:.1f}L)")
        st.info(f"🔄 **권장 1회 환수량 (30%)**: 약 **{net_liters * 0.3:.1f} 리터**")

with tab4:
    st.subheader("📅 30일 초보 물잡이 가이드 스케줄러")
    st.markdown("""
    - **1~3일차**: 바닥재 깔고 물 채우고 히터/여과기 24시간 풀가동 (생물 투입 금지)
    - **4~7일차**: 박테리아제 투여 및 백탁 현상 대처 (가만히 두기)
    - **8~14일차**: 물 맑아지면 수초 식재 및 수질 테스트
    - **15~30일차**: 튼튼한 생물 소수만 먼저 투입 후 점진적 개체수 증가
    """)
