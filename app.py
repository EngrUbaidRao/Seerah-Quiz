import time
import streamlit as st
from database import init_db, save_result, get_leaderboard, get_player_history, get_total_attempts


quiz_data = [
    {
        "question": "What year was the Prophet Muhammad (PBUH) born?",
        "options": ["570 CE", "610 CE", "622 CE", "632 CE"],
        "answer": "570 CE",
        "explanation": "The Prophet (PBUH) was born in the Year of the Elephant, 570 CE, in Mecca.",
    },
    {
        "question": "What is the name of the Prophet's (PBUH) mother?",
        "options": ["Amina bint Wahb", "Khadijah bint Khuwaylid", "Fatimah bint Asad", "Safiyyah bint Abdul Muttalib"],
        "answer": "Amina bint Wahb",
        "explanation": "His mother, Amina bint Wahb, passed away when he was six years old.",
    },
    {
        "question": "In which city was the Prophet Muhammad (PBUH) born?",
        "options": ["Medina", "Mecca", "Ta'if", "Jerusalem"],
        "answer": "Mecca",
        "explanation": "He was born in Mecca, in the Banu Hashim clan of the Quraysh tribe.",
    },
    {
        "question": "What is the name of the Prophet's (PBUH) father?",
        "options": ["Abu Talib", "Abdullah ibn Abdul Muttalib", "Abdul Muttalib", "Hamza ibn Abdul Muttalib"],
        "answer": "Abdullah ibn Abdul Muttalib",
        "explanation": "His father Abdullah passed away before he was born.",
    },
    {
        "question": "Who was the first wife of the Prophet (PBUH)?",
        "options": ["Aisha bint Abu Bakr", "Khadijah bint Khuwaylid", "Hafsa bint Umar", "Zaynab bint Jahsh"],
        "answer": "Khadijah bint Khuwaylid",
        "explanation": "Khadijah (RA) was a respected businesswoman and the first person to accept Islam.",
    },
    {
        "question": "At what age did the Prophet (PBUH) receive the first revelation?",
        "options": ["30", "35", "40", "45"],
        "answer": "40",
        "explanation": "The first revelation came in the Cave of Hira when he was 40 years old.",
    },
    {
        "question": "Which angel brought the revelations to the Prophet (PBUH)?",
        "options": ["Mikail", "Israfil", "Jibril (Gabriel)", "Azrael"],
        "answer": "Jibril (Gabriel)",
        "explanation": "Angel Jibril (AS) delivered the revelations of the Qur'an over 23 years.",
    },
    {
        "question": "What is the event of Hijrah?",
        "options": ["Battle of Badr", "Migration to Medina", "Night Journey", "Treaty of Hudaybiyyah"],
        "answer": "Migration to Medina",
        "explanation": "Hijrah refers to the migration from Mecca to Medina in 622 CE, marking the start of the Islamic calendar.",
    },
    {
        "question": "What is the name of the Prophet's (PBUH) last sermon called?",
        "options": ["Khutbatul-Wida (Farewell Sermon)", "Khutbah al-Jummah", "Khutbah al-Hajj", "Khutbah al-Aqsa"],
        "answer": "Khutbatul-Wida (Farewell Sermon)",
        "explanation": "Delivered during his final pilgrimage, it summarized the core teachings of Islam.",
    },
    {
        "question": "Where is the Prophet Muhammad (PBUH) buried?",
        "options": ["Mecca", "Jerusalem", "Medina", "Karbala"],
        "answer": "Medina",
        "explanation": "He is buried in Masjid an-Nabawi, in Medina.",
    },
]
TOTAL_Q = len(quiz_data)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config("Seerah Quiz", page_icon="🕌", layout="centered")
init_db()

