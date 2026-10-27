import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="픽셀 파우더 어항 & 어항선배 가이드",
    page_icon="🐠",
    layout="wide"
)

# 탭 메뉴 구성 (샌드박스 어항 / 어항선배 Q&A)
main_tab1, main_tab2 = st.tabs(["🎮 픽셀 파우더 어항 샌드박스", "💬 초보 물집사를 위한 어항선배 Q&A"])

with main_tab1:
    st.subheader("🐠 레트로 픽셀 파우더 어항 게임")
    st.caption("모래, 자갈, 수초를 심고 물고기와 거북이를 키워보세요!")

    # 어항 HTML/JS 샌드박스 게임 컴포넌트
    html_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>픽셀 파우더 어항 Sandbox</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
          font-family: 'Pretendard', sans-serif;
          background-color: #060913;
          color: #f1f5f9;
          display: flex;
          height: 75vh;
          overflow: hidden;
          border-radius: 12px;
        }
        .tank-area {
          flex: 1;
          position: relative;
          background: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 10px;
        }
        .glass-tank {
          position: relative;
          width: 100%;
          height: 100%;
          border-radius: 12px;
          box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.25);
          border: 3px solid #38bdf8;
          background-color: #020617;
          overflow: hidden;
        }
        canvas { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
        .controls-bar {
          position: absolute;
          bottom: 10px;
          left: 50%;
          transform: translateX(-50%);
          background: rgba(15, 23, 42, 0.85);
          padding: 6px 14px;
          border-radius: 20px;
          font-size: 11px;
          color: #cbd5e1;
          border: 1px solid rgba(255,255,255,0.2);
        }
      </style>
    </head>
    <body>
      <div class="tank-area">
        <div class="glass-tank">
          <canvas id="aquariumCanvas"></canvas>
          <div class="controls-bar">마우스로 모래를 쌓고 물고기를 관찰하세요!</div>
        </div>
      </div>

      <script>
        const canvas = document.getElementById('aquariumCanvas');
        const ctx = canvas.getContext('2d');

        function resize() {
          canvas.width = canvas.parentElement.clientWidth;
          canvas.height = canvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // 간단한 루프 애니메이션 테스트
        function animate() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.fillStyle = '#38bdf8';
          ctx.font = '14px sans-serif';
          ctx.fillText("✨ 픽셀 어항 엔진 구동 중... 하단 도구를 활용해 보세요!", 20, 30);
          requestAnimationFrame(animate);
        }
        animate();
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=False)

with main_tab2:
    st.subheader("💬 어항선배에게 물어보기")
    st.markdown("초보 물집사들이 가장 많이 하는 질문과 맞춤형 가이드를 확인해보세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🐠 **물잡이란 무엇인가요?**\n생물을 넣기 전 여과 박테리아가 살 수 있는 환경을 1~2주간 미리 만드는 과정입니다.")
        st.success("🌿 **초보자 추천 물고기**\n- 네온테트라\n- 구피\n- 체리새우")
    with col2:
        st.warning("⚠️ **주의할 점 (합사 금지)**\n- 투견 물고기(베타 등)는 단독 사육이 원칙입니다.\n- 여과기 없이 어항을 운영하면 수질이 급격히 나빠집니다.")

    user_query = st.text_input("어항선배에게 궁금한 점을 물어보세요! (예: 물고기가 자꾸 가라앉아요)")
    if st.button("선배에게 질문하기"):
        if user_query:
            st.success(f"🎓 **어항선배의 답변:** '{user_query}'에 대한 답변이네요! 수온을 24~26도로 맞추고 여과기 상태를 확인해 보세요!")
        else:
            st.warning("질문 내용을 입력해주세요!")
