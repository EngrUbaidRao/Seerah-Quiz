# 🕌 Seerah Quiz

An interactive **Streamlit** quiz app that tests knowledge of the life (Seerah) of Prophet Muhammad (PBUH) — built with a persistent **SQLite** database, a one-question-at-a-time flow, and a live leaderboard.

## ✨ Features

- **10-question quiz** with instant scoring
- **One question per screen** with a progress bar (instead of one long scroll)
- **Back / Next navigation** so users can review or change answers before submitting
- **SQLite database** — every attempt is saved (name, score, percentage, time taken)
- **Live leaderboard** in the sidebar, ranked by score
- **Answer review** after submission, with a short explanation for each question
- **Personal history** — see your last 5 attempts
- Clean, custom-styled UI (no default Streamlit look)

## 🛠 Tech stack

- [Streamlit](https://streamlit.io/) — UI framework
- SQLite (via Python's built-in `sqlite3`) — persistent storage, no external DB required
- Pure Python, no heavy dependencies

## 📁 Project structure

```
seerah-quiz/
├── app.py            # Streamlit UI and quiz logic
├── database.py        # SQLite setup, save/query functions
├── requirements.txt
└── README.md
```

## 🚀 Run locally

```bash
git clone https://github.com/<your-username>/seerah-quiz.git
cd seerah-quiz
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`. A `quiz_data.db` file is created automatically on first run.

## ☁️ Deploy for free

The easiest option is [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub
2. Go to share.streamlit.io → "New app" → select your repo and `app.py`
3. Deploy — you'll get a public link to add to your LinkedIn/GitHub profile

## 🗺 Possible next steps

- Add more question categories (Sahaba, Battles, Qur'an)
- Add a countdown timer per question
- Export leaderboard to CSV
- Add multi-language support (Urdu/English toggle)

## 📄 License

MIT — feel free to fork and extend.