# ---------------- CUSTOM CSS ---------------- #
st.markdown(
    """
    <style>
    .stApp { background-color: #f7f5ef; }
    .main .block-container { padding-top: 2rem; max-width: 720px; }

    .quiz-header {
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
    }
    .quiz-header h1 { color: #0f6e56; margin-bottom: 0.1rem; }
    .quiz-header p { color: #5f5e5a; font-size: 0.95rem; }

    .question-card {
        background: #ffffff;
        border: 1px solid #e3e0d5;
        border-left: 6px solid #0f6e56;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .question-card h4 { color: #26215c; margin-top: 0; }

    .stRadio > label { font-weight: 500; }
    div[role="radiogroup"] label {
        background: #fbfaf6;
        border: 1px solid #e3e0d5;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        width: 100%;
    }
    /* Force visible dark text for radio option labels regardless of light/dark theme */
    div[role="radiogroup"] label p,
    div[role="radiogroup"] label span,
    div[role="radiogroup"] label div {
        color: #2c2c2a !important;
        font-size: 0.95rem;
    }
    div[role="radiogroup"] label:hover {
        border-color: #0f6e56;
    }

    .stButton > button {
        background-color: #0f6e56;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #085041; color: white; }

    .score-banner {
        text-align: center;
        background: linear-gradient(90deg, #0f6e56, #1d9e75);
        color: white;
        border-radius: 14px;
        padding: 1.6rem;
        margin-bottom: 1.2rem;
    }
    .score-banner h1 { color: white; font-size: 2.6rem; margin: 0; }
    .score-banner p { color: #e1f5ee; margin: 0; }

    .leaderboard-row {
        display: flex; justify-content: space-between;
        padding: 0.5rem 0.8rem; border-bottom: 1px solid #ececec;
        font-size: 0.92rem;
    }

    /* ---------- Responsive tweaks for phones / small screens ---------- */
    @media (max-width: 640px) {
        .main .block-container { padding-left: 0.8rem; padding-right: 0.8rem; padding-top: 1rem; }
        .quiz-header h1 { font-size: 1.5rem; }
        .quiz-header p { font-size: 0.85rem; }
        .question-card { padding: 1rem; }
        .question-card h4 { font-size: 1.05rem; }
        .score-banner h1 { font-size: 2rem; }
        div[role="radiogroup"] label { padding: 0.6rem 0.7rem; }
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
        .stButton > button { width: 100%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- SESSION STATE ---------------- #
defaults = {
    "stage": "welcome",   # welcome -> quiz -> results
    "player_name": "",
    "player_email": "",
    "q_index": 0,
    "answers": {},
    "start_time": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def restart():
    st.session_state.stage = "welcome"
    st.session_state.q_index = 0
    st.session_state.answers = {}
    st.session_state.start_time = None


# ---------------- SIDEBAR: LEADERBOARD ---------------- #
with st.sidebar:
    st.markdown("### 🏆 Leaderboard")
    board = get_leaderboard(10)
    if not board:
        st.caption("No attempts yet — be the first!")
    else:
        for i, row in enumerate(board, start=1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            st.markdown(
                f"<div class='leaderboard-row'><span>{medal} {row['player_name']}</span>"
                f"<span>{row['score']}/{row['total_questions']} ({row['percentage']}%)</span></div>",
                unsafe_allow_html=True,
            )
    st.caption(f"Total attempts recorded: {get_total_attempts()}")

# ---------------- HEADER ---------------- #
st.markdown(
    """
    <div class="quiz-header">
        <h1>🕌 Seerah Quiz</h1>
        <p>Test your knowledge of the life of Prophet Muhammad (PBUH) — 10 questions</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- WELCOME SCREEN ---------------- #
if st.session_state.stage == "welcome":
    st.write("")
    name = st.text_input("Your name", value=st.session_state.player_name, placeholder="e.g. Ali Raza")
    email = st.text_input("Your email", value=st.session_state.player_email, placeholder="e.g. ali@example.com")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("Questions", TOTAL_Q)
    with col2:
        st.metric("Players so far", get_total_attempts())
    if st.button("Start Quiz ➜", use_container_width=True):
        name = name.strip()
        email = email.strip()
        if not name:
            st.warning("Please enter your name before starting.")
        elif not email or "@" not in email or "." not in email.split("@")[-1]:
            st.warning("Please enter a valid email address before starting.")
        else:
            st.session_state.player_name = name
            st.session_state.player_email = email
            st.session_state.stage = "quiz"
            st.session_state.q_index = 0
            st.session_state.answers = {}
            st.session_state.start_time = time.time()
            st.rerun()

# ---------------- QUIZ SCREEN (one question at a time) ---------------- #
elif st.session_state.stage == "quiz":
    idx = st.session_state.q_index
    q = quiz_data[idx]

    st.progress((idx) / TOTAL_Q, text=f"Question {idx + 1} of {TOTAL_Q}")

    st.markdown(
        f"""<div class="question-card"><h4>Q{idx + 1}. {q['question']}</h4></div>""",
        unsafe_allow_html=True,
    )

    current_answer = st.session_state.answers.get(idx)
    choice = st.radio(
        "Choose one:",
        q["options"],
        index=q["options"].index(current_answer) if current_answer in q["options"] else None,
        key=f"radio_{idx}",
        label_visibility="collapsed",
    )
    if choice:
        st.session_state.answers[idx] = choice

    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        if idx > 0 and st.button("← Back"):
            st.session_state.q_index -= 1
            st.rerun()
    with nav3:
        label = "Finish ✔" if idx == TOTAL_Q - 1 else "Next →"
        if st.button(label, use_container_width=True):
            if idx == TOTAL_Q - 1:
                score = sum(
                    1 for i, item in enumerate(quiz_data)
                    if st.session_state.answers.get(i) == item["answer"]
                )
                elapsed = int(time.time() - st.session_state.start_time)
                save_result(st.session_state.player_name, st.session_state.player_email, score, TOTAL_Q, elapsed)
                st.session_state.stage = "results"
                st.rerun()
            else:
                st.session_state.q_index += 1
                st.rerun()

# ---------------- RESULTS SCREEN ---------------- #
elif st.session_state.stage == "results":
    score = sum(
        1 for i, item in enumerate(quiz_data)
        if st.session_state.answers.get(i) == item["answer"]
    )
    pct = round((score / TOTAL_Q) * 100, 2)

    st.markdown(
        f"""
        <div class="score-banner">
            <p>{st.session_state.player_name}, your result</p>
            <h1>{score}/{TOTAL_Q}</h1>
            <p>{pct}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if pct == 100:
        st.success("Perfect score, mashaAllah! 🌟")
    elif pct >= 70:
        st.info("Great job! 👏")
    else:
        st.warning("Good effort — review the answers below and try again.")

    with st.expander("📖 Review your answers", expanded=True):
        for i, q in enumerate(quiz_data):
            user_ans = st.session_state.answers.get(i)
            correct = q["answer"]
            if user_ans == correct:
                st.success(f"Q{i+1}. {q['question']}\n\nYour answer: {user_ans} ✅")
            else:
                st.error(f"Q{i+1}. {q['question']}\n\nYour answer: {user_ans or '—'} ❌  |  Correct: {correct}")
            st.caption(q["explanation"])

    history = get_player_history(st.session_state.player_name, 5)
    if len(history) > 1:
        with st.expander("📊 Your past attempts"):
            for h in history:
                st.write(f"{h['played_at']} — {h['score']}/{h['total_questions']} ({h['percentage']}%)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Retake Quiz", use_container_width=True):
            restart()
            st.rerun()
    with col2:
        if st.button("👤 Change Player", use_container_width=True):
            st.session_state.player_name = ""
            st.session_state.player_email = ""
            restart()
            st.rerun()
