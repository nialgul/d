import streamlit as st
import requests
import os
from datetime import datetime

# -------------------
# 기본 설정
# -------------------
st.set_page_config(page_title="디스코드 관리 패널", page_icon="🛠️")
st.title("🛠️ 디스코드 관리 패널")

# -------------------
# 토큰 자동 불러오기
# -------------------
bot_token = ""

# Streamlit Secrets
if "DISCORD_TOKEN" in st.secrets:
    bot_token = st.secrets["DISCORD_TOKEN"]
# 로컬 환경변수
else:
    bot_token = os.getenv("DISCORD_TOKEN", "")

# -------------------
# 사이드바
# -------------------
st.sidebar.header("설정")

guild_id = st.sidebar.text_input("서버 ID")

if bot_token:
    st.sidebar.success("토큰 연결됨 ✅")
else:
    st.sidebar.error("토큰 없음 ❌ (Secrets 설정 필요)")

# -------------------
# 헤더
# -------------------
def headers():
    return {"Authorization": f"Bot {bot_token}"}

# -------------------
# 탭
# -------------------
tab1, tab2, tab3 = st.tabs(["📊 서버 정보", "📁 채널 목록", "📜 로그"])

# -------------------
# 서버 정보
# -------------------
with tab1:
    st.subheader("서버 정보")

    if st.button("불러오기"):
        if not bot_token or not guild_id:
            st.error("토큰 + 서버ID 필요")
        else:
            res = requests.get(
                f"https://discord.com/api/v10/guilds/{guild_id}",
                headers=headers()
            )

            if res.status_code == 200:
                data = res.json()
                st.success("성공")
                st.write(f"📛 이름: {data.get('name')}")
                st.write(f"🆔 ID: {data.get('id')}")
                st.write(f"👑 Owner: {data.get('owner_id')}")
                st.json(data)
            else:
                st.error(f"오류: {res.status_code}")

# -------------------
# 채널 목록
# -------------------
with tab2:
    st.subheader("채널 목록")

    if st.button("채널 불러오기"):
        if not bot_token or not guild_id:
            st.error("토큰 + 서버ID 필요")
        else:
            res = requests.get(
                f"https://discord.com/api/v10/guilds/{guild_id}/channels",
                headers=headers()
            )

            if res.status_code == 200:
                channels = res.json()
                st.success(f"{len(channels)}개 채널")

                for ch in channels:
                    st.write(f"📁 {ch.get('name')} ({ch.get('id')})")
            else:
                st.error(f"오류: {res.status_code}")

# -------------------
# 로그 보기
# -------------------
with tab3:
    st.subheader("로그 보기")

    file = st.file_uploader("로그 파일 업로드 (.txt/.json)")

    if file:
        content = file.read().decode("utf-8", errors="ignore")
        lines = content.splitlines()

        st.success(f"{len(lines)}줄 로그")

        for line in lines[::-1][:100]:
            st.code(line)

# -------------------
# 하단
# -------------------
st.markdown("---")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
