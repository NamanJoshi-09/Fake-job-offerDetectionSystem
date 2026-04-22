import streamlit as st
import pickle
from train_model import explain_prediction

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ─── Sample Texts ────────────────────────────────────────────────────────────
SCAM_SAMPLE = """Job Title: Work From Home Data Entry Specialist — $5,000/Week GUARANTEED!

We are a global company hiring IMMEDIATELY. No experience needed. No interview required.
You will earn $200–$500 per hour processing simple online forms from the comfort of your home.

Requirements:
- Must be 18+
- Access to a smartphone or computer
- Willing to receive payments and forward funds to our international partners

To get started, you MUST pay a small $49.99 registration and training kit fee.
Once paid, your earning account is activated within 24 hours.

Contact us on WhatsApp: +1-555-0199 or email: jobs@quick-cash-now.biz
DO NOT miss this opportunity — only 10 spots left!!"""

REAL_SAMPLE = """Job Title: Junior Software Engineer — Python/Django

Company: TechNova Solutions (Series B, 120 employees)
Location: Hybrid — Bangalore, India (3 days/week in office)
Salary: ₹8–12 LPA depending on experience

About the Role:
We're looking for a curious and driven junior engineer to join our backend team. You'll work
closely with senior engineers on our SaaS analytics platform, shipping features end-to-end.

Responsibilities:
- Build and maintain REST APIs using Python and Django
- Write clean, well-tested code with >80% coverage
- Participate in code reviews and sprint planning
- Debug and optimise database queries (PostgreSQL)

Requirements:
- 1–2 years of Python development experience (internships count)
- Familiarity with Git, REST principles, and basic SQL
- A degree in CS, Engineering, or equivalent practical experience

Benefits:
- Health insurance for employee + family
- 18 days PTO + public holidays
- Annual learning budget of ₹25,000

To apply, send your resume and a brief note about a project you're proud of to:
careers@technova.io — please use subject line "Junior SWE Application"."""

# ─── Session State Init ───────────────────────────────────────────────────────
if "job_text" not in st.session_state:
    st.session_state.job_text = ""
# BUG FIX: Removed auto_run session state — sample buttons now only load text,
# they do NOT trigger analysis. User must click "RUN DIAGNOSTICS" manually.

st.set_page_config(
    page_title="DataMinds",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=JetBrains+Mono:wght@400;500;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Nunito:wght@400;500;600;700&display=swap');

:root {
    --bg:       #050a14;
    --surface:  #0b1425;
    --surface2: rgba(11,20,37,0.62);
    --border:   rgba(0,210,255,0.15);
    --cyan:     #00d2ff;
    --cdim:     rgba(0,210,255,0.07);
    --red:      #ff3b5c;
    --green:    #00f5a0;
    --amber:    #ffb700;
    --text:     #e8f0fe;
    --muted:    #5a7090;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* A11y + UX */
:focus-visible { outline: 2px solid rgba(0,210,255,0.55) !important; outline-offset: 3px !important; }
@media (prefers-reduced-motion: reduce) {
    * { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}

.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    background-size: 200px; opacity: 0.5;
}
.stApp::after {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(0,210,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,210,255,0.025) 1px, transparent 1px);
    background-size: 64px 64px;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── NAVBAR ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 56px; border-bottom: 1px solid var(--border);
    background: rgba(5,10,20,0.85); backdrop-filter: blur(16px);
    position: sticky; top: 0; z-index: 999;
}
.nav-logo { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 17px; letter-spacing: 3px; color: var(--cyan); text-transform: uppercase; }
.nav-logo span { color: var(--text); opacity: 0.35; }
.nav-badge { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 6px 16px; border: 1px solid var(--border); border-radius: 100px; color: var(--cyan); background: var(--cdim); letter-spacing: 2px; }

/* ── HERO ── */
.hero {
    padding: 80px 56px 40px; position: relative; overflow: hidden;
    background: linear-gradient(160deg, rgba(0,210,255,0.09) 0%, rgba(0,149,204,0.06) 30%, rgba(0,245,160,0.04) 60%, transparent 100%);
}
.hero-title { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: clamp(48px, 5.5vw, 82px); line-height: 1.0; letter-spacing: -2px; margin-bottom: 24px; color: var(--text); }
.hero-title em { font-style: normal; background: linear-gradient(135deg, #00d2ff 0%, #00f5a0 50%, #0095cc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(0 0 22px rgba(0,210,255,0.55)); }
.hero-sub { font-size: 16px; color: rgba(232, 240, 254, 0.72); max-width: 440px; line-height: 1.75; font-weight: 400; }

/* 🔥 NATIVE STREAMLIT CARDS 🔥 */
div[data-testid="column"]:has(.card-tag) > div:first-child {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 40px !important;
    position: relative !important;
    box-shadow: 0 0 40px rgba(0,210,255,0.05) !important;
}
div[data-testid="column"]:has(.card-tag) > div:first-child::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.45;
}

.card-tag { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 3px; color: var(--cyan); display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.card-tag-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); animation: blink 2s infinite; }
@keyframes blink { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:.35; transform:scale(.75); } }
.card-heading { font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 10px; }
.card-desc { font-size: 14px; color: var(--muted); line-height: 1.75; }

