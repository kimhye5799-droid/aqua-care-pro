import streamlit as st

# ==================================================
# 1. 페이지 기본 설정
# ==================================================
st.set_page_config(
    page_title="AquaCare Pro",
    page_icon="🐠",
    layout="wide"
)


# ==================================================
# 2. 어종별 생태 데이터베이스 (총 16종)
# ==================================================
FISH_DATABASE = {
    "체리새우": {
        "category": "담수어", "salinity": "담수",
        "emoji": "🦐", "temp": (20, 26),
        "temperament": "순함", "size_cm": 3
    },
    "구피": {
        "category": "열대어", "salinity": "담수",
        "emoji": "🐟", "temp": (22, 28),
        "temperament": "순함", "size_cm": 4
    },
    "네온테트라": {
        "category": "열대어", "salinity": "담수",
        "emoji": "🐟", "temp": (21, 26),
        "temperament": "순함", "size_cm": 3
    },
    "베타": {
        "category": "열대어", "salinity": "담수",
        "emoji": "🐠", "temp": (24, 30),
        "temperament": "공격적", "size_cm": 6
    },
    "애플스네일": {
        "category": "담수어", "salinity": "담수",
        "emoji": "🐌", "temp": (20, 28),
        "temperament": "순함", "size_cm": 5
    },
    "디스커스": {
        "category": "열대어", "salinity": "담수",
        "emoji": "🐟", "temp": (28, 30),
        "temperament": "보통", "size_cm": 15
    },
    "엔젤피쉬": {
        "category": "열대어", "salinity": "담수",
        "emoji": "🐠", "temp": (24, 28),
        "temperament": "보통", "size_cm": 12
    },
    "반수생거북": {
        "category": "담수어", "salinity": "담수",
        "emoji": "🐢", "temp": (24, 28),
        "temperament": "보통", "size_cm": 15
    },
    "크라운피쉬": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐠", "temp": (24, 28),
        "temperament": "보통", "size_cm": 10
    },
    "블루탱": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐟", "temp": (24, 28),
        "temperament": "보통", "size_cm": 20
    },
    "해마": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐴", "temp": (22, 26),
        "temperament": "순함", "size_cm": 12
    },
    "복어": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐡", "temp": (23, 27),
        "temperament": "보통", "size_cm": 15
    },
    "박스피쉬": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐡", "temp": (24, 27),
        "temperament": "순함", "size_cm": 15
    },
    "옐로우탱": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐠", "temp": (24, 28),
        "temperament": "보통", "size_cm": 15
    },
    "퀸엔젤": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐠", "temp": (24, 27),
        "temperament": "보통", "size_cm": 25
    },
    "바다거북": {
        "category": "해수어", "salinity": "해수",
        "emoji": "🐢", "temp": (24, 28),
        "temperament": "순함", "size_cm": 30
    }
}


# ==================================================
# 3. 생물별 그림 색상 설정
# ==================================================
FISH_COLORS = {
    "체리새우": "#ed4b5c",
    "구피": "#35b9ed",
    "네온테트라": "#35e5dc",
    "베타": "#ed64a6",
    "애플스네일": "#d99a45",
    "디스커스": "#e85b48",
    "엔젤피쉬": "#f1d9ed",
    "반수생거북": "#55a86a",
    "크라운피쉬": "#ff873e",
    "블루탱": "#247be9",
    "해마": "#e8b94c",
    "복어": "#e5bd70",
    "박스피쉬": "#f2b83f",
    "옐로우탱": "#f5df28",
    "퀸엔젤": "#eaa94c",
    "바다거북": "#398d71"
}


