"""
pages/3_settings.py — 단원 설정
보호자/아이가 학교에서 배운 단원을 체크해 잠금을 해제합니다.
is_unlocked = True 인 단원만 모험 화면에서 출제됩니다.
"""

from pathlib import Path

import streamlit as st

from core.state import init_session_state

# ── 페이지 설정 ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="⚙️ 단원 설정 | 냥이의 수학 모험",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

init_session_state()

if not st.session_state.onboarded:
    st.switch_page("streamlit_app.py")

# ── 헤더 ─────────────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='text-align:center;color:#C8B2E8;'>⚙️ 단원 설정</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="speech-bubble">'
    "학교에서 배운 단원에 체크해줘냥! ✅<br>"
    "체크한 단원만 모험에서 문제로 나온다냥~ 🐾"
    "</div>",
    unsafe_allow_html=True,
)

st.write("")

# ── 단원 목록 ────────────────────────────────────────────────────────────────

learning_status: list[dict] = st.session_state.learning_status

# 학기별로 분리
semesters = ["1학기", "2학기"]

changed = False

for semester in semesters:
    topics_in_semester = [t for t in learning_status if t["semester"] == semester]

    with st.expander(f"📅 {semester}", expanded=True):
        for topic in topics_in_semester:
            col_check, col_info = st.columns([1, 5])

            with col_check:
                new_val = st.checkbox(
                    label="",
                    value=topic["is_unlocked"],
                    key=f"unlock_{topic['topic_id']}",
                )
            with col_info:
                mastery = topic["mastery_score"]
                if mastery >= 80:
                    mastery_label = f'<span class="badge-high">🟢 {mastery}점</span>'
                elif mastery >= 50:
                    mastery_label = f'<span class="badge-mid">🟡 {mastery}점</span>'
                else:
                    mastery_label = f'<span class="badge-low">🔴 {mastery}점</span>'

                lock_icon = "✅" if topic["is_unlocked"] else "🔒"
                st.markdown(
                    f'<div class="topic-row">'
                    f"{lock_icon} <b>{topic['unit']}단원</b> {topic['label']} &nbsp; {mastery_label}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            if new_val != topic["is_unlocked"]:
                topic["is_unlocked"] = new_val
                changed = True

if changed:
    unlocked_count = sum(1 for t in learning_status if t["is_unlocked"])
    st.success(f"✅ 저장됐어냥! 현재 {unlocked_count}개 단원이 활성화 중이야냥~ 🐾")

st.write("")

# ── 하단 버튼 ────────────────────────────────────────────────────────────────

col_home, col_adv = st.columns(2)
with col_home:
    if st.button("🏠 마이룸으로", use_container_width=True):
        st.switch_page("streamlit_app.py")
with col_adv:
    if st.button("⚔️ 모험 떠나기!", use_container_width=True):
        st.switch_page("pages/1_adventure.py")
