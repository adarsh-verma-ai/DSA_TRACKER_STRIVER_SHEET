import streamlit as st
import json
import os
from questions_data import DSA_SHEET

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Striver A2Z DSA Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load / Save Progress ───────────────────────────────────────────────────────
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

def toggle_done(pid):
    key = str(pid)
    st.session_state.progress[key] = not st.session_state.progress.get(key, False)
    save_progress(st.session_state.progress)

# ─── Helpers ────────────────────────────────────────────────────────────────────
def is_done(pid):
    return st.session_state.progress.get(str(pid), False)

def get_all_problems():
    all_p = []
    for step in DSA_SHEET:
        for sub in step["sub_steps"]:
            for p in sub["problems"]:
                all_p.append(p)
    return all_p

def get_step_stats(step):
    total, done = 0, 0
    for sub in step["sub_steps"]:
        for p in sub["problems"]:
            total += 1
            if is_done(p["id"]):
                done += 1
    return done, total

def get_overall_stats():
    all_p = get_all_problems()
    total = len(all_p)
    done = sum(1 for p in all_p if is_done(p["id"]))
    easy = [p for p in all_p if p["difficulty"] == "Easy"]
    medium = [p for p in all_p if p["difficulty"] == "Medium"]
    hard = [p for p in all_p if p["difficulty"] == "Hard"]
    easy_done = sum(1 for p in easy if is_done(p["id"]))
    med_done = sum(1 for p in medium if is_done(p["id"]))
    hard_done = sum(1 for p in hard if is_done(p["id"]))
    return {
        "total": total, "done": done,
        "easy": len(easy), "easy_done": easy_done,
        "medium": len(medium), "med_done": med_done,
        "hard": len(hard), "hard_done": hard_done,
    }

DIFF_COLOR = {"Easy": "#00b8a3", "Medium": "#f7b731", "Hard": "#fc5c65"}

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

/* ── Root ── */
:root {
    --bg: #0e1117;
    --surface: #161b22;
    --surface2: #1c2330;
    --border: #30363d;
    --accent: #f7b731;
    --accent2: #fc5c65;
    --green: #00b8a3;
    --text: #e6edf3;
    --muted: #8b949e;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Progress bar custom ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00b8a3, #f7b731) !important;
    border-radius: 999px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 0.2rem 0.6rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Metric boxes ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2rem !important;
    color: var(--accent) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    margin-bottom: 6px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}