# ==================================================
# 4. 생물별 SVG 그림 생성 함수
# ==================================================
def draw_fish(name, index=0):

    color = FISH_COLORS[name]

    # 체리새우
    if name == "체리새우":
        shape = f"""
        <path d="M45 40 Q60 15 85 35
        Q100 50 85 65 Q60 80 45 55"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M45 40 L25 25 L30 50 L25 70 L45 55"
        fill="{color}"/>
        <path d="M52 62 L48 78 M62 65 L60 80
        M72 64 L75 78"
        stroke="{color}" stroke-width="3"/>
        <path d="M45 35 L30 18 M50 33 L40 15"
        stroke="{color}" stroke-width="2"/>
        """

    # 애플스네일
    elif name == "애플스네일":
        shape = f"""
        <path d="M35 65 Q60 75 95 65 L90 75 L40 75 Z"
        fill="{color}"/>
        <circle cx="65" cy="45" r="27"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M65 45 Q90 15 78 45
        Q60 65 65 45"
        fill="none" stroke="#9b6332" stroke-width="3"/>
        <path d="M85 23 L90 10 M95 23 L103 12"
        stroke="{color}" stroke-width="3"/>
        """

    # 거북이
    elif name in ["반수생거북", "바다거북"]:
        shape = f"""
        <ellipse cx="65" cy="48" rx="34" ry="24"
        fill="{color}" stroke="white" stroke-width="2"/>
        <circle cx="105" cy="45" r="11" fill="{color}"/>
        <path d="M40 30 L25 18 L35 42
        M40 65 L25 80 L48 68
        M85 30 L100 17 L94 40
        M85 65 L100 80 L90 65"
        fill="{color}" stroke="{color}" stroke-width="4"/>
        <path d="M45 48 L65 27 L85 48 L65 68 Z"
        fill="none" stroke="#235e43" stroke-width="2"/>
        """

    # 해마
    elif name == "해마":
        shape = f"""
        <path d="M70 75 Q45 80 52 58
        Q30 40 55 25 Q75 10 78 30
        Q90 48 72 55 Q60 65 78 68 L85 80"
        fill="none" stroke="{color}"
        stroke-width="12" stroke-linecap="round"/>
        <path d="M76 30 L105 25 L78 40"
        fill="{color}"/>
        """

    # 박스피쉬
    elif name == "박스피쉬":
        shape = f"""
        <rect x="35" y="23" width="65" height="50"
        rx="13" fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M35 35 L15 25 L15 70 L35 60"
        fill="{color}"/>
        <path d="M50 28 L50 68 M75 28 L75 68"
        stroke="#9b7a32" stroke-width="2"/>
        """

    # 복어
    elif name == "복어":
        shape = f"""
        <path d="M25 48 L5 25 L5 70 Z" fill="{color}"/>
        <circle cx="65" cy="48" r="32"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M40 25 L35 15 M55 17 L55 7
        M75 17 L80 7 M90 30 L100 20
        M95 50 L108 50"
        stroke="white" stroke-width="3"/>
        <circle cx="55" cy="55" r="3" fill="#a67c32"/>
        <circle cx="75" cy="60" r="3" fill="#a67c32"/>
        """

    # 기본 물고기 모양
    else:
        shape = f"""
        <path d="M25 48 L5 25 L5 70 Z"
        fill="{color}" stroke="white" stroke-width="1"/>
        <path d="M20 48 Q35 12 85 30
        Q110 48 85 66 Q35 84 20 48 Z"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M55 25 L70 10 L85 29"
        fill="{color}"/>
        <path d="M55 65 L70 80 L85 65"
        fill="{color}"/>
        """

        # 네온테트라 줄무늬
        if name == "네온테트라":
            shape += """
            <path d="M35 43 Q55 35 80 43"
            stroke="#ff4d9d" stroke-width="3" fill="none"/>
            <path d="M35 48 Q55 43 80 48"
            stroke="#35ffff" stroke-width="4" fill="none"/>
            """

        # 크라운피쉬 줄무늬
        elif name == "크라운피쉬":
            shape += """
            <path d="M42 25 L48 68 M65 24 L72 68"
            stroke="white" stroke-width="6"/>
            """

        # 퀸엔젤 무늬
        elif name == "퀸엔젤":
            shape += """
            <path d="M35 35 L85 35 M35 45 L85 45
            M35 55 L85 55"
            stroke="#2565a8" stroke-width="3"/>
            """

        # 베타의 큰 지느러미
        elif name == "베타":
            shape += """
            <path d="M45 30 Q60 0 90 12
            Q80 30 85 35"
            fill="#a83d8d" opacity="0.8"/>
            <path d="M45 65 Q65 90 95 80
            Q80 65 85 60"
            fill="#a83d8d" opacity="0.8"/>
            """

        # 구피의 화려한 꼬리
        elif name == "구피":
            shape += """
            <path d="M28 48 Q0 5 10 48
            Q0 90 28 48"
            fill="#f5a5dc" stroke="white" stroke-width="1"/>
            """

        # 디스커스의 둥근 무늬
        elif name == "디스커스":
            shape += """
            <circle cx="55" cy="42" r="5"
            fill="#f6b94a"/>
            <circle cx="70" cy="55" r="5"
            fill="#f6b94a"/>
            <circle cx="45" cy="55" r="4"
            fill="#f6b94a"/>
            """

        # 엔젤피쉬의 긴 지느러미
        elif name == "엔젤피쉬":
            shape += """
            <path d="M50 25 L65 0 L75 25
            M50 65 L65 90 L75 65"
            fill="none" stroke="white" stroke-width="2"/>
            """

    # 눈 위치 및 SVG 완성
    eye = """
    <circle cx="87" cy="42" r="3.5" fill="white"/>
    <circle cx="88" cy="42" r="1.8" fill="#172033"/>
    """

    if name in ["반수생거북", "바다거북"]:
        eye = """
        <circle cx="108" cy="42" r="3" fill="white"/>
        <circle cx="109" cy="42" r="1.5" fill="#172033"/>
        """
    elif name == "해마":
        eye = """
        <circle cx="78" cy="27" r="3" fill="white"/>
        <circle cx="79" cy="27" r="1.5" fill="#172033"/>
        """
    elif name in ["애플스네일"]:
        eye = ""

    return f"""
    <svg width="130" height="90"
         viewBox="0 0 120 90"
         xmlns="http://www.w3.org/2000/svg">
        {shape}
        {eye}
    </svg>
    """


