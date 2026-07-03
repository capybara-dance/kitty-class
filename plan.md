# 🐾 Kitty's Class — 구현 계획서

> **프로젝트 한 줄 요약:** 초등 3학년 수학을 고양이 테마 스토리텔링으로 학습하는 Streamlit 기반 웹 앱

---

## 1. 기술 스택

| 항목 | 선택 |
| :--- | :--- |
| 프론트엔드 / 서버 | Streamlit (Python) |
| 데이터 저장소 | Google Sheets (gspread + oauth2client) |
| 배포 환경 | Streamlit Cloud 무료 티어 |
| 디자인 | 파스텔톤(핑크·연보라·민트) + 유니코드 이모지 |

---

## 2. 프로젝트 구조 (권장 디렉터리 레이아웃)

```
kitty-class/
├── streamlit_app.py        # Streamlit 진입점 (페이지 라우팅)
├── pages/
│   ├── 01_home.py          # 마이룸 & 고양이 대시보드
│   ├── 02_adventure.py     # 학습(동물 구조 모험) 화면
│   └── 03_dex.py           # 동물 도감
├── core/
│   ├── sheets.py           # Google Sheets CRUD 헬퍼
│   ├── curriculum.py       # 단원 정의 & 문제 생성 로직
│   ├── algorithm.py        # 가중치 선택 & 이해도 갱신
│   └── cat.py              # 고양이 레벨/경험치 시스템
├── assets/
│   └── style.css           # 커스텀 CSS (파스텔 테마)
├── .env                    # 로컬 환경변수 (python-dotenv, .gitignore)
├── .env.example            # 환경변수 예시 (Git에 포함)
├── requirements.txt
└── plan.md
```

---

## 3. 데이터베이스 스키마 (Google Sheets 3탭)

### 탭 1 — `user_game_data`
| 컬럼 | 타입 | 설명 |
| :--- | :--- | :--- |
| `user_id` | String | 사용자 고유 식별자 |
| `cat_name` | String | 아이가 지어준 고양이 이름 |
| `cat_level` | Int | 고양이 레벨 (경험치에 따른 진화) |
| `exp` | Int | 현재 경험치 |
| `gold` | Int | 츄르코인 보유량 |
| `rescued_count` | Int | 총 구출 동물 수 |

### 탭 2 — `learning_status`
| 컬럼 | 타입 | 설명 |
| :--- | :--- | :--- |
| `topic_id` | String | 단원명 (예: `덧셈과_뺄셈`) |
| `total_solved` | Int | 총 풀이 횟수 |
| `correct_count` | Int | 정답 횟수 |
| `mastery_score` | Int | 이해도 점수 (0~100) |

### 탭 3 — `rescue_dex_logs`
| 컬럼 | 타입 | 설명 |
| :--- | :--- | :--- |
| `rescue_time` | DateTime | 구출 성공 시각 |
| `category` | String | 동물/곤충 분류 |
| `animal_name` | String | 구출된 동물 이름 |
| `rarity` | String | 희귀도 (일반 / 희귀 / 전설) |

---

## 4. 핵심 알고리즘

### 4-A. 가중치 기반 문제 출제
```
가중치 W = 100 - mastery_score
```
- `mastery_score`가 낮을수록(취약 단원) 가중치가 높아져 문제 노출 빈도 증가.
- `mastery_score < 60`인 단원은 노출 확률 **약 2배** 이상 보장.
- 구현: `random.choices(topics, weights=[W1, W2, ...])` 사용.

### 4-B. 이해도 점수 갱신
```
정답 시: mastery_score = min(100, mastery_score + 5)
오답 시: mastery_score = max(0,  mastery_score - 3)
```

### 4-C. 절차적 스토리텔링 문제 생성
- 단원별 템플릿 딕셔너리에서 무작위 동물·아이템·숫자를 조합.
- 예시 템플릿 (나눗셈):
  > `"{동물}들이 모은 {아이템} {A}개를 {B}마리에게 똑같이 나누어 주려고 해냥! 한 마리가 몇 개씩 가질 수 있을까냥?"`

### 4-D. 고양이 성장 시스템
| 레벨 범위 | 진화 형태 | 이모지 |
| :---: | :---: | :---: |
| 1–4 | 아기 고양이 | 🐾 |
| 5–9 | 고양이 마법사 | 🐱 |
| 10+ | 전설의 냥이 | 🦄 |
- 경험치 획득: 정답 +10 EXP, 첫 구출 보너스 +20 EXP.
- 레벨업 조건: `exp >= level * 50`.

---

## 5. 초등 3학년 수학 커리큘럼 (문제 생성 단원 목록)

### 1학기
| 단원 | 주제 | 난이도 |
| :--- | :--- | :---: |
| 1 | 덧셈과 뺄셈 (세 자리 수, 받아올림/내림) | ⭐⭐ |
| 2 | 평면도형 (선분, 직각, 직사각형, 정사각형) | ⭐ |
| 3 | 나눗셈 기초 (곱셈구구 활용, 똑같이 나누기) | ⭐⭐ |
| 4 | 곱셈 (두 자리 × 한 자리, 올림) | ⭐⭐ |
| 5 | 길이와 시간 (mm, km, 초 단위) | ⭐⭐ |
| 6 | **분수와 소수 ★핵심** (등분, 분수 개념, 소수 기초) | ⭐⭐⭐ |

