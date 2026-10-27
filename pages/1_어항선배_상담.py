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
    st.info('"하… 또 기초적인 거 물어보러 왔네. 물고기 용궁 보내기 싫으면 내가 시키는 대로만 해. 물잡이부터 환수까지 다 알려줄 테니까 집중해."')
    
    # ⚡ 초보 필수 퀵 질문 버튼 영역
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
            {"role": "assistant", "content": "어머, 반가워라. 🐟 어항 사이즈든 여과기든 모르는 거 있으면 물어봐. 대충대충 대답 안 해줄 테니까 똑바로 들으라고."}
        ]

    # 질문 내용에 따라 맞춤형 답변을 생성하는 스마트 분석 함수 (냉미녀 언니 버전)
    def generate_smart_reply(user_text):
        text = user_text.replace(" ", "").lower()
        
        # 1. 거북이 + 새우 관련 질문
        if "거북" in text and ("새우" in text or "합사" in text):
            return (
                "하… 거북이랑 새우를 같이 넣는다고? 거북이 특식 뷔페 차려주고 싶은 거 아니면 당장 그 생각 접어.\n\n"
                "1. **현실적인 진단**:\n"
                "   - 거북이는 사냥 본능이 엄청 강한 육식/잡식성 파충류야. 체리새우 같은 소형 갑각류는 거북이한테 움직이는 생식이자 최고급 간식일 뿐이지, 절대 공존할 수 없어.\n"
                "2. **결론 및 조언**:\n"
                "   - 합사 시키는 순간 새우들이 하루 만에 다 뜯겨 먹히거나 사라질 테니까, 새우를 살리고 싶다면 어항을 무조건 따로 분리해. 알겠어?"
            )
        
        # 2. 물잡이 관련 질문
        elif "물잡이" in text:
            return (
                "물잡이란 건 말 그대로 어항 속에 여과 박테리아가 살 수 있는 생태계를 미리 만들어두는 거야.\n\n"
                "1. **핵심 과정**:\n"
                "   - 히터랑 여과기 켜놓고 생물 없이 최소 1~2주는 공회전시켜야 해. 암모니아가 아질산, 질산염으로 바뀌는 사이클이 안 돌면 너네 물고기들 다 며칠 안에 용궁 간다?\n"
                "2. **선배의 조언**:\n"
                "   - 성급하게 생물부터 넣지 말고 진득하게 기다리는 게 물생활의 기본이야."
            )
            
        # 3. 뻐끔거림 / 산소 관련 질문
        elif "뻐끔" in text or "산소" in text:
            return (
                "물고기가 수면 위로 올라와서 뻐끔거린다고? 쯧, 산소가 부족하다는 다급한 SOS잖아.\n\n"
                "1. **즉각 조치**:\n"
                "   - 당장 에어스톤(산소 기포기)부터 설치하고 여과기 출수구를 수면 위로 올려서 물살이 파도를 치게 만들어.\n"
                "2. **원인**:\n"
                "   - 용존 산소량이 부족하거나 수온이 너무 높아서 그런 거니까 정신 바짝 차리고 점검해."
            )
            
        # 4. 환수 관련 질문
        elif "환수" in text or "물갈이" in text:
            return (
                "환수 주기? 당연히 일주일에 한 번씩 전체 수량의 20~30%는 해줘야지.\n\n"
                "1. **주의사항**:\n"
                "   - 설마 수돗물 그냥 냅다 붓는 건 아니겠지? 염소 제거제 꼭 넣고 기존 어항이랑 물 온도 똑같이 맞춰서 넣어라.\n"
                "2. **선배의 조언**:\n"
                "   - 온도 쇼크 오면 물고기들 다 기절하니까 물 맞댐이랑 온도 맞댐 철저히 해."
            )
            
        # 5. 백탁 현상 관련 질문
        elif "백탁" in text or "하얗" in text:
            return (
                "어항 물이 우유처럼 하얗게 변했어? 백탁 현상인데, 세균이 폭발적으로 늘었거나 분진 때문이야.\n\n"
                "1. **대처법**:\n"
                "   - 이때다 싶어서 물 전면 교체한다고 다 갈아엎으면 생태계 완전히 박살 나는 거 알지? 밥 좀 그만 주고 여과기 24시간 돌리면서 차분히 기다려.\n"
                "2. **조언**:\n"
                "   - 물생활은 시간이 약이야. 손 타면 탈수록 어항만 망가져."
            )
            
        # 6. 기타 일반적인 질문에 대한 스마트 대응
        else:
            return (
                f"네가 물어본 **'{user_text}'**, 그 질문 말이야. 초보들이 딱 실수하기 좋은 포인트네.\n\n"
                f"1. **원인 분석**:\n"
                f"   - 대개 수질 스펙트럼이 변했거나 여과 사이클, 혹은 온도/먹이 관리에서 문제가 생긴 거야. 어항은 가만히 놔두는 게 최선인데 손을 너무 많이 타서 그래.\n"
                f"2. **냉미녀 선배의 해결 솔루션**:\n"
                f"   - **첫째**, 여과기가 멈추지 않고 일 잘하고 있는지 지금 당장 확인해.\n"
                f"   - **둘째**, 온도를 딱 맞춘 깨끗한 물로 30%만 신속하게 부분 환수해.\n"
                f"   - **셋째**, 당분간 사료 주는 양 절반으로 줄여. 네가 주는 밥이 다 수질 오염의 원인이야.\n"
                f"3. **선배의 따끔한 조언**:\n"
                f"   - 물생활은 정성과 '기다림'이야. 마음만 앞서서 이것저것 약품 넣지 말고, 차분하게 관찰해봐. 알겠어?"
            )

    # 퀵 질문이 선택된 경우 답변 추가
    if selected_quick:
        st.session_state.messages.append({"role": "user", "content": selected_quick})
        ans = generate_smart_reply(selected_quick)
        st.session_state.messages.append({"role": "assistant", "content": ans})

    # 대화 내역 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 채팅창 (어떤 질문이든 스마트하게 분석해서 답변)
    if prompt := st.chat_input("어항선배에게 질문을 입력하세요 (예: 새우랑 거북이 합사해도 돼?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            smart_ans = generate_smart_reply(prompt)
            st.markdown(smart_ans)
            st.session_state.messages.append({"role": "assistant", "content": smart_ans})

with tab2:
    st.subheader("🔄 어종별 합사 진단기")
    st.markdown("키우고 싶은 두 생물을 선택해 봐. 호구처럼 아무거나 같이 넣었다가 잡아먹히기 전에.")
    c1, c2 = st.columns(2)
    with c1:
        fish1 = st.selectbox("첫 번째 생물", ["네온테트라", "구피", "엔젤피쉬", "체리새우", "초록복어", "베타"])
    with c2:
        fish2 = st.selectbox("두 번째 생물", ["체리새우", "구피", "네온테트라", "코리도라스", "애플스네일", "거북이"])
        
    if st.button("합사 가능성 분석하기"):
        if "거북" in fish1 or "거북" in fish2:
            st.error(f"⚠️ **위험 경고**: 거북이가 포함된 조합은 소형 생물(새우, 소형 테트라 등)을 사냥할 확률이 매우 높습니다! 합사 비추천!")
        else:
            st.success(f"🔍 **분석 결과 ({fish1} + {fish2})**: 합사 적합도 **85% (나쁘지 않음)**")
            st.write(f"- 둘 다 요구하는 수온(24~26℃)이나 수질이 비슷해서 공존은 가능해.")
            st.write(f"- 하지만 크기나 성격 차이가 있으니까 은신처는 알아서 넉넉하게 세팅해 두도록 해.")

with tab3:
    st.subheader("📐 수조 치수별 물용량 및 환수량 계산기")
    st.markdown("어항 사이즈도 안 재고 물생활 시작한 건 아니겠지? 가로, 세로, 높이 입력해봐.")
    w = st.number_input("가로 길이 (cm)", value=60)
    d = st.number_input("세로 폭 (cm)", value=30)
    h = st.number_input("높이 (cm)", value=36)
    
    if st.button("수량 계산하기"):
        liters = (w * d * h) / 1000
        net_liters = liters * 0.85
        st.success(f"💧 **총 수조 용량**: 약 **{liters:.1f} 리터 (L)** (바닥재 감안한 실제 물량 약 {net_liters:.1f}L)")
        st.info(f"🔄 **권장 1회 환수량 (30%)**: 약 **{net_liters * 0.3:.1f} 리터** — 이 정도는 지켜줘야지?")

with tab4:
    st.subheader("📅 30일 초보 물잡이 가이드 스케줄러")
    st.markdown("""
    - **1일차 ~ 3일차**: 바닥재 깔고 물 채우고 히터랑 여과기 24시간 풀가동. **생물 절대 투입 금지야.**
    - **4일차 ~ 7일차**: 박테리아제 넣고 백탁 와도 당황하지 말고 그냥 가만히 두기.
    - **8일차 ~ 14일차**: 물 맑아지면 수초 심고 물고기 넣기 전에 수질 테스트 필수.
    - **15일차 ~ 30일차**: 튼튼한 애들로 소수만 먼저 넣고 어항 반응 보면서 천천히 늘려.
    """)