/* ── Problem row card ── */
.prob-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    margin-bottom: 6px;
    background: var(--surface2);
    transition: border-color 0.2s;
}
.prob-row.done {
    opacity: 0.5;
    border-color: var(--green) !important;
}
.prob-row:hover {
    border-color: var(--accent) !important;
}
.prob-name {
    flex: 1;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
}
.prob-name.done-text {
    text-decoration: line-through;
    color: var(--muted);
}
.badge {
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.lc-link {
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 0.72rem;
    font-weight: 700;
    text-decoration: none !important;
    font-family: 'JetBrains Mono', monospace;
}
.lc-btn {
    background: #1a1a2e;
    color: #ffa116 !important;
    border: 1px solid #ffa116;
}
.gfg-btn {
    background: #0a1a0a;
    color: #2f8d46 !important;
    border: 1px solid #2f8d46;
}
.step-header {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: var(--accent);
    margin: 1rem 0 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.5rem;
}
.sub-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--muted);
    margin: 0.8rem 0 0.4rem 0.2rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    background: linear-gradient(90deg, #f7b731, #fc5c65);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne;font-weight:800;font-size:1.1rem;color:#f7b731;margin-bottom:1rem'>⚡ A2Z DSA Tracker</div>", unsafe_allow_html=True)

    stats = get_overall_stats()
    pct = int(100 * stats["done"] / stats["total"]) if stats["total"] else 0
    st.markdown(f"**Overall Progress: {stats['done']}/{stats['total']}**")
    st.progress(stats["done"] / max(stats["total"], 1))
    st.markdown(f"<span style='color:#00b8a3'>● Easy {stats['easy_done']}/{stats['easy']}</span> &nbsp; <span style='color:#f7b731'>● Med {stats['med_done']}/{stats['medium']}</span> &nbsp; <span style='color:#fc5c65'>● Hard {stats['hard_done']}/{stats['hard']}</span>", unsafe_allow_html=True)
    st.divider()

    view_mode = st.radio("View", ["All Steps", "Pending Only", "Completed"], index=0)
    st.divider()

    st.markdown("**Jump to Step**")
    step_names = [f"Step {s['step']}: {s['title']}" for s in DSA_SHEET]
    selected_step = st.selectbox("", ["— All —"] + step_names, label_visibility="collapsed")

    st.divider()
    filter_diff = st.multiselect("Filter Difficulty", ["Easy", "Medium", "Hard"], default=["Easy", "Medium", "Hard"])

    if st.button("🗑 Reset All Progress", use_container_width=True):
        st.session_state.progress = {}
        save_progress({})
        st.rerun()

# ─── Main Header ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="hero-title">⚡ Striver A2Z DSA Sheet</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Track your progress • Click problem name to solve • LeetCode & GFG links</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Progress", f"{pct}%", f"{stats['done']} solved")

st.divider()

# ─── Filter which steps to show ─────────────────────────────────────────────────
if selected_step == "— All —":
    steps_to_show = DSA_SHEET
else:
    step_num = int(selected_step.split(":")[0].replace("Step ", "").strip())
    steps_to_show = [s for s in DSA_SHEET if s["step"] == step_num]

# ─── Render Steps ───────────────────────────────────────────────────────────────
for step in steps_to_show:
    done_c, total_c = get_step_stats(step)
    icon = "✅" if done_c == total_c else "🔷"

    st.markdown(f'<div class="step-header">{icon} Step {step["step"]}: {step["title"]} <span style="font-size:0.85rem;color:#8b949e;font-weight:400">{done_c}/{total_c}</span></div>', unsafe_allow_html=True)
    st.progress(done_c / max(total_c, 1))

    for sub in step["sub_steps"]:
        sub_done = sum(1 for p in sub["problems"] if is_done(p["id"]))
        sub_total = len(sub["problems"])

        with st.expander(f"**{sub['sub']} — {sub['name']}** ({sub_done}/{sub_total})", expanded=(selected_step != "— All —")):
            for p in sub["problems"]:
                # Apply view mode filter
                if view_mode == "Pending Only" and is_done(p["id"]):
                    continue
                if view_mode == "Completed" and not is_done(p["id"]):
                    continue
                # Apply difficulty filter
                if p["difficulty"] not in filter_diff:
                    continue

                done_flag = is_done(p["id"])
                diff = p["difficulty"]
                color = DIFF_COLOR.get(diff, "#8b949e")

                col_check, col_name, col_diff, col_lc, col_gfg = st.columns([0.5, 5, 1.2, 1.2, 1.2])

                with col_check:
                    if st.button("✅" if done_flag else "○", key=f"btn_{p['id']}"):
                        toggle_done(p["id"])
                        st.rerun()

                with col_name:
                    name_style = "text-decoration:line-through;color:#8b949e;" if done_flag else "color:#e6edf3;"
                    st.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.83rem;{name_style}'>{p['name']}</span>", unsafe_allow_html=True)

                with col_diff:
                    st.markdown(f"<span class='badge' style='background:{color}22;color:{color};border:1px solid {color}44'>{diff}</span>", unsafe_allow_html=True)

                with col_lc:
                    if p.get("leetcode"):
                        st.markdown(f"<a href='{p['leetcode']}' target='_blank' class='lc-link lc-btn'>LeetCode ↗</a>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:#30363d;font-size:0.72rem'>—</span>", unsafe_allow_html=True)

                with col_gfg:
                    if p.get("gfg"):
                        st.markdown(f"<a href='{p['gfg']}' target='_blank' class='lc-link gfg-btn'>GFG ↗</a>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:#30363d;font-size:0.72rem'>—</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("<div style='text-align:center;color:#8b949e;font-size:0.75rem;font-family:JetBrains Mono,monospace'>Striver A2Z DSA Sheet Tracker • Progress saved locally • Built with Streamlit</div>", unsafe_allow_html=True)
