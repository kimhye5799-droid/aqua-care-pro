import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="AquaCare Pro", page_icon="🐠", layout="wide")

# 2. 어종별 생태 데이터베이스 (담수/해수/열대 분류, 수온, 성격, 성체크기)
FISH_DATABASE = {
    "구피": {"category": "열대어", "salinity": "담수", "emoji": "🐠", "temp": (22, 28), "temperament": "순함", "size_cm": 4},
    "네온테트라": {"category": "열대어", "salinity": "담수", "emoji": "🐟", "temp": (21, 26), "temperament": "순함", "size_cm": 3},
    "베타": {"category": "열대어", "salinity": "담수", "emoji": "🥊", "temp": (24, 30), "temperament": "공격적", "size_cm": 6},
    "엔젤피쉬": {"category": "열대어", "salinity": "담수", "emoji": "🐡", "temp": (24, 28), "temperament": "보통", "size_cm": 12},
    "넙치(광어)": {"category": "해수어", "salinity": "해수", "emoji": "🐟", "temp": (18, 24), "temperament": "순함", "size_cm": 30},
    "조피볼락(우럭)": {"category": "해수어", "salinity": "해수", "emoji": "🐠", "temp": (15, 21), "temperament": "순함", "size_cm": 25},
    "송어": {"category": "담수어", "salinity": "담수", "emoji": "🐟", "temp": (10, 18), "temperament": "순함", "size_cm": 20}
}

