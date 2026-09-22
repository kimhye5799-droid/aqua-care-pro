import streamlit as st

st.set_page_config(page_title="나만의 어항 꾸미기", page_icon="🎨", layout="wide")

st.title("🎨 나만의 가상 어항 커스터마이징")
st.caption("바닥재, 수초, 장식품을 자유롭게 조합하여 나만의 꿈의 어항을 꾸며보세요!")

st.markdown("---")

# 어항 꾸미기 옵션 선택
col_opt1, col_opt2, col_opt3 = st.columns(3)

with col_opt1:
    bg_style = st.selectbox("1. 어항 분위기 선택", ["푸른 바다 🌊", "신비로운 에메랄드 🌿", "석양빛 산호초 🪸", "심해 🌌"])
    gravel = st.selectbox("2. 바닥재 선택", ["금사 (황금빛 모래) 🏖️", "흑사 (검은 모래) 🖤", "수초 전용 소일 🤎", "알록달록 컬러 스톤 🌈"])

with col_opt2:
    plants = st.multiselect("3. 수초 및 구조물", ["수초 🌿", "유목 🪵", "기암괴석 🪨", "해조류 🪸"], default=["수초 🌿", "유목 🪵"])
    decorations = st.multiselect("4. 어항 장식품", ["보물상자 🏴‍☠️", "조개껍데기 🐚", "잠수함 🚢", "침몰선 ⚓"], default=["조개껍데기 🐚"])

with col_opt3:
    main_fish = st.radio("5. 어항의 주인공 물고기", ["알록달록 열대어 🐠", "귀여운 금붕어 🐟", "화려한 엔젤피쉬 🐡", "카리스마 베타 🥊"])

# 디자인 스타일에 따른 CSS 설정
BG_MAP = {
    "푸른 바다 🌊": "linear-gradient(180deg, #b3e5fc 0%, #0288d1 100%)",
    "신비로운 에메랄드 🌿": "linear-gradient(180deg, #e8f5e9 0%, #2e7d32 100%)",
    "석양빛 산호초 🪸": "linear-gradient(180deg, #fce4ec 0%, #c2185b 100%)",
    "심해 🌌": "linear-gradient(180deg, #1a237e 0%, #000000 100%)"
}

GRAVEL_MAP = {
    "금사 (황금빛 모래) 🏖️": "🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾🌾",
    "흑사 (검은 모래) 🖤": "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛",
    "수초 전용 소일 🤎": "🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫",
    "알록달록 컬러 스톤 🌈": "🔴🟠🟡🟢🔵🟣🔴🟠🟡🟢🔵🟣🔴🟠🟡"
}

st.markdown("---")
st.subheader("🖼️ 내가 직접 완성한 나만의 어항")

# 장식품 및 물고기 배치를 이모지로 연출
plant_str = " ".join([p.split()[-1] for p in plants])
decor_str = " ".join([d.split()[-1] for d in decorations])
fish_emoji = main_fish.split()[-1]

st.markdown(
    f"""
    <div style="
        background: {BG_MAP[bg_style]};
        border: 5px solid #37474f;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    ">
        <div style="font-size: 50px; margin-bottom: 30px;">
            <span style="display:inline-block; animation: floatEven 3s infinite;">{fish_emoji}</span>
            &nbsp;&nbsp;&nbsp;
            <span style="display:inline-block; animation: floatOdd 3.5s infinite;">{fish_emoji}</span>
        </div>
        <div style="font-size: 35px; margin-bottom: 10px;">
            {decor_str}
        </div>
        <div style="font-size: 30px; margin-bottom: 5px;">
            {plant_str}
        </div>
        <div style="font-size: 20px;">
            {GRAVEL_MAP[gravel]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.balloons() # 완성 축하 풍선 효과!
