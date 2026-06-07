# ⚡ Striver A2Z DSA Tracker

A full-featured DSA progress tracker for [Striver's A2Z Sheet](https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z) built with Streamlit.

## Features
- ✅ All 430+ problems from the A2Z sheet
- 🔗 Direct LeetCode links (opens your account)
- 🟢 GFG links for problems not on LeetCode
- 📊 Progress tracking per step, sub-step, and difficulty
- 💾 Progress saved locally to `progress.json`
- 🎯 Filter by difficulty (Easy / Medium / Hard)
- 🔍 Jump to any step from sidebar

## Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Deploy on Streamlit Cloud (Free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repo → set `app.py` as the main file
5. Click **Deploy** — done!

> **Note:** On Streamlit Cloud, progress resets on each deploy. For persistent progress, consider using `st.session_state` with a database or keep using local deployment.

## Files
```
dsa_tracker/
├── app.py              # Main Streamlit app
├── questions_data.py   # All 430+ problems with LeetCode/GFG links
├── requirements.txt    # Python dependencies
├── progress.json       # Auto-created on first run (your progress)
└── README.md
```
