import streamlit as st
import streamlit.components.v1 as components

# ==================================================
# 1. 페이지 기본 설정
# ==================================================
# Streamlit 페이지의 제목과 화면 레이아웃을 설정
st.set_page_config(
    page_title="AquaCare Pro",
    page_icon="🐠",
    layout="wide"
)


# ==================================================
# 2. 어종별 생태 데이터베이스
# 어종별 생태 정보와 사육 환경을 저장
# ==================================================
# 체리새우의 기본 사육 정보를 등록
FISH_DATABASE = {
    "체리새우": {"category": "담수어", "salinity": "담수", "emoji": "🦐", "temp": (20, 26), "temperament": "순함", "size_cm": 3},
    "구피": {"category": "열대어", "salinity": "담수", "emoji": "🐟", "temp": (22, 28), "temperament": "순함", "size_cm": 4},
    "네온테트라": {"category": "열대어", "salinity": "담수", "emoji": "🐟", "temp": (21, 26), "temperament": "순함", "size_cm": 3},
    "베타": {"category": "열대어", "salinity": "담수", "emoji": "🐠", "temp": (24, 30), "temperament": "공격적", "size_cm": 6},
    "애플스네일": {"category": "담수어", "salinity": "담수", "emoji": "🐌", "temp": (20, 28), "temperament": "순함", "size_cm": 5},
    "디스커스": {"category": "열대어", "salinity": "담수", "emoji": "🐟", "temp": (28, 30), "temperament": "보통", "size_cm": 15},
    "엔젤피쉬": {"category": "열대어", "salinity": "담수", "emoji": "🐠", "temp": (24, 28), "temperament": "보통", "size_cm": 12},
    "반수생거북": {"category": "담수어", "salinity": "담수", "emoji": "🐢", "temp": (24, 28), "temperament": "보통", "size_cm": 15},
    "크라운피쉬": {"category": "해수어", "salinity": "해수", "emoji": "🐠", "temp": (24, 28), "temperament": "보통", "size_cm": 10},
    "블루탱": {"category": "해수어", "salinity": "해수", "emoji": "🐟", "temp": (24, 28), "temperament": "보통", "size_cm": 20},
    "해마": {"category": "해수어", "salinity": "해수", "emoji": "🐴", "temp": (22, 26), "temperament": "순함", "size_cm": 12},
    "복어": {"category": "해수어", "salinity": "해수", "emoji": "🐡", "temp": (23, 27), "temperament": "보통", "size_cm": 15},
    "박스피쉬": {"category": "해수어", "salinity": "해수", "emoji": "🐡", "temp": (24, 27), "temperament": "순함", "size_cm": 15},
    "옐로우탱": {"category": "해수어", "salinity": "해수", "emoji": "🐠", "temp": (24, 28), "temperament": "보통", "size_cm": 15},
    "퀸엔젤": {"category": "해수어", "salinity": "해수", "emoji": "🐠", "temp": (24, 27), "temperament": "보통", "size_cm": 25},
    "바다거북": {"category": "해수어", "salinity": "해수", "emoji": "🐢", "temp": (24, 28), "temperament": "순함", "size_cm": 30}
}