/* ── SAMPLE BUTTONS (Inside the Left Card) ── */
div[data-testid="column"]:has(.card-tag) div[data-testid="column"] div[data-testid="stButton"] > button {
    width: 100% !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    padding: 18px 16px !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: transparent !important;
    color: var(--text) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"]:has(.card-tag) div[data-testid="column"] div[data-testid="stButton"] > button:hover {
    background: var(--cdim) !important;
    border-color: rgba(0,210,255,0.35) !important;
}

/* ── TEXT AREA ── */
[data-testid="stTextArea"] label { display: none !important; }
[data-testid="stTextArea"] textarea {
    background: rgba(11,20,37,0.6) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
    padding: 20px !important;
    resize: none !important;
}
[data-testid="stTextArea"] textarea:focus { border-color: rgba(0,210,255,0.4) !important; box-shadow: 0 0 0 3px rgba(0,210,255,0.07) !important; outline: none !important; }
[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; box-shadow: none !important; }

/* ── SUBMIT BUTTON ── */
[data-testid="stFormSubmitButton"] > button { width: 100% !important; font-family: 'Nunito', sans-serif !important; font-size: 14px !important; font-weight: 700 !important; letter-spacing: 3px !important; text-transform: uppercase !important; padding: 17px !important; border-radius: 12px !important; border: none !important; background: linear-gradient(135deg, #00d2ff 0%, #0095cc 100%) !important; color: #050a14 !important; cursor: pointer !important; box-shadow: 0 6px 28px rgba(0,210,255,0.22) !important; transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important; margin-top: 12px !important; }
[data-testid="stFormSubmitButton"] > button:hover { transform: scale(1.02) translateY(-3px) !important; box-shadow: 0 14px 40px rgba(0,210,255,0.4) !important; }
[data-testid="stFormSubmitButton"] > button:active { transform: scale(0.98) translateY(0) !important; box-shadow: 0 4px 15px rgba(0,210,255,0.2) !important; }

/* ── DIAGNOSTICS REPORT ── */
.report {
    margin-top: 18px;
    background: linear-gradient(180deg, rgba(11,20,37,0.72) 0%, rgba(11,20,37,0.55) 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 18px 16px;
    position: relative;
    overflow: hidden;
}
.report::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(600px 180px at 18% 0%, rgba(0,210,255,0.12), transparent 55%);
    pointer-events: none;
}
.report-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}
.verdict {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(5,10,20,0.35);
}
.verdict-title { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 15px; letter-spacing: 0.4px; }
.verdict-sub { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.5px; color: rgba(232,240,254,0.65); margin-top: 4px; }
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    padding: 8px 10px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(0,210,255,0.06);
    color: var(--cyan);
    white-space: nowrap;
}
.badge.badge-red { color: #ffd3da; background: rgba(255,59,92,0.12); border-color: rgba(255,59,92,0.28); }
.badge.badge-green { color: #c9ffe7; background: rgba(0,245,160,0.11); border-color: rgba(0,245,160,0.25); }

.report-grid { display: grid; grid-template-columns: 1fr; gap: 10px; position: relative; z-index: 1; }
.report-h {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    color: rgba(232,240,254,0.62);
    margin-top: 2px;
}
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface2);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
}
.pill:hover { transform: translateY(-2px); border-color: rgba(0,210,255,0.32); box-shadow: 0 10px 24px rgba(0,210,255,0.07); background: rgba(11,20,37,0.85); }
.pill-k { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: rgba(232,240,254,0.88); }
.pill-v { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: rgba(232,240,254,0.52); }
.pill-s { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--border); }
.pill-s.fake { background: rgba(255,59,92,0.10); border-color: rgba(255,59,92,0.22); color: #ffd3da; }
.pill-s.real { background: rgba(0,245,160,0.09); border-color: rgba(0,245,160,0.20); color: #c9ffe7; }

/* Reset button container to prevent hover overlap */
.reset-button-container { margin-top: 28px; }
.reset-button-container [data-testid="stButton"] > button {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.16) !important;
    color: var(--text) !important;
}
.reset-button-container [data-testid="stButton"] > button:hover {
    transform: none !important;
    background: rgba(0,210,255,0.12) !important;
    border-color: rgba(0,210,255,0.35) !important;
    box-shadow: 0 10px 30px rgba(0,210,255,0.12) !important;
}

/* Make Streamlit alerts match theme */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    background: rgba(11,20,37,0.55) !important;
}

