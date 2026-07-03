"""
pages/2_dex.py — 동물 도감
구출한 동물들의 기록을 보여줍니다.
"""

from pathlib import Path

import streamlit as st

from core.state import init_session_state

# ── 페이지 설정 ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="📖 동물 도감 | 냥이의 수학 모험",
    page_icon="📖",
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

s = st.session_state

st.markdown(
    "<h1 style='text-align:center;color:#C8B2E8;'>📖 동물 도감</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="speech-bubble">'
    f"지금까지 <b>{s.rescued_count}마리</b>의 동물을 구출했어냥! 🐾<br>"
    "희귀한 동물일수록 더 열심히 공부해야 나온다냥~ 🌟"
    "</div>",
    unsafe_allow_html=True,
)

st.write("")

# ── 통계 ─────────────────────────────────────────────────────────────────────

logs = s.rescue_logs

if not logs:
    st.info("아직 구출한 동물이 없어냥! ⚔️ 모험을 떠나서 동물 친구를 구출해봐냥~ 🐱")
    if st.button("⚔️ 모험 떠나기!", use_container_width=True):
        st.switch_page("pages/1_adventure.py")
    st.stop()

# 희귀도별 카운트
from collections import Counter

rarity_count = Counter(log["rarity"] for log in logs)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🐾 전체", s.rescued_count)
col2.metric("⬜ 일반", rarity_count.get("일반", 0))
col3.metric("🔵 희귀", rarity_count.get("희귀", 0))
col4.metric("⭐ 전설", rarity_count.get("전설", 0))

st.divider()

# ── 구출 기록 테이블 ─────────────────────────────────────────────────────────

RARITY_CLASS = {"일반": "rarity-normal", "희귀": "rarity-rare", "전설": "rarity-legendary"}
RARITY_BADGE = {"일반": "⬜", "희귀": "🔵", "전설": "⭐"}

st.subheader("구출 기록")

# 최신 순으로 표시
for log in reversed(logs):
    rarity = log["rarity"]
    badge = RARITY_BADGE.get(rarity, "")
    css_cls = RARITY_CLASS.get(rarity, "")

    st.markdown(
        f'<div class="topic-row" style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:1.1rem;">{log["animal_name"]}</span>'
        f'<span class="{css_cls}">{badge} {rarity} &nbsp;|&nbsp; {log["category"]}</span>'
        f'<span style="color:#aaa;font-size:0.85rem;">{log["rescue_time"]}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

st.write("")
if st.button("🏠 마이룸으로", use_container_width=False):
    st.switch_page("streamlit_app.py")