# ==================================================
# 5. 사이드바 - 고민 선택
# ==================================================
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


# ==================================================
# 6. 어종 다중 선택
# ==================================================
selected_fishes = st.sidebar.multiselect(
    "어항에 넣을 생물 종류를 선택하세요:",
    list(FISH_DATABASE.keys()),
    default=["엔젤피쉬", "네온테트라"]
)


# ==================================================
# 7. 세부 환경 입력
# ==================================================
count = st.sidebar.number_input(
    "총 개체 수 (마리)",
    min_value=1,
    value=7,
    step=1
)

tank_volume_l = st.sidebar.number_input(
    "어항/수조 용량 (L)",
    min_value=1,
    value=50,
    step=5
)

current_temp = st.sidebar.slider(
    "현재 사육 수온 (°C)",
    min_value=5.0,
    max_value=35.0,
    value=23.0,
    step=0.5
)


# ==================================================
# 8. 어항 환경 및 테마 자동 판별
# ==================================================
current_env = "기본"

if selected_fishes:

    salinities = {
        FISH_DATABASE[fish]["salinity"]
        for fish in selected_fishes
    }

    if len(salinities) > 1:
        current_env = "기본"

    elif "해수" in salinities:
        current_env = "해수어"

    elif any(
        FISH_DATABASE[fish]["category"] == "열대어"
        for fish in selected_fishes
    ):
        current_env = "열대어"

    else:
        current_env = "담수어"


# ==================================================
# 9. 배경 테마 설정
# ==================================================
BACKGROUND_STYLES = {

    "기본": {
        "bg_color": "linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 100%)",
        "border_color": "#00bcd4",
        "title": "🫧 기본 수조"
    },

    "담수어": {
        "bg_color": "linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%)",
        "border_color": "#4caf50",
        "title": "🌿 수초 담수 생태계"
    },

    "해수어": {
        "bg_color": "linear-gradient(180deg, #e0f2fe 0%, #0284c7 100%)",
        "border_color": "#0369a1",
        "title": "🌊 푸른 바다 생태계"
    },

    "열대어": {
        "bg_color": "linear-gradient(180deg, #f3e5f5 0%, #e1bee7 100%)",
        "border_color": "#ab47bc",
        "title": "🪸 화려한 열대 생태계"
    }
}

style = BACKGROUND_STYLES[current_env]