/* ── HOW IT WORKS ── */
.hiw { padding: 0 56px 72px; }
.hiw-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 4px; color: var(--cyan); margin-bottom: 12px; display: flex; align-items: center; gap: 12px; }
.hiw-eyebrow::before { content: ''; display: block; width: 28px; height: 1px; background: var(--cyan); }
.section-h { font-family: 'Outfit', sans-serif; font-size: 34px; font-weight: 800; margin-bottom: 6px; }
.section-sub { font-family: 'Plus Jakarta Sans', sans-serif; color: var(--muted); font-size: 14px; margin-bottom: 36px; }
.hiw-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
.hiw-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 30px 28px; position: relative; overflow: hidden; transition: transform .2s, box-shadow .2s; }
.hiw-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,210,255,0.07); }
.hiw-icon { font-size: 28px; margin-bottom: 14px; }
.hiw-t { font-family: 'Outfit', sans-serif; font-size: 17px; font-weight: 700; margin-bottom: 8px; }
.hiw-d { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: var(--muted); line-height: 1.7; }

/* ── MINOR PROJECT CARD ── */
.mp-section { padding: 0 56px 72px; }
.mp-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 56px 60px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(0,210,255,0.05);
}
.mp-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,210,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.mp-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2.5px;
    color: var(--cyan);
    margin-bottom: 18px;
}
.mp-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(26px, 3vw, 36px);
    font-weight: 800;
    color: var(--text);
    margin-bottom: 20px;
    line-height: 1.15;
}
.mp-desc {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    color: var(--muted);
    line-height: 1.85;
    margin-bottom: 28px;
}
.mp-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 32px;
}
.mp-tag {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: var(--cyan);
    background: var(--cdim);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 5px 14px;
    transition: transform .18s ease, border-color .18s ease, background .18s ease, box-shadow .18s ease;
}
.mp-tag:hover { transform: translateY(-2px); border-color: rgba(0,210,255,0.3); background: rgba(0,210,255,0.09); box-shadow: 0 10px 24px rgba(0,210,255,0.06); }
.mp-meta {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    color: var(--muted);
    line-height: 2;
}
.mp-right { }
.mp-team-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2.5px;
    color: var(--cyan);
    margin-bottom: 16px;
}
.mp-members { display: flex; flex-direction: column; gap: 14px; }
.mp-member {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(11,20,37,0.6);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    transition: all 0.3s ease;
}
.mp-member:hover {
    background: rgba(11,20,37,0.9);
    border-color: rgba(0,210,255,0.3);
    transform: translateX(4px);
    box-shadow: -4px 0 0 var(--cyan), 0 8px 24px rgba(0,210,255,0.08);
}
.mp-avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    background: var(--cdim);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: var(--cyan);
    border: 1px solid rgba(0,210,255,0.15);
    flex-shrink: 0;
}
.mp-member-info { display: flex; flex-direction: column; gap: 3px; }
.mp-member-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
}
.mp-member-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--cyan);
    letter-spacing: 0.5px;
}
.mp-member-role {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11.5px;
    color: var(--muted);
    line-height: 1.3;
}