### 2학기
| 단원 | 주제 | 난이도 |
| :--- | :--- | :---: |
| 1 | 곱셈 심화 (세 자리 × 한 자리, 두 자리 × 두 자리) | ⭐⭐⭐ |
| 2 | **나눗셈 심화 ★핵심** (나머지 개념 첫 등장) | ⭐⭐⭐ |
| 3 | 원 (중심, 반지름, 지름, 컴퍼스) | ⭐⭐ |
| 4 | **분수 심화 ★핵심** (진분수, 가분수, 대분수, 크기 비교) | ⭐⭐⭐ |
| 5 | 들이와 무게 (L, mL, kg, g, t) | ⭐⭐ |
| 6 | 자료의 정리 (표, 그림그래프) | ⭐ |

---

## 6. UI/UX 흐름

```
[앱 실행]
    │
    ▼
[온보딩] ── 처음 방문 시 고양이 이름 짓기 → user_game_data 생성
    │
    ▼
[메인 화면 / 마이룸]
  ├─ 고양이 상태 카드 (레벨, EXP 바, 이름)
  ├─ "오늘의 도전" 버튼  →  [학습 화면]
  └─ "동물 도감" 버튼   →  [도감 화면]

[학습 화면 / 동물 구조 모험]
  ├─ 가중치 알고리즘으로 단원 선택
  ├─ 스토리텔링 문제 생성 & 출제
  ├─ 정답 시: st.balloons() + 🐾 스탬프 + 동물 구출 연출
  └─ 오답 시: 고양이 힌트 (시각적 교구 이모지 활용, 정답 미공개)
```

### 핵심 UX 규칙
- **오답 처리:** 정답을 바로 알려주지 않고, 해당 단원 핵심 개념(예: 곱셈이면 구구단 원리)을 활용한 힌트만 제공.
- **색상 팔레트:** `#FFB7C5`(핑크), `#C8B2E8`(연보라), `#B2E8D4`(민트).
- **폰트 / 이모지:** 경량화를 위해 별도 이미지 없이 유니코드 이모지 전용 사용.

---

## 7. 구현 로드맵

### 1단계 — 기반 구축 (Prototype)
- [ ] Google Cloud 서비스 계정 생성 & Sheets API 활성화
- [ ] `core/sheets.py`: gspread 연동, 3개 탭 CRUD 함수 구현
- [ ] `.env` 파일 작성 및 `python-dotenv`로 로컬 환경변수 로드 설정
- [ ] `.env.example` 작성 (키 이름만 포함, 값은 비워둠)
- [ ] Streamlit Cloud 배포 시 Secrets 기능으로 동일 변수 주입
- [ ] 기본 앱 실행 확인 (`streamlit_app.py` 뼈대)

### 2단계 — 문제 생성 엔진
- [ ] `core/curriculum.py`: 12개 단원 템플릿 딕셔너리 정의
- [ ] 각 단원별 숫자 범위 및 정답 계산 로직 구현
- [ ] 단위 테스트: 문제 생성 함수 정확성 검증

### 3단계 — 학습 알고리즘 & 고양이 시스템
- [ ] `core/algorithm.py`: 가중치 선택(`random.choices`) 구현
- [ ] 이해도 점수 갱신 로직 (정답/오답 시 ±점수)
- [ ] `core/cat.py`: 경험치·레벨·진화 로직 구현
- [ ] `rescue_dex_logs` 저장 및 희귀도 뽑기 로직

### 4단계 — UI 구현
- [ ] `pages/01_home.py`: 마이룸 대시보드 (고양이 카드, EXP 바)
- [ ] `pages/02_adventure.py`: 학습 화면 (문제 출제, 정답/오답 연출)
- [ ] `pages/03_dex.py`: 동물 도감 (구출 기록 테이블)
- [ ] `assets/style.css`: 파스텔 테마 커스텀 CSS 적용

### 5단계 — 배포 및 마무리
- [ ] `requirements.txt` 정리 (streamlit, gspread, oauth2client 등)
- [ ] Streamlit Cloud 연결 & 환경변수(secrets) 등록
- [ ] 실사용 테스트 (아이 대상 UX 검증)
- [ ] README.md 작성

---

## 8. 주요 의존성 (requirements.txt 초안)

```
streamlit>=1.32.0
gspread>=6.0.0
oauth2client>=4.1.3
pandas>=2.0.0
python-dotenv>=1.0.0
```

---

## 9. 보안 / 운영 주의사항

- Google 서비스 계정 키(`credentials.json`) 및 `.env`는 **절대 Git에 커밋하지 않음** → `.gitignore`에 추가.
- **로컬 개발:** `.env` 파일에 환경변수 저장, `python-dotenv`의 `load_dotenv()`로 로드.
  ```
  # .env.example
  GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
  SPREADSHEET_ID=your_spreadsheet_id
  ```
- **Streamlit Cloud 배포:** Secrets 기능을 통해 동일 환경변수를 주입 (`os.environ` 또는 `st.secrets` 공용 접근).
- Google Sheets 공유 설정: 서비스 계정 이메일에만 **편집자** 권한 부여.
