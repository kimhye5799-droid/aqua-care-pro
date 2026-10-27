import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="어항선배 AI 상담소",
    page_icon="🐠",
    layout="wide"
)

# 어항선배 PRO v2.0 헤더 (링크 아이콘 제거된 깔끔한 HTML 적용)
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
    # 링크 아이콘이 생기지 않도록 HTML div로 제목 처리
    st.markdown('<div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">💬 어항선배 1:1 상담실</div>', unsafe_allow_html=True)
    
    # 세션 스테이트 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "어머, 반가워라. 🐟 어항 사이즈든 여과기든 모르는 거 있으면 물어봐. 대충대충 대답 안 해줄 테니까 똑바로 들으라고."}
        ]
        
    # 퀵 질문 선택 시 냉미녀 말투로 답변 생성
    if selected_quick:
        st.session_state.messages.append({"role": "user", "content": selected_quick})
        if "물잡이란" in selected_quick:
            ans = "하… 물잡이도 모호한 상태로 생물부터 넣으려고 했던 거야? 물잡이란 건 말 그대로 어항 속에 여과 박테리아가 살 수 있는 생태계를 미리 만들어두는 거야. 히터랑 여과기 켜놓고 생물 없이 최소 1~2주는 공회전시켜야지. 암모니아가 아질산, 질산염으로 바뀌는 사이클이 안 돌면 너네 물고기들 다 며칠 안에 용궁 간다? 기본이야, 정말."
        elif "뻐끔거림" in selected_quick:
            ans = "물고기가 수면 위로 올라와서 뻐끔거린다고? 쯧, 산소가 부족하다는 SOS잖아. 눈치 좀 채지? 당장 에어스톤(산소 기포기)부터 설치하고 여과기 출수구를 수면 위로 올려서 물살이 파도를 치게 만들어. 수온도 체크하고. 산소 용해도가 떨어져서 그런 거니까."
        elif "환수" in selected_quick:
            ans = "환수 주기? 당연히 일주일에 한 번씩 전체 수량의 20~30%는 해줘야지. 설마 수돗물 그냥 냅다 붓는 건 아니겠지? 염소 제거제 꼭 넣고 기존 어항이랑 물 온도 똑같이 맞춰서 넣어라. 온도 쇼크 오면 물고기들 다 기절하니까."
        elif "백탁" in selected_quick:
            ans = "어항 물이 우유처럼 하얗게 변했어? 백탁 현상인데, 세균이 폭발적으로 늘었거나 분진 때문이야. 이때다 싶어서 물 전면 교체한다고 다 갈아엎으면 생태계 완전히 박살 나는 거 알지? 밥 좀 그만 주고 여과기 24시간 돌리면서 차분히 기다려. 시간이 약이야."
        elif "구피" in selected_quick:
            ans = "구피랑 체리새우? 합사 자체는 불가능한 건 아니야. 근데 구피가 입에 들어가는 작은 치새우들은 간식처럼 냠냠 먹어 치울 수도 있거든? 수초나 은신처를 아주 빽빽하게 심어둘 거 아니면 추천 안 해. 알아서 판단해."
        else:
            ans = f"'{selected_quick}' 말이지? 하… 기초적인 거지만 이번만 특별히 알려줄게. 수온은 24~26도 고정, 여과기 24시간 풀가동, 환수는 꾸준히. 이것만 지켜도 반은 먹고 들어가니까 명심해."
        st.session_state.messages.append({"role": "assistant", "content": ans})

    # 대화 내역 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 채팅창
    if prompt := st.chat_input("어항선배에게 질문을 입력하세요 (예: 새우가 자꾸 죽어요, 물이 하얘요)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            detailed_ans = (
                f"하… 질문한 **'{prompt}'**, 그럴 줄 알았어. 딱 초보들이 흔하게 저지르는 실수라니까? 잘 들 어, 짚어줄 테니까.\n\n"
                f"1. **원인 분석**:\n"
                f"   - 네가 겪는 그 문제는 십중팔구 여과 사이클이 깨졌거나 수온/수질 스펙트럼이 급격하게 변해서 생기는 현상이야. 어항은 가만히 놔두는 게 최선인데 손을 너무 많이 타서 그래.\n\n"
                f"2. **냉미녀 선배의 해결 솔루션**:\n"
                f"   - **첫째**, 여과기가 멈추지 않고 일 잘하고 있는지 지금 당장 확인해. 수류도 점검하고.\n"
                f"   - **둘째**, 온도를 딱 맞춘 깨끗한 물로 30%만 신속하게 부분 환수해. 한 번에 다 갈면 대참사 나는 거 알지?\n"
                f"   - **셋째**, 당분간 사료 주는 양 절반으로 줄여. 네가 주는 밥이 다 수질 오염의 원인이야.\n\n"
                f"3. **선배의 따끔한 조언**:\n"
                f"   - 물생활은 정성과 '기다림'이야. 마음만 앞서서 이것저것 약품 넣지 말고, 차분하게 기다려봐. 알겠어?"
            )
            st.markdown(detailed_ans)
            st.session_state.messages.append({"role": "assistant", "content": detailed_ans})

with tab2:
    st.subheader("🔄 어종별 합사 진단기")
    st.markdown("키우고 싶은 두 생물을 선택해 봐. 호구처럼 아무거나 같이 넣었다가 잡아먹히기 전에.")
    c1, c2 = st.columns(2)
    with c1:
        fish1 = st.selectbox("첫 번째 생물", ["네온테트라", "구피", "엔젤피쉬", "체리새우", "초록복어", "베타"])
    with c2:
        fish2 = st.selectbox("두 번째 생물", ["체리새우", "구피", "네온테트라", "코리도라스", "애플스네일", "거북이"])
        
    if st.button("합사 가능성 분석하기"):
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
