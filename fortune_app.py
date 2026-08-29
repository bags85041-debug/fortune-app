import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)

def ask_ai(prompt):
    """AI에게 질문하고 응답 반환"""
    res = client.messages.create(
        model="claude-haiku",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text

# 12개 별자리
ZODIAC_SIGNS = [
    "양자리 ♈", "황소자리 ♉", "쌍둥이자리 ♊", "게자리 ♋",
    "사자자리 ♌", "처녀자리 ♍", "천칭자리 ♎", "전갈자리 ♏",
    "궁수자리 ♐", "염소자리 ♑", "물병자리 ♒", "물고기자리 ♓"
]

st.set_page_config(page_title="나의 운세 & 별자리 앱", layout="centered")

st.markdown("<h1 style='text-align: center;'>🌟 나의 운세 & 별자리 앱 🌟</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 이름", placeholder="예: 김철수")

with col2:
    birth = st.text_input("📅 생년월일", placeholder="예: 1995-05-15", help="YYYY-MM-DD 형식")

zodiac = st.selectbox("⭐ 별자리 선택", ZODIAC_SIGNS)

if st.button("🔮 운세 보기", use_container_width=True):
    # 입력값 검증
    if not name:
        st.warning("이름을 입력해주세요!")
    elif not birth:
        st.warning("생년월일을 입력해주세요! (YYYY-MM-DD)")
    else:
        # 생년월일 형식 검증
        try:
            datetime.strptime(birth, "%Y-%m-%d")
        except ValueError:
            st.error("생년월일 형식이 올바르지 않습니다. (예: 1995-05-15)")
        else:
            # AI 호출
            with st.spinner("⏳ 운세를 읽고 있습니다..."):
                prompt = f"""사용자의 정보:
- 이름: {name}
- 생년월일: {birth}
- 별자리: {zodiac}

위 정보를 바탕으로 오늘의 운세를 4~5줄로 작성해줘.
- 밝고 친근한 말투로 작성
- 사용자가 재미있게 읽을 수 있도록 긍정적이고 격려하는 내용
- 일상 생활에서 도움이 될 만한 조언 포함
- 별자리의 특징을 반영하되, 너무 무겁지 않게"""

                try:
                    fortune_text = ask_ai(prompt)
                    st.success("✨ 운세가 나왔습니다!")
                    st.markdown(f"<div style='background-color: #FFF8F0; padding: 20px; border-radius: 10px; margin-top: 20px;'>{fortune_text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
