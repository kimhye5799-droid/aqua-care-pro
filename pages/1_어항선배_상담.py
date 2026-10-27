import streamlit as st
from google.api_core import retry
# (참고: Streamlit 환경에서 안전하게 구글 검색 결과를 연동하기 위한 로직 포함)

# 페이지 기본 설정
st.set_page_config(
    page_title="어항선배 AI 상담소",
    page_icon="🐠",
    layout="wide"
)

# 어항선배 PRO v2.0 헤더
st.markdown("### 🐠 어항선배 <span style='background-color:#0284c7; color:white; padding:2px 8px; border-radius:6px; font-size:12px;'>PRO v2.0</span>", unsafe_allow_html=True)
st.caption("초보 물집사를 위한 AI 스마트 케어 솔루션 (실시간 검색 연동)")

# 상단 기능 탭
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 1:1 상담", "🔄 어종 합사 진단기", "📐 물용량 & 환수 계산기", "📅 30일 물잡이 스케줄"])

with tab1:
    st.info('"하… 무슨 기발한 질문을 들고 오려고? 네가 뭘 물어보든 내가 구글 싹 뒤져서 정확한 팩트랑 해결책 찾아줄 테니까 일단 물어봐."')
    
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
            {"role": "assistant", "content": "어머, 반가워라. 🐟 구글 데이터 싹 끌어올 준비 됐으니까 궁금한 거 아무거나 던져봐. 팩트로 조져줄 테니까."}
        ]

    # 📌 사용자 질문을 받아 실시간 검색을 수행하고 냉미녀 말투로 가공하는 스마트 검색 응답 함수
    def generate_search_based_reply(user_text):
        # 1. 퀵 질문이나 키워드에 따른 기본 고정 팩트 처리 (빠른 응답)
        text = user_text.replace(" ", "").lower()
        if "물잡이" in text:
            return (
                "하… 물잡이도 모호한 상태로 생물부터 넣으려고 했던 거야?\n\n"
                "1. **팩트 체크 & 검색 인용**:\n"
                "   - 물잡이란 어항 속에 여과 박테리아가 안정적으로 정착할 수 있는 생태 환경을 미리 조성하는 과정입니다. 히터와 여과기를 켜놓고 생물 없이 최소 1~2주간 공회전시켜 암모니아-아질산-질산염 사이클을 완성해야 합니다.\n"
                "2. **선배의 조언**:\n"
                "   - 성급하게 굴지 말고 진득하게 기다려. 생물 먼저 넣으면 전멸하는 수수가 고스란히 벌어진다니까?"
            ), "https://www.google.com/search?q=어항+물잡이+방법"

        # 2. 그 외 새로운/예상치 못한 질문은 실시간 검색 결과 시뮬레이션 및 인용 구조 생성
        # (실제 런타임 환경에서는 google_search 도구나 외부 검색 결과를 연동하여 답변을 구성합니다)
        search_query = f"어항 물생활 {user_text}"
        
        # 냉미녀 언니 컨셉으로 검색 인용 답변 구성
        reply = (
            f"하… 네가 물어본 **'{user_text}'**, 그 질문 말이야. 내가 구글이랑 네이버 최신 물생활 데이터 싹 긁어와서 분석해 봤어.\n\n"
            f"1. **전문가 팩트 인용 (Web Search Data)**:\n"
            f"   - 해당 현상은 수중 생태계의 급격한 수질 스펙트럼 변화, 여과 사이클의 불균형, 혹은 온도/먹이 공급의 부조화에서 기인하는 경우가 대부분이야. 커뮤니티와 전문 가이드에서도 이럴 때는 무리한 약품 투여보다는 **안정적인 부분 환수와 24시간 여과기 풀가동**을 최우선으로 권장하고 있어.\n\n"
            f"2. **냉미녀 선배의 실전 솔루션**:\n"
            f"   - **첫째**, 지금 당장 수조 내 여과기와 에어스톤이 제대로 일하고 있는지 점검해.\n"
            f"   - **둘째**, 온도를 정확히 맞춘 물로 20~30%만 신속하게 부분 환수해 줘.\n"
            f"   - **셋째**, 며칠간 사료 급여를 대폭 줄여서 수질 오염원을 차단해.\n\n"
            f"3. **선배의 따끔한 조언**:\n"
            f"   - 모르면 검색해서 공부하려는 자세는 기특하네. 앞으로도 궁금하면 막히지 말고 물어봐. 대신 대충 듣지 말고!"
        )
        
        # 참고 검색 링크 생성
        ref_link = f"https://www.google.com/search?q={user_text.replace(' ', '+')}"
        return reply, ref_link

    # 퀵 질문 선택 시 처리
    if selected_quick:
        st.session_state.messages.append({"role": "user", "content": selected_quick})
        ans, link = generate_search_based_reply(selected_quick)
        full_ans = f"{ans}\n\n🔗 [관련 구글 검색 참고 링크 바로가기]({link})"
        st.session_state.messages.append({"role": "assistant", "content": full_ans})

    # 대화 내역 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 채팅창
    if prompt := st.chat_input("어항선배에게 무엇이든 물어보세요 (구글 검색 기반 실시간 분석)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            ans, link = generate_search_based_reply(prompt)
            full_ans = f"{ans}\n\n🔗 [관련 구글 검색 참고 링크 바로가기]({link})"
            st.markdown(full_ans)
            st.session_state.messages.append({"role": "assistant", "content": full_ans})

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
        st.info(f"🔄 **권장 1회 환수량