/* ── FOOTER ── */
.footer { border-top: 1px solid var(--border); padding: 40px 56px; display: flex; align-items: center; justify-content: space-between; }
.foot-logo { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 18px; color: var(--cyan); letter-spacing: 2px; }
.foot-copy { font-family: 'Cormorant Garamond', serif; font-size: 14px; color: var(--muted); letter-spacing: 1.5px; font-weight: 300; font-style: italic; }
.foot-links { display: flex; gap: 28px; font-size: 13px; color: var(--muted); }

/* ── ANIMATIONS & TRANSITIONS ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero { animation: fadeInUp 0.7s ease-out forwards; }

div[data-testid="column"]:has(.card-tag) > div:first-child {
    opacity: 0;
    animation: fadeInUp 0.7s ease-out forwards;
    animation-delay: 0.2s;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
div[data-testid="column"]:has(.card-tag) > div:first-child:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px rgba(0,210,255,0.12) !important;
}

.hiw-card { opacity: 0; animation: fadeInUp 0.7s ease-out forwards; }
.hiw-card:nth-child(1) { animation-delay: 0.3s; }
.hiw-card:nth-child(2) { animation-delay: 0.4s; }
.hiw-card:nth-child(3) { animation-delay: 0.5s; }

.mp-card { opacity: 0; animation: fadeInUp 0.7s ease-out forwards; animation-delay: 0.6s; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.mp-card:hover { transform: translateY(-4px); box-shadow: 0 16px 50px rgba(0,210,255,0.1); }

/* Buttons */
[data-testid="stButton"] > button { transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important; border: 1px solid var(--border) !important; }
[data-testid="stButton"] > button:hover { transform: scale(1.02) translateY(-3px) !important; box-shadow: 0 10px 30px rgba(0,210,255,0.15) !important; border-color: rgba(0,210,255,0.3) !important; }
[data-testid="stButton"] > button:active { transform: scale(0.98) translateY(0) !important; box-shadow: none !important; }

[data-testid="stColumns"] { gap: 0 !important; }
[data-testid="stHorizontalBlock"] { gap: 20px !important; }
.sp8 { height: 8px; } .sp16 { height: 16px; } .sp28 { height: 28px; }

/* ── RESPONSIVE ── */
@media (max-width: 980px) {
    .navbar { padding: 16px 22px; }
    .hero { padding: 56px 22px 34px; }
    .hiw, .mp-section, .footer { padding-left: 22px; padding-right: 22px; }
    .hiw-grid { grid-template-columns: 1fr; }
    .mp-card { grid-template-columns: 1fr; padding: 32px 26px; gap: 30px; }
    .mp-members { gap: 10px; }
}
@media (max-width: 560px) {
    .nav-badge { display: none; }
}

</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Job<span>Shield</span> &nbsp;·&nbsp; DataMinds</div>
    <div class="nav-badge">● LIVE SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Detect Scam<br>Jobs <em>Instantly.</em></h1>
    <p class="hero-sub">
        Paste any job posting and our engine scans for fraud signals,
        deceptive language, and red-flag patterns in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 56px 60px;">', unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1.08], gap="large")