# ==================================================
# 10. Custom CSS 및 애니메이션
# ==================================================
st.markdown(
    f"""
    <style>

    .stApp {{
        background: {style['bg_color']};
        transition: background 0.8s ease-in-out;
    }}

    .fish-tank {{
        display: grid;
        grid-template-columns:
            repeat(auto-fit, minmax(140px, 1fr));
        gap: 18px;
        padding: 25px;
        min-height: 300px;
        align-items: center;
        justify-items: center;
        overflow: hidden;
    }}

    .fish-item {{
        width: 140px;
        height: 125px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 15px;
        animation: swim 3s ease-in-out infinite;
    }}

    .fish-item:nth-child(even) {{
        animation-delay: 0.8s;
    }}

    .fish-item svg {{
        max-width: 100%;
        overflow: visible;
    }}

    .fish-name {{
        color: white;
        font-size: 13px;
        font-weight: bold;
        margin-top: 3px;
    }}

    @keyframes swim {{
        0%, 100% {{
            transform: translateY(0);
        }}

        50% {{
            transform: translateY(-7px);
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 11. 메인 화면 제목
# ==================================================
st.title("🐠 AquaCare Pro - 고민 맞춤형 수산/어항 진단 플랫폼")

st.caption(f"현재 테마: **{style['title']}**")

st.markdown("---")


# ==================================================
# 12. 가상 어항 시각화
# ==================================================
if selected_fishes:

    tank_html = ""

    # 전체 개체 수만큼 생물 그림 생성
    for idx in range(count):

        fish_name = selected_fishes[idx % len(selected_fishes)]

        tank_html += f"""
        <div class="fish-item">
            {draw_fish(fish_name, idx)}
            <div class="fish-name">
                {FISH_DATABASE[fish_name]['emoji']} {fish_name}
            </div>
        </div>
        """

    st.markdown(
        f"""
        <div class="fish-tank"
             style="
                background: {style['bg_color']};
                border: 4px solid {style['border_color']};
                border-radius: 20px;
             ">

            {tank_html}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # ==================================================
    # 13. 고민 선택별 진단 결과
    # ==================================================
    st.subheader(f"📊 진단 결과: {problem_type}")


    # --------------------------------------------------
    # 공통 삼투압 오류 체크
    # --------------------------------------------------
    salinities = {
        FISH_DATABASE[fish]["salinity"]
        for fish in selected_fishes
    }

    if "담수" in salinities and "해수" in salinities:

        st.error(
            "🚨 [치명적 예외] "
            "담수어와 해수어는 삼투압 체계가 달라 "
            "한 어항에서 함께 사육할 수 없습니다!"
        )


    # ==================================================
    # 고민 1. 적정 사료량 계산
    # ==================================================
    if "적정 사료량" in problem_type:

        avg_weight = 10.0

        total_biomass_g = count * avg_weight

        # 수온 대사율 보정
        if 20.0 <= current_temp <= 28.0:

            metabolic_factor = 1.0
            status_msg = "적정 수온 (기준 급여량)"

        elif current_temp < 20.0:

            metabolic_factor = max(
                0.2,
                1.0 - (20.0 - current_temp) * 0.08
            )

            status_msg = (
                f"저수온 대사 저하 "
                f"({int(metabolic_factor * 100)}% 기준)"
            )

        else:

            metabolic_factor = max(
                0.1,
                1.0 - (current_temp - 28.0) * 0.1
            )

            status_msg = (
                f"고수온 스트레스 "
                f"({int(metabolic_factor * 100)}% 기준)"
            )

        daily_feed_g = (
            total_biomass_g * 0.03
        ) * metabolic_factor

        col1, col2 = st.columns(2)

        col1.metric(
            "🐟 일일 참고 사료량",
            f"{daily_feed_g:.2f} g"
        )

        col2.metric(
            "🌡️ 수온 대사 상태",
            status_msg
        )

        st.info(
            "💡 Tip: 사료량은 어종과 성장 단계에 따라 달라집니다. "
            "소량씩 급여하고 남은 사료는 제거해 주세요."
        )


    # ==================================================
    # 고민 2. 합사 가능 여부
    # ==================================================
    elif "합사 가능" in problem_type:

        temperaments = [
            FISH_DATABASE[fish]["temperament"]
            for fish in selected_fishes
        ]

        if len(salinities) > 1:

            st.error(
                "🚨 담수 생물과 해수 생물이 함께 선택되어 "
                "합사를 추천하지 않습니다."
            )

        elif "베타" in selected_fishes and len(selected_fishes) > 1:

            st.error(
                "⚠️ [합사 위험] 베타는 영역 다툼이 발생할 수 있어 "
                "다른 어종과의 합사에 주의해야 합니다."
            )

        elif "공격적" in temperaments:

            st.warning(
                "⚠️ 공격성이 있는 생물이 포함되어 있습니다. "
                "서로의 행동을 관찰해 주세요."
            )

        else:

            st.success(
                "✅ 선택한 생물의 성격은 전반적으로 "
                "온순하거나 보통 수준입니다."
            )

        st.info(
            "💡 실제 합사 가능 여부는 성체 크기, 수조 크기, "
            "영역성 및 개체별 성향도 함께 확인해야 합니다."
        )


    # ==================================================
    # 고민 3. 수조 과밀 여부
    # ==================================================
    elif "수조 과밀" in problem_type:

        total_required_volume = (
            sum(
                FISH_DATABASE[fish]["size_cm"]
                for fish in selected_fishes
            ) / len(selected_fishes)
        ) * count

        density_ratio = (
            total_required_volume / tank_volume_l
        ) * 100

        col1, col2 = st.columns(2)

        col1.metric(
            "🏠 크기 기반 참고 지표",
            f"{total_required_volume:.1f}"
        )

        col2.metric(
            "📊 참고 비율",
            f"{density_ratio:.1f}%"
        )

        st.info(
            "💡 위 수치는 어종별 크기를 이용한 단순 참고 지표이며, "
            "실제 적정 수조 용량을 계산한 값은 아닙니다."
        )

        if density_ratio > 100:

            st.warning(
                "⚠️ 수조 환경을 다시 확인해 주세요. "
                "더 넓은 수조와 충분한 여과력이 필요할 수 있습니다."
            )

        else:

            st.success(
                "✅ 단순 크기 참고 지표상 100% 이하입니다. "
                "실제 사육 밀도와 여과력도 확인해 주세요."
            )


    # ==================================================
    # 고민 4. 수질 및 환경 관리
    # ==================================================
    elif "수질 및 환경" in problem_type:

        st.write("🌡️ **선택 어종별 적정 수온 범위**")

        for fish in selected_fishes:

            min_t, max_t = FISH_DATABASE[fish]["temp"]

            status = (
                "정상"
                if min_t <= current_temp <= max_t
                else "범위 벗어남"
            )

            st.write(
                f"- **{fish}**: "
                f"{min_t}~{max_t}°C "
                f"(현재 수온: **{status}**)"
            )

        st.info(
            "💡 수온 외에도 pH, 암모니아, 아질산염, "
            "질산염 및 용존산소를 확인해야 합니다."
        )


    # ==================================================
    # 고민 5. 질병 예찰 및 대처
    # ==================================================
    elif "질병 예찰" in problem_type:

        st.info("🩺 **어종별 질병 및 환경 주의 안내**")

        if current_temp < 18.0:

            st.warning(
                "⚠️ 저수온 상태입니다. "
                "어종별 적정 수온을 확인하고 "
                "급격한 온도 변화를 피하세요."
            )

        elif current_temp > 29.0:

            st.warning(
                "⚠️ 고수온 상태입니다. "
                "용존산소 부족과 수질 악화에 주의하세요."
            )

        else:

            st.success(
                "✅ 현재 수온은 일반적인 참고 범위에 있습니다. "
                "다만 어종별 적정 수온을 반드시 확인하세요."
            )

        st.write("**선택 어종별 수온 확인**")

        for fish in selected_fishes:

            min_t, max_t = FISH_DATABASE[fish]["temp"]

            status = (
                "적정"
                if min_t <= current_temp <= max_t
                else "주의"
            )

            st.write(
                f"- {fish}: {min_t}~{max_t}°C / {status}"
            )

        st.info(
            "💡 질병이 의심되면 수질과 행동 변화를 먼저 확인하고 "
            "수산생물 전문가의 진단을 받는 것이 좋습니다."
        )


# ==================================================
# 14. 어종을 선택하지 않았을 때
# ==================================================
else:

    st.info(
        "👈 좌측 사이드바에서 어종을 하나 이상 선택해 주세요!"
    )