# 생물 종류에 따른 그림 색상을 관리
# ==================================================
# 3. 생물별 그림 색상
# ==================================================
FISH_COLORS = {
    # 체리새우 그림에 사용할 색상을 지정
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
# 선택한 생물에 맞는 그림 색상을 불러옴
# 4. 물고기 SVG 그림 생성 함수
# ==================================================
def draw_fish(name):

    color = FISH_COLORS[name]
    # 체리새우의 그림 모양을 생성

    # 체리새우
    if name == "체리새우":
        shape = f"""
        <path d="M40 40 Q55 15 85 35 Q100 50 85 65 Q55 80 40 55 Z"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M42 40 L20 20 L25 50 L20 75 L42 58"
        fill="{color}"/>
        <path d="M50 60 L45 78 M60 65 L60 82 M70 64 L75 80"
        stroke="{color}" stroke-width="3"/>
        <path d="M45 35 L35 15 M55 30 L50 12"
        stroke="{color}" stroke-width="3"/>
        """
# 애플스네일의 껍데기와 몸 모양을 생성
    # 애플스네일
    elif name == "애플스네일":
        shape = f"""
        <path d="M30 65 Q60 80 100 65 L90 78 L35 78 Z"
        fill="{color}"/>
        <circle cx="62" cy="43" r="28"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M62 43 Q90 15 77 43 Q60 65 62 43"
        fill="none" stroke="#8c542d" stroke-width="3"/>
        <path d="M85 20 L90 8 M95 20 L103 10"
        stroke="{color}" stroke-width="3"/>
        """
# 거북이의 몸과 다리 모양을 생성
    # 거북이
    elif name in ["반수생거북", "바다거북"]:
        shape = f"""
        <ellipse cx="62" cy="48" rx="34" ry="24"
        fill="{color}" stroke="white" stroke-width="2"/>
        <circle cx="105" cy="45" r="11" fill="{color}"/>
        <path d="M40 30 L23 15 L35 42
        M40 65 L23 82 L48 68
        M85 30 L100 15 L94 40
        M85 65 L100 82 L90 65"
        fill="{color}" stroke="{color}" stroke-width="4"/>
        <path d="M45 48 L62 27 L80 48 L62 68 Z"
        fill="none" stroke="#235e43" stroke-width="2"/>
        """
# 해마의 특징적인 곡선 모양을 표현
    # 해마
    elif name == "해마":
        shape = f"""
        <path d="M70 75 Q45 80 52 58
        Q30 40 55 25 Q75 10 78 30
        Q90 48 72 55 Q60 65 78 68 L85 80"
        fill="none" stroke="{color}" stroke-width="12"
        stroke-linecap="round"/>
        <path d="M76 30 L105 25 L78 40" fill="{color}"/>
        """
# 박스피쉬의 네모난 몸 모양을 생성
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
# 복어의 둥근 몸과 무늬를 표현
    # 복어
    elif name == "복어":
        shape = f"""
        <path d="M30 48 L5 25 L5 70 Z" fill="{color}"/>
        <circle cx="65" cy="48" r="32"
        fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M40 25 L35 15 M55 17 L55 7
        M75 17 L80 7 M90 30 L100 20"
        stroke="white" stroke-width="3"/>
        <circle cx="55" cy="55" r="3" fill="#a67c32"/>
        <circle cx="75" cy="60" r="3" fill="#a67c32"/>
        """
# 별도 그림이 없는 생물의 기본 물고기 모양을 생성
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
# 네온테트라의 특징적인 줄무늬를 추가
        # 네온테트라
        if name == "네온테트라":
            shape += """
            <path d="M35 43 Q55 35 80 43"
            stroke="#ff4d9d" stroke-width="3" fill="none"/>
            <path d="M35 48 Q55 43 80 48"
            stroke="#35ffff" stroke-width="4" fill="none"/>
            """
# 크라운피쉬의 흰색 줄무늬를 추가
        # 크라운피쉬
        elif name == "크라운피쉬":
            shape += """
            <path d="M42 25 L48 68 M65 24 L72 68"
            stroke="white" stroke-width="6"/>
            """

        # 퀸엔젤
        elif name == "퀸엔젤":
            shape += """
            <path d="M35 35 L85 35 M35 45 L85 45
            M35 55 L85 55"
            stroke="#2565a8" stroke-width="3"/>
            """

        # 베타
        elif name == "베타":
            shape += """
            <path d="M45 30 Q60 0 90 12 Q80 30 85 35"
            fill="#a83d8d"/>
            <path d="M45 65 Q65 90 95 80 Q80 65 85 60"
            fill="#a83d8d"/>
            """

        # 구피
        elif name == "구피":
            shape += """
            <path d="M28 48 Q0 5 10 48 Q0 90 28 48"
            fill="#f5a5dc" stroke="white" stroke-width="1"/>
            """

        # 디스커스
        elif name == "디스커스":
            shape += """
            <circle cx="55" cy="42" r="5" fill="#f6b94a"/>
            <circle cx="70" cy="55" r="5" fill="#f6b94a"/>
            <circle cx="45" cy="55" r="4" fill="#f6b94a"/>
            """

        # 엔젤피쉬
        elif name == "엔젤피쉬":
            shape += """
            <path d="M50 25 L65 0 L75 25
            M50 65 L65 90 L75 65"
            fill="none" stroke="white" stroke-width="2"/>
            """

        # 블루탱
        elif name == "블루탱":
            shape += """
            <path d="M65 25 L75 10 L85 30"
            fill="#153c9c"/>
            """

        # 옐로우탱
        elif name == "옐로우탱":
            shape += """
            <path d="M35 30 L45 65"
            stroke="#fff6a0" stroke-width="3"/>
            """
# 생물 종류에 따라 눈의 위치를 설정
    # 눈 위치 설정
    if name in ["반수생거북", "바다거북"]:
        eye = '<circle cx="108" cy="42" r="3" fill="white"/>'
    elif name == "해마":
        eye = '<circle cx="78" cy="27" r="3" fill="white"/>'
    elif name == "애플스네일":
        eye = ""
    else:
        eye = """
        <circle cx="87" cy="42" r="3.5" fill="white"/>
        <circle cx="88" cy="42" r="1.8" fill="#172033"/>
        """
# 완성된 SVG 그림을 문자열로 반환
    return f"""
    <svg width="130" height="90" viewBox="0 0 120 90"
    xmlns="http://www.w3.org/2000/svg">
        {shape}
        {eye}
    </svg>
    """

# 사용자가 원하는 진단 항목을 선택하도록 설정
# ==================================================
# 5. 사이드바 설정
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

# 어항에 넣을 생물 종류를 선택
# ==================================================
# 6. 생물 선택
# ==================================================
selected_fishes = st.sidebar.multiselect(
    "어항에 넣을 생물 종류를 선택하세요:",
    list(FISH_DATABASE.keys()),
    default=["엔젤피쉬", "네온테트라"]
)

# 어항에 들어가는 전체 생물 개체 수를 입력
# ==================================================
# 7. 환경 입력
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
# 8. 환경별 테마 판별
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
# 9. 배경 테마 데이터
# ==================================================
BACKGROUND_STYLES = {
    "기본": {
        "bg_color": "#b2ebf2",
        "border_color": "#00bcd4",
        "title": "🫧 기본 수조"
    },
    "담수어": {
        "bg_color": "#c8e6c9",
        "border_color": "#4caf50",
        "title": "🌿 수초 담수 생태계"
    },
    "해수어": {
        "bg_color": "#0284c7",
        "border_color": "#0369a1",
        "title": "🌊 푸른 바다 생태계"
    },
    "열대어": {
        "bg_color": "#e1bee7",
        "border_color": "#ab47bc",
        "title": "🪸 화려한 열대 생태계"
    }
}

style = BACKGROUND_STYLES[current_env]


# ==================================================
# 10. 메인 화면
# ==================================================
st.title("🐠 AquaCare Pro - 고민 맞춤형 수산/어항 진단 플랫폼")

st.caption(f"현재 테마: **{style['title']}**")

st.markdown("---")


# ==================================================
# 11. 어항 그림 출력
# ==================================================
if selected_fishes:

    tank_html = ""

    # 선택한 생물을 개체 수만큼 배치
    for idx in range(int(count)):

        fish_name = selected_fishes[idx % len(selected_fishes)]

        tank_html += f"""
        <div class="fish-item">
            {draw_fish(fish_name)}
            <div class="fish-name">
                {FISH_DATABASE[fish_name]['emoji']} {fish_name}
            </div>
        </div>
        """

    # 별도의 HTML 화면에서 SVG 렌더링
    aquarium_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
            background: transparent;
        }}

        .fish-tank {{
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(140px, 1fr));
            gap: 18px;
            padding: 25px;
            min-height: 350px;
            align-items: center;
            justify-items: center;
            background: {style['bg_color']};
            border: 4px solid {style['border_color']};
            border-radius: 20px;
            overflow: hidden;
        }}

        .fish-item {{
            width: 140px;
            height: 125px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 15px;
            animation: swim 3s ease-in-out infinite;
        }}

        .fish-item:nth-child(even) {{
            animation-delay: 0.8s;
        }}

        .fish-item svg {{
            width: 130px;
            height: 90px;
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
    </head>

    <body>

        <div class="fish-tank">
            {tank_html}
        </div>

    </body>
    </html>
    """

    # 중요: st.markdown이 아니라 components.html 사용!
    components.html(
        aquarium_html,
        height=450,
        scrolling=True
    )

    st.markdown("---")


    # ==================================================
    # 12. 진단 결과
    # ==================================================
    st.subheader(f"📊 진단 결과: {problem_type}")

    salinities = {
        FISH_DATABASE[fish]["salinity"]
        for fish in selected_fishes
    }

    # 담수와 해수 혼합 검사
    if len(salinities) > 1:
        st.error(
            "🚨 담수 생물과 해수 생물이 함께 선택되었습니다. "
            "서로 다른 염분 환경의 생물을 한 수조에서 함께 사육하지 마세요."
        )


    # ==================================================
    # 13. 사료량 계산
    # ==================================================
    if "적정 사료량" in problem_type:

        avg_weight = 10.0
        total_biomass_g = count * avg_weight

        if 20.0 <= current_temp <= 28.0:
            metabolic_factor = 1.0
            status_msg = "기준 수온 구간"

        elif current_temp < 20.0:
            metabolic_factor = max(
                0.2,
                1.0 - (20.0 - current_temp) * 0.08
            )
            status_msg = "저수온 주의"

        else:
            metabolic_factor = max(
                0.1,
                1.0 - (current_temp - 28.0) * 0.1
            )
            status_msg = "고수온 주의"

        daily_feed_g = (
            total_biomass_g * 0.03
        ) * metabolic_factor

        col1, col2 = st.columns(2)

        col1.metric(
            "🐟 일일 참고 사료량",
            f"{daily_feed_g:.2f} g"
        )

        col2.metric(
            "🌡️ 수온 상태",
            status_msg
        )

        st.info(
            "💡 실제 급여량은 어종, 체중, 성장 단계에 따라 다릅니다. "
            "소량씩 급여하고 남은 사료를 제거해 주세요."
        )


    # ==================================================
    # 14. 합사 가능 여부
    # ==================================================
    elif "합사 가능" in problem_type:

        temperaments = [
            FISH_DATABASE[fish]["temperament"]
            for fish in selected_fishes
        ]

        if len(salinities) > 1:

            st.error("🚨 담수 생물과 해수 생물의 혼합은 불가능합니다.")

        elif "베타" in selected_fishes and len(selected_fishes) > 1:

            st.error(
                "⚠️ 베타는 영역성이 강할 수 있어 "
                "다른 어종과의 합사에 주의해야 합니다."
            )

        elif "공격적" in temperaments:

            st.warning(
                "⚠️ 공격성이 있는 생물이 포함되어 있습니다."
            )

        else:

            st.success(
                "✅ 선택한 생물의 성격은 전반적으로 "
                "온순하거나 보통 수준입니다."
            )

        st.info(
            "💡 실제 합사 여부는 성체 크기, 영역성, "
            "수조 크기 등을 함께 확인해야 합니다."
        )


    # ==================================================
    # 15. 수조 과밀 여부
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
            "💡 이 값은 교육용 단순 계산이며 실제 적정 수조 용량을 "
            "나타내지는 않습니다."
        )

        if density_ratio > 100:
            st.warning(
                "⚠️ 수조 공간과 여과력을 다시 확인해 주세요."
            )
        else:
            st.success(
                "✅ 단순 참고 비율이 100% 이하입니다. "
                "실제 사육 환경도 확인해 주세요."
            )


    # ==================================================
    # 16. 수질 및 환경 관리
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
                f"- **{fish}**: {min_t}~{max_t}°C "
                f"(현재 수온: **{status}**)"
            )

        st.info(
            "💡 수온 외에도 pH, 암모니아, 아질산염, "
            "질산염과 용존산소를 확인해 주세요."
        )


    # ==================================================
    # 17. 질병 예찰
    # ==================================================
    elif "질병 예찰" in problem_type:

        st.info("🩺 **어종별 질병 및 환경 주의 안내**")

        if current_temp < 18.0:

            st.warning(
                "⚠️ 저수온 상태입니다. "
                "선택한 어종의 적정 수온을 확인해 주세요."
            )

        elif current_temp > 29.0:

            st.warning(
                "⚠️ 고수온 상태입니다. "
                "용존산소 감소와 수질 악화에 주의하세요."
            )

        else:

            st.success(
                "✅ 일반적인 참고 수온 구간입니다. "
                "어종별 적정 수온도 확인해 주세요."
            )

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
            "💡 질병이 의심되면 수질과 행동 변화를 확인하고 "
            "수산생물 전문가의 진단을 받아 주세요."
        )


# ==================================================
# 18. 생물 미선택 안내
# ==================================================
else:

    st.info(
        "👈 좌측 사이드바에서 생물을 하나 이상 선택해 주세요!"
    )
