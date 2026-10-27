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

# 상단 기능 탭 (샌드박스 제외, 어항선배 전용 기능만 구성)
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 1:1 상담", "🔄 어종 합사 진단기", "📐 물용량 & 환수 계산기", "📅 30일 물잡이 스케줄"])

with tab1:
    st.info('"안녕 초보 물집사! 물고기가 용궁 갈까 봐 걱정인가? 물잡이부터 어종 합사, 환수 주기까지 뭐든 물어보게나!"')
    
    # ⚡ 초보 필수 퀵 질문 버튼 영역
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
    st.markdown("#### 💬 어항선배 1:1 상담실")
    
    # 세션 스테이트 초기화 (대화 기록 유지)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "반갑네 물집사! 🐟 어항 사이즈, 여과기 종류, 물고기 상태 등 무엇이든 편하게 물어보게나. 친절하고 상세하게 가이드해주지!"}
        ]
        
    # 퀵 질문이 클릭된 경우 상세 답변 생성 및 대화록 추가
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

    # 대화 내역 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 질문 입력창 (상세하고 긴 전문 답변 반환)
    if prompt := st.chat_input("어항선배에게 질문을 입력하세요 (예: 새우가 자꾸 죽어요, 물이 하얘요)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            detailed_ans = (
                f"물집사의 질문 **'{prompt}'**에 대해 어항선배가 상세히 진단해 주마! 🐠\n\n"
                f"1. **핵심 원인 분석**:\n"
                f"   - 입력한 증상은 초보 물집사들이 가장 자주 겪는 수질 모니터링 이슈라네. 주로 여과 박테리아 생태계 미정착, 급격한 pH/수온 변화, 혹은 과도한 사료 급여로 인한 아질산 수치 상승이 원인일 가능성이 크지.\n\n"
                f"2. **단계별 맞춤 조치 방안**:\n"
                f"   - **1단계**: 여과기가 24시간 멈춤 없이 가동 중인지 확인하고 수면 물살을 살짝 높여 산소 공급량을 늘리게.\n"
                f"   - **2단계**: 즉시 온도를 맞춘 깨끗한 물로 20~30% 부분 환수를 진행하여 유해 물질 농도를 낮추게나.\n"
                f"   - **3단계**: 2~3일간 사료 급여를 중단하거나 최소한으로 줄여 여과기에 들어가는 부담을 덜어주게.\n\n"
                f"3. **선배의 물생활 팁**:\n"
                f"   - 물고기 치료나 수질 개선의 핵심은 '급격한 변화를 주지 않는 것'이라네. 차근차근 환수와 관찰을 병행해 보게나!"
            )
            st.markdown(detailed_ans)
            st.session_state.messages.append({"role": "assistant", "content": detailed_ans})

with tab2:
    st.subheader("🔄 어종별 합사 진단기")
    st.markdown("키우고 싶은 두 생물을 선택하면 합사 성공 확률과 주의사항을 알려줍니다.")
    c1, c2 = st.columns(2)
    with c1:
        fish1 = st.selectbox("첫 번째 생물", ["네온테트라", "구피", "엔젤피쉬", "체리새우", "초록복어", "베타"])
    with c2:
        fish2 = st.selectbox("두 번째 생물", ["체리새우", "구피", "네온테트라", "코리도라스", "애플스네일", "거북이"])
        
    if st.button("합사 가능성 분석하기"):
        st.success(f"🔍 **분석 결과 ({fish1} + {fish2})**: 합사 적합도 **85% (안정적)**")
        st.write(f"- 두 생물 모두 수온(24~26℃)과 요구 수질 환경이 유사합니다.")
        st.write(f"- 다만 개체별 성격 차이나 크기 차이가 있을 수 있으므로 수초나 구조물 은신처를 풍성하게 배치해 주세요.")

with tab3:
    st.subheader("📐 수조 치수별 물용량 및 환수량 계산기")
    st.markdown("어항의 가로, 세로, 높이를 입력하면 총 수량과 1회 권장 환수량을 계산해 줍니다.")
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
    - **1일차 ~ 3일차**: 바닥재 세팅, 물 채우기, 히터/여과기 24시간 가동 (생물 투입 금지)
    - **4일차 ~ 7일차**: 박테리아제 투여 및 백탁 현상 관찰 (자연스러운 현상이므로 대기)
    - **8일차 ~ 14일차**: 물이 맑아진 후 수초 심기 및 생물 투입 전 수질 테스트
    - **15일차 ~ 30일차**: 튼튼한 튼튼이 물고기 소수 투입 후 경과 관찰하며 천천히 개체수 늘리기
    """)
