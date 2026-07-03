"""
pages/1_adventure.py — 동물 구조 모험 (학습 화면)
잠금 해제된 단원 중 가중치 알고리즘으로 단원을 선택하고
스토리텔링 문제를 출제합니다.
"""

from pathlib import Path

import streamlit as st

from core.state import (
    ANIMAL_POOL,
    RARITY_WEIGHTS,
    apply_exp,
    get_cat_emoji,
    get_sample_question,
    get_unlocked_topics,
    init_session_state,
    pick_topic,
)

# ── 페이지 설정 ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="⚔️ 동물 구조 모험 | 냥이의 수학 모험",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

init_session_state()

# ── 온보딩 미완료 시 홈으로 ──────────────────────────────────────────────────

if not st.session_state.onboarded:
    st.switch_page("streamlit_app.py")

# ── 헤더 ─────────────────────────────────────────────────────────────────────

s = st.session_state
cat_emoji = get_cat_emoji(s.cat_level)

st.markdown(
    f"<h1 style='text-align:center;color:#C8B2E8;'>⚔️ 동물 구조 모험</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="speech-bubble">'
    f"도움을 기다리는 동물 친구를 구출해봐냥! {cat_emoji}"
    f"</div>",
    unsafe_allow_html=True,
)
st.write("")

# ════════════════════════════════════════════════════════════════════════════
# 잠금 해제된 단원 없음
# ════════════════════════════════════════════════════════════════════════════

unlocked = get_unlocked_topics()
if not unlocked:
    st.warning("아직 배운 단원이 없어냥! ⚙️ 단원 설정에서 배운 단원을 먼저 체크해봐냥~ 🐱")
    if st.button("⚙️ 단원 설정으로 가기", use_container_width=True):
        st.switch_page("pages/3_settings.py")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# 문제 출제
# ════════════════════════════════════════════════════════════════════════════

# 새 문제 뽑기 (또는 기존 문제 유지)
if st.session_state.current_question is None or st.button("🔀 다른 문제 풀기", use_container_width=False):
    topic = pick_topic()
    if topic:
        q = get_sample_question(topic["topic_id"])
        st.session_state.current_question = {"topic": topic, "question": q}
        st.session_state.answer_submitted = False
        st.session_state.last_correct = None

q_data = st.session_state.current_question
if q_data is None:
    st.info("문제를 불러오는 중이야냥... 잠깐만 기다려봐! 🐾")
    st.stop()

topic = q_data["topic"]
question = q_data["question"]

# ── 단원 배지 ────────────────────────────────────────────────────────────────

st.markdown(
    f"<div style='text-align:center;margin-bottom:0.5rem;'>"
    f"<span style='background:#C8B2E8;color:white;border-radius:12px;"
    f"padding:0.2rem 0.8rem;font-size:0.85rem;font-weight:700;'>"
    f"{topic['semester']} {topic['unit']}단원 · {topic['label']}</span>"
    f"</div>",
    unsafe_allow_html=True,
)

# ── 문제 박스 ────────────────────────────────────────────────────────────────

st.markdown(
    f'<div class="question-box">{question["q"]}</div>',
    unsafe_allow_html=True,
)

# ── 이미 제출된 경우 피드백만 표시 ──────────────────────────────────────────

if st.session_state.answer_submitted:
    if st.session_state.last_correct:
        st.markdown(
            '<div class="feedback-correct">🎉 정답이야냥! 최고야냥~ 🐾</div>',
            unsafe_allow_html=True,
        )
        st.balloons()
    else:
        hint_text = question.get("hint", "")
        st.markdown(
            f'<div class="feedback-wrong">'
            f"아쉽냥~ 틀렸어! 😿<br><br>"
            f"<b>힌트:</b> {hint_text}"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    col_next, col_home = st.columns(2)
    with col_next:
        if st.button("➡️ 다음 문제", use_container_width=True):
            st.session_state.current_question = None
            st.rerun()
    with col_home:
        if st.button("🏠 마이룸으로", use_container_width=True):
            st.switch_page("streamlit_app.py")
    st.stop()

# ── 정답 입력 ────────────────────────────────────────────────────────────────

q_type = question.get("type", "number")
correct_answer = question.get("answer")

if correct_answer is None:
    # 문제 준비 중
    st.info(question["q"])
    if st.button("🏠 마이룸으로", use_container_width=True):
        st.switch_page("streamlit_app.py")
    st.stop()

if q_type == "remainder":
    st.caption("몫과 나머지를 쉼표로 입력해봐냥! 예) 7, 1")
    user_input = st.text_input("✏️ 내 답:", placeholder="예) 7, 1", key="ans_input")
else:
    user_input = st.text_input("✏️ 내 답:", placeholder="숫자를 입력해봐냥!", key="ans_input")

if st.button("✅ 정답 확인!", use_container_width=True, disabled=not user_input.strip()):
    is_correct = False
    try:
        if q_type == "remainder":
            # "몫...나머지" 형태 비교
            quotient, remainder = map(int, user_input.replace(" ", "").split(","))
            expected_q, expected_r = map(int, str(correct_answer).split("..."))
            is_correct = (quotient == expected_q and remainder == expected_r)
        else:
            is_correct = int(user_input.strip()) == int(correct_answer)
    except (ValueError, AttributeError):
        is_correct = False

    # 학습 상태 갱신
    topic_state = next(
        (t for t in s.learning_status if t["topic_id"] == topic["topic_id"]), None
    )
    if topic_state:
        topic_state["total_solved"] += 1
        if is_correct:
            topic_state["correct_count"] += 1
            topic_state["mastery_score"] = min(100, topic_state["mastery_score"] + 5)
        else:
            topic_state["mastery_score"] = max(0, topic_state["mastery_score"] - 3)

    # 정답 시 보상
    if is_correct:
        apply_exp(10)
        s.gold += 1

        # 랜덤 동물 구출
        import random
        emoji, name, category, rarity = random.choices(ANIMAL_POOL, weights=RARITY_WEIGHTS, k=1)[0]
        s.rescued_count += 1
        from datetime import datetime
        s.rescue_logs.append({
            "rescue_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "animal_name": f"{emoji} {name}",
            "rarity": rarity,
        })

    st.session_state.answer_submitted = True
    st.session_state.last_correct = is_correct
    st.rerun()