# 3. 사이드바 - [고민 선택 및 어황 설정]
st.sidebar.header("🎯 해결하고 싶은 고민 선택")
problem_type = st.sidebar.radio(
    "어떤 고민을 진단해 드릴까요?",
    [
        "🍖 적정 사료량 계산 (수온 대사율 반영)",
        "🥊 합사 가능 여부 및 삼투압 진단",
        "🏠 수조 과밀 여부 진단",
        "🌡️ 수질 및 환경 맞춤 가이드",
        "🩺 어종별 질병 예찰 및 대처"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("🌊 어항 생태계 설정")

# 어종 다중 선택
selected_fishes = st.sidebar.multiselect(
    "어항에 넣을 어종을 선택하세요 (여러 개 선택 가능):",
    list(FISH_DATABASE.keys()),
    default=["구피"]
)

# 세부 환경 입력
count = st.sidebar.number_input("총 개체 수 (마리)", min_value=1, value=5, step=1)
tank_volume_l = st.sidebar.number_input("어항/수조 용량 (L)", min_value=1, value=30, step=5)
current_temp = st.sidebar.slider("현재 사육 수온 (°C)", min_value=5.0, max_value=35.0, value=25.0, step=0.5)

# 4. 동적 배경 및 테마 자동 판별
current_env = "기본"
if selected_fishes:
    categories = [FISH_DATABASE[fish]["category"] for fish in selected_fishes]
    if "해수어" in categories:
        current_env = "해수어"
    elif "열대어" in categories:
        current_env = "열대어"
    else:
        current_env = "담수어"

BACKGROUND_STYLES = {
    "기본": {"bg_color": "linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 100%)", "border_color": "#00bcd4", "title": "🫧 기본 수조"},
    "담수어": {"bg_color": "linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%)", "border_color": "#4caf50", "title": "🌿 수초 담수 생태계"},
    "해수어": {"bg_color": "linear-gradient(180deg, #e0f2fe 0%, #0284c7 100%)", "border_color": "#0369a1", "title": "🌊 푸른 바다(해수) 생태계"},
    "열대어": {"bg_color": "linear-gradient(180deg, #f3e5f5 0%, #e1bee7 100%)", "border_color": "#ab47bc", "title": "🪸 화려한 열대 산호초"}
}

style = BACKGROUND_STYLES[current_env]

# Custom CSS 주입으로 배경 전환
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {style['bg_color']};
        transition: background 0.8s ease-in-out;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐠 AquaCare Pro - 고민 맞춤형 수산/어항 진단 플랫폼")
st.caption(f"현재 테마: **{style['title']}**")
st.markdown("---")

# 5. 가상 어항 시각화 영역
if selected_fishes:
    tank_icons = [FISH_DATABASE[fish]["emoji"] for fish in selected_fishes]
    fish_display = " ".join(tank_icons * max(1, count // len(selected_fishes)))

    st.markdown(
        f"""
        <div style="
            border: 4px solid {style['border_color']}; 
            border-radius: 20px; 
            padding: 30px; 
            text-align: center; 
            font-size: 35px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(5px);">
            🌊 {style['title']} 🌊<br><br>
            {fish_display}<br><br>
            🪨 🌿 🐚 🪸 🪨
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # 6. 고민 선택별 결과 솔루션 출력
    st.subheader(f"📊 진단 결과: {problem_type}")

    # 공통 삼투압 오류 체크 (담수어 + 해수어 조합)
    salinities = set([FISH_DATABASE[f]["salinity"] for f in selected_fishes])
    if "담수" in salinities and "해수" in salinities:
        st.error("🚨 [치명적 예외] 담수어(민물)와 해수어(바닷물)는 삼투압 체계가 달라 절대 한 어항에서 살 수 없습니다!")

    # 고민 1: 사료량 계산
    if "적정 사료량" in problem_type:
        avg_weight = 10.0  # 평균 체중 10g 기준
        total_biomass_g = count * avg_weight
        
        # 수온 대사율 보정
        if 20.0 <= current_temp <= 28.0:
            metabolic_factor = 1.0
            status_msg = "적정 수온 (100% 정상 급여)"
        elif current_temp < 20.0:
            metabolic_factor = max(0.2, 1.0 - (20.0 - current_temp) * 0.08)
            status_msg = f"저수온 대사 저하 ({int(metabolic_factor*100)}% 감량 급여)"
        else:
            metabolic_factor = max(0.1, 1.0 - (current_temp - 28.0) * 0.1)
            status_msg = f"고수온 스트레스 ({int(metabolic_factor*100)}% 절감 급여)"
            
        daily_feed_g = (total_biomass_g * 0.03) * metabolic_factor
        
        col1, col2 = st.columns(2)
        col1.metric("🐟 일일 추천 총 사료량", f"{daily_feed_g:.2f} g")
        col2.metric("🌡️ 수온 대사 상태", status_msg)
        st.info("💡 Tip: 사료는 1일 2~3회 분할 급여하며, 5분 내에 남은 잔반은 수질 오염 방지를 위해 뜰채로 제거하세요.")

    # 고민 2: 합사 가능 여부
    elif "합사 가능" in problem_type:
        temperaments = [FISH_DATABASE[f]["temperament"] for f in selected_fishes]
        if "베타" in selected_fishes and len(selected_fishes) > 1:
            st.error("⚠️ [합사 위험] '베타'는 강한 공격성/영역 다툼으로 타 어종과의 합사를 추천하지 않습니다.")
        elif "공격적" in temperaments:
            st.warning("⚠️ [주의] 공격성이 있는 어종이 포함되어 있습니다. 지느러미 손상 여부를 잘 관찰하세요.")
        else:
            st.success("✅ 선택하신 어종들은 전반적으로 순한 성격으로 합사가 원활합니다.")

    # 고민 3: 수조 과밀 여부
    elif "수조 과밀" in problem_type:
        total_required_volume = sum([FISH_DATABASE[f]["size_cm"] for f in selected_fishes]) * (count / len(selected_fishes))
        density_ratio = (total_required_volume / tank_volume_l) * 100
        
        col1, col2 = st.columns(2)
        col1.metric("🏠 현재 수조 필요 최소 용량", f"{total_required_volume:.1f} L")
        col2.metric("📊 수조 과밀도", f"{density_ratio:.1f} %")
        
        if density_ratio > 100:
            st.warning("⚠️ [수조 과밀] 어항 용량 대비 물고기가 많습니다. 여과력을 높이거나 넓은 수조로 이동을 권장합니다.")
        else:
            st.success("✅ 어항 크기 대비 쾌적한 사육 환경입니다.")

    # 고민 4: 환경 관리
    elif "수질 및 환경" in problem_type:
        st.write("🌡️ **선택 어종 적정 수온 범위**")
        for fish in selected_fishes:
            min_t, max_t = FISH_DATABASE[fish]["temp"]
            status = "정상" if min_t <= current_temp <= max_t else "범위 벗어남"
            st.write(f"- **{fish}**: {min_t}~{max_t}°C (현재 수온 상태: **{status}**)")

    # 고민 5: 질병 예찰
    elif "질병 예찰" in problem_type:
        st.info("🩺 **어종별 주의 질병 안내**")
        if current_temp < 18.0:
            st.warning("⚠️ 저수온 구간: 백점병 및 곰팡이성 질병 유발 가능성이 높습니다. 히터를 점검하세요.")
        elif current_temp > 29.0:
            st.warning("⚠️ 고수온 구간: 용존산소 감소 및 세균성 감염(연쇄구균 등) 위험이 올라갑니다.")
        else:
            st.success("✅ 현재 수온은 면역력 유지에 안정적인 구간입니다.")

else:
    st.info("👈 좌측 사이드바에서 어종을 하나 이상 선택해 주세요!")