with col_l:
    st.markdown("""
        <div class="card-tag"><span class="card-tag-dot"></span>QUICK LOAD</div>
        <div class="card-heading">Try a Sample</div>
        <p class="card-desc" style="margin-bottom: 28px;">
            Click either sample below — it will load the posting
            into the analysis portal. Then click <strong>Run Diagnostics</strong>.
        </p>
    """, unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2, gap="large")

    with btn_col1:
        scam_clicked = st.button("🚩  Scam Sample", key="btn_scam", use_container_width=True)

    with btn_col2:
        real_clicked = st.button("✅  Real Sample", key="btn_real", use_container_width=True)

    # BUG FIX: Only load text into session state — do NOT set auto_run.
    # Analysis will only run when the user explicitly clicks "RUN DIAGNOSTICS".
    if scam_clicked:
        st.session_state.job_text = SCAM_SAMPLE
        st.rerun()

    if real_clicked:
        st.session_state.job_text = REAL_SAMPLE
        st.rerun()

with col_r:
    st.markdown("""
        <div class="card-tag"><span class="card-tag-dot"></span>ANALYSIS PORTAL</div>
        <div class="card-heading">Paste Job Description</div>
    """, unsafe_allow_html=True)

    with st.form("verify_form"):
        st.text_area(
            "JOB POSTING TEXT",
            height=272,
            placeholder="Paste the full job description here — title, responsibilities, salary, contact info…",
            key="job_text",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("⚡  RUN DIAGNOSTICS", use_container_width=True)

    # BUG FIX: Only run analysis when the form is explicitly submitted.
    if submitted:
        text = st.session_state.job_text.strip()
        if not text:
            st.warning("Please enter a job description.")
        else:
            pred, prob, reasons = explain_prediction(text, model, vectorizer)

            if pred == 1:
                confidence = prob * 100
                verdict_title = "Fake Job Detected"
                verdict_badge = "HIGH RISK" if confidence >= 75 else "RISK"
                badge_class = "badge-red"
            else:
                confidence = (1 - prob) * 100
                verdict_title = "Genuine Job"
                verdict_badge = "LIKELY SAFE" if confidence >= 75 else "CHECK DETAILS"
                badge_class = "badge-green"

            # Clean, themed diagnostics container (replaces default Streamlit text list)
            pills_html = []
            for word, score, label in reasons:
                safe_label = "FAKE" if str(label).upper() == "FAKE" else "REAL"
                pill_cls = "fake" if safe_label == "FAKE" else "real"
                pills_html.append(
                    f"""<div class="pill" title="Model weight: {score:.3f}">
  <span class="pill-k">{word}</span>
  <span class="pill-s {pill_cls}">{safe_label}</span>
  <span class="pill-v">{score:.3f}</span>
</div>"""
                )

            st.markdown(
                f"""<div class="report">
  <div class="report-head">
    <div class="verdict">
      <div>
        <div class="verdict-title">{'❌' if pred == 1 else '✅'} {verdict_title}</div>
        <div class="verdict-sub">CONFIDENCE · {confidence:.2f}%</div>
      </div>
    </div>
    <div class="badge {badge_class}">{verdict_badge}</div>
  </div>

  <div class="report-grid">
    <div>
      <div class="report-h">Top indicators</div>
      <div class="pill-row">
        {''.join(pills_html) if pills_html else '<span style="color: rgba(232,240,254,0.62); font-size: 13px;">No strong indicators found for this text.</span>'}
      </div>
    </div>
  </div>
</div>""",
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="reset-button-container">', unsafe_allow_html=True)
            def reset_defaults():
                st.session_state.job_text = ""
            st.button("↺ Reset to Defaults", on_click=reset_defaults, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hiw">
    <div class="hiw-eyebrow">THE PROCESS</div>
    <div class="section-h">How It Works</div>
    <div class="section-sub">Three steps. Zero guesswork.</div>
    <div class="hiw-grid">
        <div class="hiw-card">
            <div class="hiw-icon">📋</div>
            <div class="hiw-t">Paste the Posting</div>
            <div class="hiw-d">Copy the full job description — title, responsibilities,
            requirements, and contact info — into the analysis portal.</div>
        </div>
        <div class="hiw-card">
            <div class="hiw-icon">⚡</div>
            <div class="hiw-t">Engine Scans Instantly</div>
            <div class="hiw-d">Cross-references fraud signals, linguistic patterns,
            salary anomalies, and contact-method checks in real time.</div>
        </div>
        <div class="hiw-card">
            <div class="hiw-icon">🛡️</div>
            <div class="hiw-t">Get Your Report</div>
            <div class="hiw-d">Receive a trust score, verdict classification, and a
            breakdown of every signal — good or bad — detected in the text.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MINOR PROJECT CARD ────────────────────────────────────────────────────────
st.markdown("""
<div class="mp-section">
    <div class="mp-card">
        <div class="mp-left">
            <div class="mp-eyebrow">MINOR PROJECT · SEMESTER II · 2026</div>
            <div class="mp-title">Fake Job Detection System</div>
            <div class="mp-desc">
                Developed as part of B.Tech (CSE – AI &amp; ML, Section F) at K.R. Mangalam University,
                Gurugram. The project tackles a real-world problem: millions of fraudulent job postings
                targeting students and freshers, causing financial loss, identity theft, and psychological
                distress. Our system provides a free, accessible verification tool that operates in real time.
            </div>
            <div class="mp-tags">
                <span class="mp-tag">Machine Learning</span>
                <span class="mp-tag">NLP</span>
                <span class="mp-tag">Fraud Detection</span>
                <span class="mp-tag">Logistic Regression</span>
                <span class="mp-tag">TF-IDF</span>
                <span class="mp-tag">Python &amp; Streamlit</span>
                <span class="mp-tag">Kaggle EMSCAD</span>
            </div>
            <div class="mp-meta">
                Supervised by Atisha Dahiya<br>
                School of Engineering &amp; Technology<br>
                Projexa Team ID: 26E1022 &nbsp;·&nbsp; January 2026
            </div>
        </div>
        <div class="mp-right">
            <div class="mp-team-label">OUR TEAM</div>
            <div class="mp-members">
                <div class="mp-member">
                    <div class="mp-avatar">NJ</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">Naman Joshi</div>
                        <div class="mp-member-id">2501730415</div>
                        <div class="mp-member-role">Data Processing &amp; Vectorization</div>
                    </div>
                </div>
                <div class="mp-member">
                    <div class="mp-avatar">VR</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">Vedansh Rawat</div>
                        <div class="mp-member-id">2501730364</div>
                        <div class="mp-member-role">Main ML Engineer</div>
                    </div>
                </div>
                <div class="mp-member">
                    <div class="mp-avatar">DJ</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">Dhruv Jaiswal</div>
                        <div class="mp-member-id">2501730362</div>
                        <div class="mp-member-role">Streamlit Frontend Developer</div>
                    </div>
                </div>
                <div class="mp-member">
                    <div class="mp-avatar">PY</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">Pranav Yadav</div>
                        <div class="mp-member-id">2501730390</div>
                        <div class="mp-member-role">Backend &amp; Logic Integration</div>
                    </div>
                </div>
                <div class="mp-member">
                    <div class="mp-avatar">VA</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">V.R. Adikrishna</div>
                        <div class="mp-member-id">2501730397</div>
                        <div class="mp-member-role">Documentation &amp; Data Handling</div>
                    </div>
                </div>
                <div class="mp-member">
                    <div class="mp-avatar">VS</div>
                    <div class="mp-member-info">
                        <div class="mp-member-name">Vansh Sihag</div>
                        <div class="mp-member-id">2501730387</div>
                        <div class="mp-member-role">Debugging &amp; Deployment Engineer</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="foot-logo">DATAMINDS</div>
    <div class="foot-copy">© 2026 DATAMINDS. ALL RIGHTS RESERVED.</div>
    <div class="foot-links">
        <span>Privacy</span><span>Terms</span><span>Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)
