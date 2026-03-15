import streamlit as st
import requests
from datetime import datetime, date
from collections import Counter

st.set_page_config(
    page_title="InternFlow AI – Tracker",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = "http://127.0.0.1:8000"
STATUSES = ["Applied", "Interview", "Offer", "Rejected"]

STATUS_STYLE = {
    "Applied":   ("rgba(168,85,247,0.12)",  "rgba(168,85,247,0.4)",  "#c084fc"),
    "Interview": ("rgba(245,158,11,0.12)",  "rgba(245,158,11,0.45)", "#fcd34d"),
    "Offer":     ("rgba(16,185,129,0.12)",  "rgba(16,185,129,0.45)", "#6ee7b7"),
    "Rejected":  ("rgba(239,68,68,0.10)",   "rgba(239,68,68,0.35)",  "#fca5a5"),
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');"
    "#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}"
    "[data-testid='collapsedControl']{display:none;}"
    "* {box-sizing:border-box;}"
    ":root{--lav200:#e9d5ff;--lav300:#d8b4fe;--lav400:#c084fc;--lav500:#a855f7;--lav600:#9333ea;--bg:#08080f;--bg2:#0e0e1a;--bg3:#131325;--txt:#f1f0f8;--muted:#7c7a9a;--bdr:rgba(168,85,247,0.18);}"
    ".stApp{background:#08080f !important;font-family:'Outfit',sans-serif;color:#f1f0f8;}"
    ".block-container{padding:32px 48px 80px !important;max-width:1200px !important;margin:0 auto !important;}"
    # Inputs + selects
    ".stTextInput > div > div > input{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;font-family:'Outfit',sans-serif !important;font-size:15px !important;}"
    ".stTextInput label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;}"
    ".stSelectbox > div > div{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;}"
    ".stSelectbox label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;}"
    ".stTextArea > div > textarea{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;}"
    ".stTextArea label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;}"
    # Buttons
    ".stButton > button{background:linear-gradient(135deg,#7c3aed,#6d28d9) !important;color:#fff !important;border:none !important;border-radius:10px !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;font-weight:600 !important;padding:9px 20px !important;height:auto !important;transition:opacity 0.2s !important;}"
    ".stButton > button:hover{opacity:0.82 !important;}"
    ".stButton > button[kind='secondary']{background:rgba(168,85,247,0.08) !important;border:1px solid rgba(168,85,247,0.25) !important;color:#c084fc !important;}"
    # Expander
    ".streamlit-expanderHeader{background:rgba(255,255,255,0.02) !important;border:1px solid rgba(168,85,247,0.18) !important;border-radius:12px !important;color:#c084fc !important;font-family:'Outfit',sans-serif !important;font-size:15px !important;}"
    # Nav
    ".nav-logo{font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;background:linear-gradient(135deg,#c4b5fd,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}"
    # Page header
    ".page-hd{font-family:'Instrument Serif',serif;font-size:clamp(32px,4vw,48px);font-weight:400;color:var(--txt);letter-spacing:-1px;margin:0 0 6px;}"
    ".page-hd em{font-style:italic;color:var(--lav300);}"
    ".page-sub{font-size:16px;color:var(--muted);font-weight:300;margin:0;}"
    # Divider
    ".div{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.22),transparent);margin:20px 0;}"
    # Section eyebrow
    ".eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;color:var(--lav400);margin-bottom:16px;display:flex;align-items:center;gap:10px;}"
    ".eyebrow::before{content:'';display:inline-block;width:20px;height:1px;background:var(--lav500);}"
    # Analytics cards
    ".stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;}"
    ".stat-card{background:var(--bg2);border:1px solid var(--bdr);border-radius:16px;padding:28px 24px;position:relative;overflow:hidden;}"
    ".stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.35),transparent);}"
    ".stat-num{font-family:'Instrument Serif',serif;font-size:48px;color:var(--lav200);line-height:1;margin-bottom:6px;}"
    ".stat-lbl{font-size:14px;color:var(--muted);font-weight:400;line-height:1.5;}"
    ".stat-lbl strong{color:var(--lav300);font-weight:600;display:block;}"
    # Funnel bar
    ".funnel-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:32px;}"
    ".funnel-seg{border-radius:12px;padding:16px 20px;}"
    ".funnel-label{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;}"
    ".funnel-count{font-family:'Instrument Serif',serif;font-size:36px;line-height:1;}"
    ".funnel-pct{font-size:12px;margin-top:4px;opacity:0.7;}"
    # Table header
    ".tbl-hdr{display:grid;grid-template-columns:2.5fr 1.8fr 1.8fr 1.2fr 1fr 0.8fr;gap:12px;padding:10px 20px;background:var(--bg3);border:1px solid var(--bdr);border-radius:10px;margin-bottom:8px;}"
    ".tbl-hdr-cell{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:var(--muted);}"
    # App row
    ".app-row{background:rgba(255,255,255,0.025);border:1px solid rgba(168,85,247,0.15);border-radius:12px;padding:16px 20px;margin-bottom:8px;position:relative;overflow:hidden;transition:border-color 0.2s;}"
    ".app-row:hover{border-color:rgba(168,85,247,0.35);}"
    ".app-row::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.25),transparent);}"
    ".app-title{font-size:15px;font-weight:700;color:var(--txt);margin-bottom:2px;}"
    ".app-company{font-size:13px;color:var(--lav400);font-weight:500;}"
    ".app-meta{font-family:'JetBrains Mono',monospace;font-size:11px;color:#4b5563;}"
    ".app-resume{font-size:13px;color:#7c7a9a;font-style:italic;}"
    ".status-pill{display:inline-block;padding:4px 12px;border-radius:100px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;border:1px solid;}"
    # Best resume highlight
    ".best-card{background:linear-gradient(135deg,rgba(168,85,247,0.08),rgba(124,58,237,0.04));border:1px solid rgba(168,85,247,0.3);border-radius:16px;padding:28px 32px;margin-bottom:8px;}"
    ".best-title{font-family:'Instrument Serif',serif;font-size:28px;color:var(--lav200);margin-bottom:4px;}"
    ".best-sub{font-size:14px;color:var(--muted);}"
    # Empty state
    ".empty{background:var(--bg2);border:1px dashed rgba(168,85,247,0.2);border-radius:16px;padding:60px;text-align:center;}"
    ".empty-ico{font-size:40px;margin-bottom:16px;}"
    ".empty-title{font-family:'Outfit',sans-serif;font-size:20px;font-weight:600;color:var(--txt);margin-bottom:8px;}"
    ".empty-sub{font-size:15px;color:var(--muted);}"
    "</style>",
    unsafe_allow_html=True
)

# ── Helpers ───────────────────────────────────────────────────────────────────
def status_pill(status: str) -> str:
    bg, bdr, txt = STATUS_STYLE.get(status, STATUS_STYLE["Applied"])
    return f"<span class='status-pill' style='background:{bg};border-color:{bdr};color:{txt}'>{status}</span>"

def fetch_apps():
    try:
        r = requests.get(f"{API}/applications", timeout=5)
        return r.json() if isinstance(r.json(), list) else []
    except Exception:
        return None

def update_status(app_id: str, new_status: str):
    try:
        requests.put(f"{API}/applications/{app_id}/status", params={"status": new_status}, timeout=5)
        return True
    except Exception:
        return False

def delete_app(app_id: str):
    try:
        requests.delete(f"{API}/applications/{app_id}", timeout=5)
        return True
    except Exception:
        return False

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
with c1:
    st.markdown("<div class='nav-logo'>🚀 InternFlow AI</div>", unsafe_allow_html=True)
with c2:
    if st.button("📝 Profile", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")
with c3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with c4:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.switch_page("pages/4_agent.py")
with c5:
    if st.button("📋 Tracker", use_container_width=True, type="primary"):
        pass

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(
    "<div class='page-hd'>Application <em>Tracker</em></div>"
    "<p class='page-sub'>Every application, every status, every resume version — in one place.</p>",
    unsafe_allow_html=True
)
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Fetch ─────────────────────────────────────────────────────────────────────
apps = fetch_apps()

if apps is None:
    st.error("❌ Cannot connect to backend. Run: `cd backend && uvicorn main:app --reload`")
    st.stop()

# ══════════════════════════════════════════════════════════
# ANALYTICS SECTION
# ══════════════════════════════════════════════════════════
st.markdown("<div class='eyebrow'>Analytics</div>", unsafe_allow_html=True)

total        = len(apps)
status_counts = Counter(a.get("status", "Applied") for a in apps)
n_applied    = status_counts.get("Applied", 0)
n_interview  = status_counts.get("Interview", 0)
n_offer      = status_counts.get("Offer", 0)
n_rejected   = status_counts.get("Rejected", 0)

# Success rate = offers / total (or interviews / total if no offers yet)
if total == 0:
    success_rate = 0
    interview_rate = 0
elif n_offer > 0:
    success_rate = round(n_offer / total * 100)
    interview_rate = round(n_interview / total * 100)
else:
    success_rate = 0
    interview_rate = round(n_interview / total * 100) if total > 0 else 0

# Best performing resume
resume_counter = Counter()
resume_wins    = Counter()
for a in apps:
    r = a.get("resume_used") or "Base Resume"
    resume_counter[r] += 1
    if a.get("status") in ("Interview", "Offer"):
        resume_wins[r] += 1

best_resume = "—"
best_resume_rate = 0
if resume_wins:
    best_resume = resume_wins.most_common(1)[0][0]
    best_resume_rate = round(resume_wins[best_resume] / max(resume_counter[best_resume], 1) * 100)
elif resume_counter:
    best_resume = resume_counter.most_common(1)[0][0]

# ── Top stats ─────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='stat-row'>"
    f"<div class='stat-card'>"
    f"<div class='stat-num'>{total}</div>"
    f"<div class='stat-lbl'><strong>Total Applications</strong>tracked this session</div>"
    f"</div>"
    f"<div class='stat-card'>"
    f"<div class='stat-num'>{interview_rate}%</div>"
    f"<div class='stat-lbl'><strong>Interview Rate</strong>applications → interviews</div>"
    f"</div>"
    f"<div class='stat-card'>"
    f"<div class='stat-num'>{success_rate}%</div>"
    f"<div class='stat-lbl'><strong>Offer Rate</strong>applications → offers</div>"
    f"</div>"
    f"<div class='stat-card'>"
    f"<div class='stat-num'>{n_offer}</div>"
    f"<div class='stat-lbl'><strong>Offers</strong>received so far</div>"
    f"</div>"
    "</div>",
    unsafe_allow_html=True
)

# ── Funnel ────────────────────────────────────────────────────────────────────
funnel_data = [
    ("Applied",   n_applied,   STATUS_STYLE["Applied"]),
    ("Interview", n_interview, STATUS_STYLE["Interview"]),
    ("Offer",     n_offer,     STATUS_STYLE["Offer"]),
    ("Rejected",  n_rejected,  STATUS_STYLE["Rejected"]),
]
funnel_html = "<div class='funnel-row'>"
for label, count, (bg, bdr, txt) in funnel_data:
    pct = f"{round(count / total * 100)}%" if total > 0 else "—"
    funnel_html += (
        f"<div class='funnel-seg' style='background:{bg};border:1px solid {bdr};'>"
        f"<div class='funnel-label' style='color:{txt}'>{label}</div>"
        f"<div class='funnel-count' style='color:{txt}'>{count}</div>"
        f"<div class='funnel-pct' style='color:{txt}'>{pct} of total</div>"
        f"</div>"
    )
funnel_html += "</div>"
st.markdown(funnel_html, unsafe_allow_html=True)

# ── Best resume ───────────────────────────────────────────────────────────────
if best_resume != "—":
    st.markdown(
        f"<div class='best-card'>"
        f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;color:#a855f7;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:10px'>⭐ Best Performing Resume</div>"
        f"<div class='best-title'>{best_resume}</div>"
        f"<div class='best-sub'>{best_resume_rate}% interview/offer rate &nbsp;·&nbsp; used {resume_counter[best_resume]} time{'s' if resume_counter[best_resume] != 1 else ''}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# APPLICATIONS TABLE
# ══════════════════════════════════════════════════════════
header_col, add_col = st.columns([4, 1])
with header_col:
    st.markdown("<div class='eyebrow'>Applications</div>", unsafe_allow_html=True)
with add_col:
    show_add = st.button("＋ Add Manual", use_container_width=True, type="primary")

# ── Manual add form ───────────────────────────────────────────────────────────
if show_add:
    with st.expander("➕ Add Application Manually", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            m_title   = st.text_input("Job Title", placeholder="e.g. ML Engineering Intern")
            m_company = st.text_input("Company", placeholder="e.g. NVIDIA")
            m_resume  = st.text_input("Resume Used", placeholder="e.g. ML_Resume_v2")
        with f2:
            m_loc     = st.text_input("Location", placeholder="e.g. Remote")
            m_url     = st.text_input("Job URL", placeholder="https://...")
            m_status  = st.selectbox("Status", STATUSES)
        m_notes = st.text_area("Notes", placeholder="Anything worth remembering about this role...", height=80)
        if st.button("Save Application", type="primary"):
            if m_title and m_company:
                try:
                    requests.post(f"{API}/applications", json={
                        "job_id": f"manual-{datetime.now().timestamp()}",
                        "company": m_company,
                        "job_title": m_title,
                        "location": m_loc,
                        "resume_used": m_resume or "Base Resume",
                        "status": m_status,
                        "notes": m_notes,
                        "url": m_url,
                    }, timeout=5)
                    st.success("✅ Application saved!")
                    st.rerun()
                except Exception:
                    st.error("Could not save — is the backend running?")
            else:
                st.warning("Job Title and Company are required.")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Filter row ────────────────────────────────────────────────────────────────
if apps:
    fil1, fil2, fil3 = st.columns([2, 2, 2])
    with fil1:
        filter_status = st.selectbox("Filter by status", ["All"] + STATUSES, key="filter_status")
    with fil2:
        filter_search = st.text_input("Search company or title", placeholder="e.g. Google, ML...")
    with fil3:
        sort_by = st.selectbox("Sort by", ["Date (newest)", "Date (oldest)", "Company A–Z", "Status"])

    # Apply filters
    display_apps = apps[:]
    if filter_status != "All":
        display_apps = [a for a in display_apps if a.get("status") == filter_status]
    if filter_search:
        q = filter_search.lower()
        display_apps = [a for a in display_apps if q in a.get("company","").lower() or q in a.get("job_title","").lower()]
    # Sort
    if sort_by == "Date (newest)":
        display_apps = sorted(display_apps, key=lambda a: a.get("applied_date",""), reverse=True)
    elif sort_by == "Date (oldest)":
        display_apps = sorted(display_apps, key=lambda a: a.get("applied_date",""))
    elif sort_by == "Company A–Z":
        display_apps = sorted(display_apps, key=lambda a: a.get("company","").lower())
    elif sort_by == "Status":
        order = {s: i for i, s in enumerate(STATUSES)}
        display_apps = sorted(display_apps, key=lambda a: order.get(a.get("status","Applied"), 99))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Table header ──────────────────────────────────────────────────────────
    st.markdown(
        "<div class='tbl-hdr'>"
        "<div class='tbl-hdr-cell'>Job Title</div>"
        "<div class='tbl-hdr-cell'>Company</div>"
        "<div class='tbl-hdr-cell'>Resume Used</div>"
        "<div class='tbl-hdr-cell'>Status</div>"
        "<div class='tbl-hdr-cell'>Date</div>"
        "<div class='tbl-hdr-cell'>Actions</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if not display_apps:
        st.markdown(
            "<div class='empty'>"
            "<div class='empty-ico'>🔍</div>"
            "<div class='empty-title'>No applications match your filter</div>"
            "<div class='empty-sub'>Try clearing the filters above</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        for app in display_apps:
            app_id      = app.get("id", "")
            job_title   = app.get("job_title", "—")
            company     = app.get("company", "—")
            resume_used = app.get("resume_used") or "Base Resume"
            status      = app.get("status", "Applied")
            applied_date= app.get("applied_date", "—")
            notes       = app.get("notes", "")
            url         = app.get("url", "")

            bg, bdr, txt = STATUS_STYLE.get(status, STATUS_STYLE["Applied"])

            # Pre-compute conditional HTML (no backslashes inside f-strings — Python <3.12)
            url_link   = f"&nbsp;<a href='{url}' target='_blank' style='color:#7c3aed;font-size:11px;text-decoration:none'>&#x2197;</a>" if url else ""
            notes_html = f"<div style='font-size:12px;color:#4b5563;margin-top:2px'>{notes}</div>" if notes else ""

            # Card HTML
            card_html = (
                "<div class='app-row'>"
                "<div style='display:grid;grid-template-columns:2.5fr 1.8fr 1.8fr 1.2fr 1fr;gap:12px;align-items:center'>"
                "<div>"
                f"<div class='app-title'>{job_title}{url_link}</div>"
                f"{notes_html}"
                "</div>"
                f"<div class='app-company'>{company}</div>"
                f"<div class='app-resume'>{resume_used}</div>"
                f"<div>{status_pill(status)}</div>"
                f"<div class='app-meta'>{applied_date}</div>"
                "</div>"
                "</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

            # Inline action row
            a1, a2, a3, a4 = st.columns([2, 2, 1, 5])
            with a1:
                new_status = st.selectbox(
                    "Update status",
                    STATUSES,
                    index=STATUSES.index(status) if status in STATUSES else 0,
                    key=f"sel_{app_id}",
                    label_visibility="collapsed"
                )
            with a2:
                if st.button("Update", key=f"upd_{app_id}", use_container_width=True):
                    if update_status(app_id, new_status):
                        st.rerun()
                    else:
                        st.error("Update failed.")
            with a3:
                if st.button("🗑", key=f"del_{app_id}", use_container_width=True):
                    if delete_app(app_id):
                        st.rerun()
                    else:
                        st.error("Delete failed.")

            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

else:
    # Empty state
    st.markdown(
        "<div class='empty'>"
        "<div class='empty-ico'>📭</div>"
        "<div class='empty-title'>No applications yet</div>"
        "<div class='empty-sub'>Go to the Jobs page, hit <strong style='color:#c084fc'>📋 Track</strong> on any listing,<br>or add one manually above.</div>"
        "</div>",
        unsafe_allow_html=True
    )
