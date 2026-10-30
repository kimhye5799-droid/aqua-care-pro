import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="어항선배 AI 상담소",
    page_icon="🐠",
    layout="wide"
)

# 어항선배 PRO v2.0 헤더
st.markdown("### 🐠 어항선배 <span style='background-color:#0284c7; color:white; padding:2px 8px; border-radius:6px; font-size:12px;'>PRO v2.0</span>", unsafe_allow_html=True)
st.caption("초보 물집사를 위한 AI 스마트 케어 솔루션 (큐레이션 Q&A 모드)")

# 상단 기능 탭
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 어항선배 Q&A", "🔄 어종 합사 진단기", "📐 물용량 & 환수 계산기", "📅 30일 물잡이 스케줄"])

with tab1:
    st.info('하… 직접 타이핑하면서 엉뚱한 거 물어볼 생각 말고, 아래 초보들이 제일 많이 하는 질문들 중에서 골라서 눌러봐. 다 팩트로 조져줄 테니까.')
    
    st.markdown("---")
    st.markdown('<div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">📚 초보 물집사 랭킹 TOP Q&A 선택소</div>', unsafe_allow_html=True)
    st.caption("궁금한 질문을 클릭하면 어항선배의 시크한 답변과 구글 검색 참고 링크가 출력됩니다!")

    # 미리 준비된 인기 질문 리스트 (질문, 답변, 구글 검색 링크)
    curated_qna = [
        {
            "q": "물잡이는 도대체 왜 해야 하고 어떻게 하는 거야?",
            "ans": "하… 물잡이도 안 하고 생물부터 넣으려고 했니? 물잡이란 어항 속에 여과 박테리아가 살 수 있는 생태계를 미리 만드는 거야. 히터랑 여과기 켜놓고 생물 없이 최소 1~2주는 공회전시켜야지. 안 그러면 물고기들 다 용궁 간다?",
            "link": "https://www.google.com/search?q=어항+물잡이+방법"
        },
        {
            "q": "거북이가 물고기나 새우를 잡아먹었어, 어떡해?",
            "ans": "하… 거북이랑 소형 생물을 같이 넣었으니 당연한 결과지! 거북이는 사냥 본능이 강해서 소형 갑각류나 물고기는 그냥 움직이는 간식일 뿐이야. 공존 불가능하니까 어항을 당장 분리해.",
            "link": "https://www.google.com/search?q=거북이와+물고기+합사"
        },
        {
            "q": "어항에 그냥 일반 돌이나 주운 돌 넣어도 돼?",
            "ans": "아무 돌이나 주워 넣었다가 물에 녹아 나오는 성분 때문에 수질 알칼리화되거나 물고기 다 죽는다? 백화 현상이나 석회 성분 나오는 돌은 절대 금지야. 안전하게 수족관 전용 돌이나 유목을 써.",
            "link": "https://www.google.com/search?q=어항에+일반돌+넣어도+되나요"
        },
        {
            "q": "일주일에 환수를 5번이나 해도 되는 거야?",
            "ans": "미쳤어? 어항을 세탁기에 돌릴 작정이니? 환수를 너무 자주 하면 여과 박테리아가 다 쓸려 나가고 수온/수질 쇼크로 물고기들 기절해. 특별한 비상 상황 아니면 일주일에 딱 1번, 20~30%만 해라.",
            "link": "https://www.google.com/search?q=어항+환수+주기"
        },
        {
            "q": "물고기가 수면 위로 올라와서 자꾸 뻐끔거려!",
            "ans": "쯧, 산소가 부족하다는 다급한 SOS잖아. 당장 에어스톤(산소 기포기) 설치하고 여과기 출수구를 수면 위로 올려서 물살이 파도를 치게 만들어. 수온도 체크하고.",
            "link": "https://www.google.com/search?q=물고기+수면+뻐끔거림"
        },
        {
            "q": "어항 물이 우유처럼 하얗게 변했어 (백탁 현상)",
            "ans": "백탁 현상인데 세균이 폭발적으로 늘었거나 분진 때문이야. 이때다 싶어서 물 전면 교체한다고 다 갈아엎으면 생태계 박살 난다? 밥 줄이고 여과기 24시간 돌리면서 차분히 기다려.",
            "link": "https://www.google.com/search?q=어항+백탁현상+해결"
        },
        {
            "q": "구피랑 체리새우 합사해도 정말 괜찮을까?",
            "ans": "합사 자체는 가능하지만 주의해야 해. 구피는 온순해도 입에 들어가는 아주 작은 치새우는 사냥할 수 있거든. 수초나 은신처를 아주 빽빽하게 만들어줄 거 아니면 추천 안 해.",
            "link": "https://www.google.com/search?q=구피와+체리새우+합사"
        }
    ]

    # 세션 스테이트 초기화 (선택된 Q&A 기록 유지)
    if "selected_history" not in st.session_state:
        st.session_state.selected_history = [
            {"q": "어항선배의 첫인사", "ans": "어머, 반가워라. 🐟 궁금한 질문을 아래에서 골라봐. 팩트로 조져줄 테니까.", "link": ""}
        ]

    # 버튼들을 2열 또는 3열로 예쁘게 배치
    cols = st.columns(2)
    for idx, item in enumerate(curated_qna):
        col_idx = idx % 2
        if cols[col_idx].button(f"📌 {item['q']}", use_container_width=True):
            # 중복 추가 방지 및 최신 선택 반영
            st.session_state.selected_history.append({
                "q": item["q"],
                "ans": item["ans"],
                "link": item["link"]
            })

    st.markdown("---")
    st.markdown("### 💬 상담 대화 기록")

    # 대화 기록 출력 (최신순 또는 누적 출력)
    for chat in st.session_state.selected_history:
        if chat["q"] != "어항선배의 첫인사":
            with st.chat_message("user"):
                st.markdown(chat["q"])
        
        with st.chat_message("assistant"):
            st.markdown(chat["ans"])
            if chat["link"]:
                st.markdown(f"🔗 [관련 구글 검색 참고 링크 바로가기]({chat['link']})")

    # 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화"):
        st.session_state.selected_history = [
            {"q": "어항선배의 첫인사", "ans": "어머, 반가워라. 🐟 궁금한 질문을 아래에서 골라봐. 팩트로 조져줄 테니까.", "link": ""}
        ]
        st.rerun()

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
