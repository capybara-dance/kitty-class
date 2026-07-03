"""
core/state.py
세션 상태 초기화, 커리큘럼 데이터, 고양이 유틸리티를 담당합니다.
DB 연동 전 단계 — 모든 데이터를 st.session_state 에 인메모리로 보관합니다.
"""

import streamlit as st

# ── 커리큘럼 정의 ────────────────────────────────────────────────────────────

CURRICULUM = [
    # (topic_id, 표시 이름, 학기, 단원 번호)
    ("덧셈과_뺄셈",   "덧셈과 뺄셈",      "1학기", 1),
    ("평면도형",      "평면도형",         "1학기", 2),
    ("나눗셈_기초",   "나눗셈 기초",      "1학기", 3),
    ("곱셈",          "곱셈",             "1학기", 4),
    ("길이와_시간",   "길이와 시간",      "1학기", 5),
    ("분수와_소수",   "분수와 소수 ★",   "1학기", 6),
    ("곱셈_심화",     "곱셈 심화",        "2학기", 1),
    ("나눗셈_심화",   "나눗셈 심화 ★",   "2학기", 2),
    ("원",            "원",               "2학기", 3),
    ("분수_심화",     "분수 심화 ★",     "2학기", 4),
    ("들이와_무게",   "들이와 무게",      "2학기", 5),
    ("자료의_정리",   "자료의 정리",      "2학기", 6),
]

# ── 샘플 문제 (골격용 — 추후 core/curriculum.py 로 분리) ────────────────────

SAMPLE_QUESTIONS: dict[str, list[dict]] = {
    "덧셈과_뺄셈": [
        {"q": "꿀벌 253마리가 꽃밭에 있었는데, 178마리가 더 날아왔어냥!\n모두 몇 마리일까냥? 🐝", "answer": 431, "hint": "받아올림에 주의해봐냥! 일의 자리부터 차례로 더해봐 🐾"},
        {"q": "연어가 532개 있었는데 고양이들이 247개를 먹었어냥!\n남은 연어는 몇 개일까냥? 🐟", "answer": 285, "hint": "받아내림이 필요해냥! 일의 자리부터 빼봐 🐾"},
    ],
    "나눗셈_기초": [
        {"q": "꿀단지 24개를 곰 4마리에게 똑같이 나누어 주려고 해냥!\n한 마리가 몇 개씩 가질 수 있을까냥? 🐻", "answer": 6, "hint": "4 × ? = 24 를 생각해봐냥! 🐾"},
        {"q": "당근 36개를 토끼 9마리에게 똑같이 나누어 줄 거야냥!\n토끼 한 마리가 받는 당근은 몇 개일까냥? 🐰", "answer": 4, "hint": "9 × ? = 36 을 생각해봐냥! 🐾"},
    ],
    "곱셈": [
        {"q": "아기 고양이 한 마리가 하루에 연어를 23개씩 먹는대냥!\n고양이 4마리가 하루 동안 먹는 연어는 모두 몇 개일까냥? 🐱", "answer": 92, "hint": "23 × 4 를 일의 자리, 십의 자리 순서로 계산해봐냥! 🐾"},
    ],
    "곱셈_심화": [
        {"q": "도토리 125개가 들어있는 바구니가 3개 있어냥!\n도토리는 모두 몇 개일까냥? 🌰", "answer": 375, "hint": "125 × 3 을 자리 수에 맞춰 차근차근 계산해봐냥! 🐾"},
    ],
    "나눗셈_심화": [
        {"q": "딸기 29개를 고슴도치 4마리에게 나누어 줬어냥!\n한 마리가 몇 개씩 받고, 몇 개가 남을까냥? 🦔", "answer": "7...1", "hint": "4 × 7 = 28 이니까 나머지는 29 - 28 = ? 냥! 🐾", "type": "remainder"},
    ],
}

# 문제가 없는 단원은 기본 안내 메시지 반환
DEFAULT_QUESTION = {
    "q": "이 단원의 문제는 준비 중이야냥! 🔨\n다른 단원을 선택해봐냥~ 🐾",
    "answer": None,
    "hint": "",
}

# ── 동물 도감 데이터 ─────────────────────────────────────────────────────────

ANIMAL_POOL = [
    ("🐶", "강아지",  "포유류", "일반"),
    ("🐰", "토끼",    "포유류", "일반"),
    ("🐦", "참새",    "조류",   "일반"),
    ("🐸", "개구리",  "양서류", "일반"),
    ("🦋", "나비",    "곤충",   "희귀"),
    ("🦊", "여우",    "포유류", "희귀"),
    ("🦜", "앵무새",  "조류",   "희귀"),
    ("🦄", "유니콘",  "전설",   "전설"),
    ("🐉", "용",      "전설",   "전설"),
    ("✨", "별빛 고양이", "전설", "전설"),
]

RARITY_WEIGHTS = [30, 30, 20, 20, 10, 10, 10, 2, 2, 1]  # 합계 비례 가중치

# ── 세션 상태 초기화 ─────────────────────────────────────────────────────────

def init_session_state() -> None:
    """앱 실행 시 최초 1회 session_state 기본값을 설정합니다."""
    defaults: dict = {
        "onboarded": False,
        "cat_name": "",
        "cat_level": 1,
        "exp": 0,
        "gold": 0,
        "rescued_count": 0,
        "learning_status": _make_learning_status(),
        "rescue_logs": [],
        # 학습 화면 내부 상태
        "current_question": None,
        "answer_submitted": False,
        "last_correct": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _make_learning_status() -> list[dict]:
    return [
        {
            "topic_id": tid,
            "label": label,
            "semester": semester,
            "unit": unit,
            "total_solved": 0,
            "correct_count": 0,
            "mastery_score": 50,
            "is_unlocked": False,
        }
        for tid, label, semester, unit in CURRICULUM
    ]


# ── 고양이 유틸리티 ──────────────────────────────────────────────────────────

def get_cat_emoji(level: int) -> str:
    if level >= 10:
        return "🦄"
    if level >= 5:
        return "🐱"
    return "🐾"


def get_exp_to_next_level(level: int) -> int:
    return level * 50


def apply_exp(gained: int) -> None:
    """경험치를 추가하고 레벨업을 처리합니다."""
    st.session_state.exp += gained
    while st.session_state.exp >= get_exp_to_next_level(st.session_state.cat_level):
        st.session_state.exp -= get_exp_to_next_level(st.session_state.cat_level)
        st.session_state.cat_level += 1


# ── 학습 알고리즘 헬퍼 ───────────────────────────────────────────────────────

def get_unlocked_topics() -> list[dict]:
    """is_unlocked=True 인 단원 목록을 반환합니다."""
    return [t for t in st.session_state.learning_status if t["is_unlocked"]]


def pick_topic() -> dict | None:
    """가중치(W = max(10, 100 - mastery_score)) 기반으로 단원을 선택합니다."""
    import random
    candidates = get_unlocked_topics()
    if not candidates:
        return None
    weights = [max(10, 100 - t["mastery_score"]) for t in candidates]
    return random.choices(candidates, weights=weights, k=1)[0]


def get_sample_question(topic_id: str) -> dict:
    """해당 단원의 샘플 문제를 무작위로 반환합니다."""
    import random
    questions = SAMPLE_QUESTIONS.get(topic_id)
    if not questions:
        return DEFAULT_QUESTION
    return random.choice(questions)
