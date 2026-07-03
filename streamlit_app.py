"""
streamlit_app.py — 냥이의 수학 모험
진입점: 온보딩(고양이 이름 짓기) → 홈/마이룸 화면
"""

from pathlib import Path

import streamlit as st

from core.state import (
    apply_exp,
    get_cat_emoji,
    get_exp_to_next_level,
    init_session_state,
)

# ── 페이지 설정 ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="🐾 냥이의 수학 모험",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS 주입 ─────────────────────────────────────────────────────────────────

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# ── 세션 상태 초기화 ─────────────────────────────────────────────────────────

init_session_state()

# ════════════════════════════════════════════════════════════════════════════
# 온보딩 화면 — 고양이 이름을 짓지 않은 경우
# ════════════════════════════════════════════════════════════════════════════

if not st.session_state.onboarded:
    st.markdown(
        """
        <div class="onboard-wrapper">
            <div style="font-size:5rem;">🐾</div>
            <div class="onboard-title">냥이 마법사와<br>동물 구조단</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="speech-bubble" style="max-width:480px;margin:0 auto 1.5rem;">'
        "안녕! 나는 마법사 고양이야 🐱<br>"
        "우리 함께 수학으로 동물 친구들을 구출하러 가자냥!"
        "</div>",
        unsafe_allow_html=True,
    )

    with st.container():
        col = st.columns([1, 2, 1])[1]
        with col:
            cat_name = st.text_input(
                "✏️ 내 고양이 이름을 지어줘!",
                placeholder="예) 냥냥이, 초코, 솜사탕",
                max_chars=10,
            )
            if st.button(
                "✨ 모험 시작!",
                use_container_width=True,
                disabled=not cat_name.strip(),
            ):
                st.session_state.cat_name = cat_name.strip()
                st.session_state.onboarded = True
                st.rerun()

    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# 홈 / 마이룸 화면
# ════════════════════════════════════════════════════════════════════════════

s = st.session_state
cat_emoji = get_cat_emoji(s.cat_level)
exp_needed = get_exp_to_next_level(s.cat_level)
exp_pct = min(s.exp / exp_needed, 1.0)

# ── 타이틀 ──────────────────────────────────────────────────────────────────

st.markdown(
    f"<h1 style='text-align:center;color:#C8B2E8;margin-bottom:0.2rem;'>"
    f"{cat_emoji} {s.cat_name}의 마이룸"
    f"</h1>",
    unsafe_allow_html=True,
)

# ── 고양이 상태 카드 ─────────────────────────────────────────────────────────

with st.container(border=True):
    col_icon, col_info = st.columns([1, 3])
    with col_icon:
        st.markdown(f'<div class="cat-avatar">{cat_emoji}</div>', unsafe_allow_html=True)
    with col_info:
        st.markdown(f"### Lv.{s.cat_level} &nbsp; {s.cat_name}")
        st.progress(exp_pct, text=f"✨ EXP {s.exp} / {exp_needed}")
        c1, c2 = st.columns(2)
        c1.metric("🪙 츄르코인", s.gold)
        c2.metric("🐾 구출한 동물", f"{s.rescued_count}마리")

st.write("")

# ── 말풍선 ───────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="speech-bubble">'
    "야옹~ 오늘 어떤 동물을 구하러 갈까냥? 🐾"
    "</div>",
    unsafe_allow_html=True,
)

st.write("")

# ── 네비게이션 버튼 ──────────────────────────────────────────────────────────

col_adv, col_dex = st.columns(2)
with col_adv:
    if st.button("⚔️ 오늘의 도전!", use_container_width=True):
        st.switch_page("pages/1_adventure.py")
with col_dex:
    if st.button("📖 동물 도감", use_container_width=True):
        st.switch_page("pages/2_dex.py")

_, col_mid, _ = st.columns([1, 2, 1])
with col_mid:
    if st.button("⚙️ 단원 설정", use_container_width=True):
        st.switch_page("pages/3_settings.py")
