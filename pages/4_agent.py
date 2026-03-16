import streamlit as st
import requests
import os
from fpdf import FPDF
import tempfile
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="InternFlow AI – Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = "http://127.0.0.1:8000"
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}
* {box-sizing:border-box;}

:root {
  --black: #030305; --card: #0e0e1c; --card2: #12121e;
  --border: rgba(118,185,0,0.15); --green: #76B900;
  --green-dim: rgba(118,185,0,0.08); --white: #f0efe8; --muted: #6b6b80;
  --red: #ff5555; --red-dim: rgba(255,85,85,0.08);
  --font-display: 'Syne', sans-serif; --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}

.stApp { background: var(--black) !important; font-family: var(--font-body); color: var(--white); }
.block-container { padding: 0 !important; max-width: 100% !important; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 48px; }
.wrap-sm { max-width: 860px; margin: 0 auto; padding: 0 48px; }

.nav { padding: 24px 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 40px; }
.nav-logo { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--white); }
.nav-logo span { color: var(--green); }

.page-h { font-family: var(--font-display); font-size: clamp(28px,3vw,44px); font-weight: 800; letter-spacing:-1px; color: var(--white); margin-bottom: 4px; }
.page-h em { font-style: normal; color: var(--green); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; margin-bottom: 32px; }

/* Job banner */
.job-banner {
  background: var(--card);
  border: 1px solid rgba(118,185,0,0.25);
  border-left: 4px solid var(--green);
  border-radius: 14px;
  padding: 20px 24px;
  margin-bottom: 28px;
}
.jb-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.jb-company { font-size: 14px; color: var(--green); font-weight: 500; margin-bottom: 6px; }
.jb-desc { font-size: 13px; color: var(--muted); line-height: 1.6; }

/* Section headers */
.sec-label { font-family: var(--font-mono); font-size: 10px; color: var(--green); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px; }
.sec-title { font-family: var(--font-display); font-size: 16px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.sec-desc { font-size: 13px; color: var(--muted); margin-bottom: 16px; }

/* Result cards */
.result-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
}
.result-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(118,185,0,0.3), transparent);
}

/* Score ring */
.score-wrap { text-align: center; padding: 20px; }
.score-ring {
  width: 110px; height: 110px;
  border-radius: 50%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  margin: 0 auto 12px;
  border: 3px solid;
}
.score-num { font-family: var(--font-display); font-size: 36px; font-weight: 800; line-height: 1; }
.score-lbl { font-family: var(--font-mono); font-size: 11px; margin-top: 2px; }
.score-verdict { font-size: 13px; font-weight: 500; margin-top: 8px; }

/* Keyword pills */
.kw-present {
  display: inline-block; margin: 3px;
  background: rgba(118,185,0,0.12); border: 1px solid rgba(118,185,0,0.3);
  color: var(--green); padding: 4px 12px; border-radius: 100px;
  font-size: 12px; font-family: var(--font-mono);
}
.kw-missing {
  display: inline-block; margin: 3px;
  background: var(--red-dim); border: 1px solid rgba(255,85,85,0.3);
  color: var(--red); padding: 4px 12px; border-radius: 100px;
  font-size: 12px; font-family: var(--font-mono);
}

/* Project card */
.proj-card {
  background: var(--card2);
  border: 1px solid rgba(118,185,0,0.2);
  border-left: 3px solid var(--green);
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 10px;
}
.proj-num { font-family: var(--font-mono); font-size: 10px; color: rgba(118,185,0,0.5); margin-bottom: 6px; letter-spacing: 0.1em; }
.proj-name { font-family: var(--font-display); font-size: 16px; font-weight: 700; color: var(--white); margin-bottom: 6px; }
.proj-desc { font-size: 13px; color: var(--muted); line-height: 1.6; }

/* Resume text */
.resume-box {
  background: #07070f;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: #c8c8d8;
  line-height: 1.8;
  white-space: pre-wrap;
  max-height: 500px;
  overflow-y: auto;
}

/* Processing card */
.processing-card {
  background: var(--card);
  border: 1px solid rgba(118,185,0,0.3);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  margin: 24px 0;
}
.processing-title { font-family: var(--font-display); font-size: 22px; font-weight: 700; color: var(--white); margin-bottom: 8px; }
.processing-sub { font-size: 14px; color: var(--muted); margin-bottom: 24px; }
.step-item { font-size: 13px; color: var(--muted); padding: 6px 0; display: flex; align-items: center; gap: 10px; justify-content: center; }
.step-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(118,185,0,0.3); flex-shrink: 0; }
.step-dot-active { background: var(--green); box-shadow: 0 0 8px rgba(118,185,0,0.5); }

/* Buttons */
.stButton > button {
  background: var(--green) !important; color: #000 !important;
  border: none !important; border-radius: 8px !important;
  font-family: var(--font-display) !important; font-size: 14px !important;
  font-weight: 700 !important; padding: 10px 24px !important;
  height: auto !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
  background: transparent !important; color: var(--green) !important;
  border: 1px solid rgba(118,185,0,0.3) !important;
}
.stTextArea > div > div > textarea {
  background: #0a0a14 !important; border: 1px solid rgba(118,185,0,0.2) !important;
  border-radius: 10px !important; color: var(--white) !important;
  font-family: var(--font-mono) !important; font-size: 13px !important;
}
label { color: var(--muted) !important; font-size: 13px !important; }
.stTabs [data-baseweb="tab"] { font-family: var(--font-body) !important; color: var(--muted) !important; font-size: 14px !important; }
.stTabs [aria-selected="true"] { color: var(--green) !important; border-bottom-color: var(--green) !important; }
.divline { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(118,185,0,0.15), transparent); margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Session ───────────────────────────────────────────────────────────────────
if "agent_result" not in st.session_state: st.session_state.agent_result = None
if "latex_code"   not in st.session_state: st.session_state.latex_code   = ""

profile      = st.session_state.get("profile", {})
selected_job = st.session_state.get("selected_job", None)
projects     = st.session_state.get("projects", [])
resume_text  = st.session_state.get("resume_text", "")

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("<div class='wrap'>", unsafe_allow_html=True)
n1, n2, n3, n4, n5 = st.columns([3, 1, 1, 1, 1])
with n1:
    st.markdown("<div class='nav-logo'>Intern<span>Flow</span> AI</div>", unsafe_allow_html=True)
with n2:
    if st.button("📝 Profile",  use_container_width=True): st.switch_page("pages/2_onboarding.py")
with n3:
    if st.button("💼 Jobs",     use_container_width=True): st.switch_page("pages/3_jobs.py")
with n4:
    if st.button("🤖 Agent",    type="primary", use_container_width=True): pass
with n5:
    if st.button("📂 Arsenal",  use_container_width=True): st.switch_page("pages/5_resume_arsenal.py")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='wrap'>
  <div class='page-h'>Nemotron <em>Agent</em></div>
  <p class='page-sub'>3 agents · JD Diagnostics → Project Selection → Resume Rewrite → LaTeX PDF</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='wrap'>", unsafe_allow_html=True)

# ── Job Banner ────────────────────────────────────────────────────────────────
if selected_job:
    locs = ", ".join(selected_job.get("locations",[]))
    desc = (selected_job.get("description","") or "")[:240]
    st.markdown(f"""
    <div class='job-banner'>
      <div class='jb-title'>{selected_job.get("title","")}</div>
      <div class='jb-company'>{selected_job.get("company","")} · 📍 {locs}</div>
      <div class='jb-desc'>{desc}{"..." if len(selected_job.get("description","")) > 240 else ""}</div>
    </div>
    """, unsafe_allow_html=True)
    default_jd = selected_job.get("description","")
else:
    default_jd = ""
    st.info("💡 No job selected. Go to the Jobs page and click 'Analyse with AI' — or paste a JD below.")

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='sec-label'>Job Description</div>", unsafe_allow_html=True)
    jd_text = st.text_area("jd", height=220, value=default_jd,
        placeholder="Paste the full job description here...", label_visibility="collapsed", key="jd_input")
with col2:
    st.markdown("<div class='sec-label'>Your Resume</div>", unsafe_allow_html=True)
    resume_input = st.text_area("resume", height=220, value=resume_text,
        placeholder="Your resume auto-loads from profile. Or paste here...", label_visibility="collapsed", key="resume_input")

# Projects status
if projects:
    st.markdown(f"""
    <div style='background:rgba(118,185,0,0.06);border:1px solid rgba(118,185,0,0.2);
    border-radius:10px;padding:10px 16px;font-size:13px;color:var(--green);margin:8px 0'>
    ✅ <b>{len(projects)} projects</b> loaded from your profile:
    <span style='color:var(--muted)'>{", ".join(p.get("name","") for p in projects[:5])}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='background:rgba(255,85,85,0.05);border:1px solid rgba(255,85,85,0.2);
    border-radius:10px;padding:10px 16px;font-size:13px;color:#ff8888;margin:8px 0'>
    ⚠️ No projects loaded. <a href='pages/2_onboarding.py' style='color:#ff8888'>Add them in Profile →</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divline'>", unsafe_allow_html=True)

# ── Run Button ────────────────────────────────────────────────────────────────
rc1, rc2, rc3 = st.columns([1, 2, 1])
with rc2:
    st.markdown("""
    <div style='text-align:center;font-size:13px;color:var(--muted);margin-bottom:10px'>
    Agent 1: JD Diagnostics → Agent 2: Project Selection → Agent 3: Resume Rewrite
    </div>
    """, unsafe_allow_html=True)
    run_btn = st.button("⚡ Run Nemotron Agent", type="primary", use_container_width=True)

if run_btn:
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
    elif not resume_input.strip():
        st.warning("Please add your resume text.")
    elif not projects:
        st.warning("Please add at least one project in your profile.")
    else:
        prog = st.empty()
        with prog.container():
            st.markdown("""
            <div class='processing-card'>
              <div class='processing-title'>🧠 Nemotron is thinking…</div>
              <div class='processing-sub'>Running LangGraph pipeline — 15–60 seconds</div>
              <div style='max-width:280px;margin:0 auto'>
                <div class='step-item'><div class='step-dot step-dot-active'></div>Agent 1 · Extracting JD keywords & scoring gaps</div>
                <div class='step-item'><div class='step-dot'></div>Agent 2 · Selecting best-fit projects from your portfolio</div>
                <div class='step-item'><div class='step-dot'></div>Agent 3 · Rewriting resume to match JD</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        try:
            payload = {
                "job_description": jd_text,
                "resume_text": resume_input,
                "projects": [{"name": p["name"], "description": p.get("description","")} for p in projects]
            }
            resp = requests.post(f"{API}/agent/analyze", json=payload, timeout=600)
            prog.empty()

            if resp.status_code != 200:
                st.error(f"Agent failed: HTTP {resp.status_code}")
                st.code(resp.text)
                st.stop()

            raw = resp.json()
            diag = raw.get("diagnostic", {}) or {}
            present_kw  = raw.get("present_keywords",[]) or diag.get("present_keywords",[]) or []
            missing_kw  = raw.get("missing_keywords",[]) or diag.get("missing_keywords",[]) or []
            jd_kw       = raw.get("jd_keywords",[])       or diag.get("jd_keywords",[])       or []
            match_score = int(raw.get("match_score",0) or diag.get("match_score",0) or 0)
            if jd_kw and match_score == 0:
                match_score = int(round(100 * len(present_kw) / max(len(jd_kw),1)))
            sel_projects   = raw.get("selected_projects",[]) or []
            tailored       = raw.get("tailored_resume","") or ""

            st.session_state.agent_result = {
                "match_score":    match_score,
                "present_kw":     present_kw,
                "missing_kw":     missing_kw,
                "sel_projects":   sel_projects,
                "tailored":       tailored,
                "original_resume": resume_input,
            }
            st.success("✅ Analysis complete! Scroll down to see results.")
            # Save to arsenal
            if tailored and selected_job:
                try:
                    requests.post(f"{API}/resumes/company", json={
                        "company": selected_job.get("company",""),
                        "job_title": selected_job.get("title",""),
                        "tailored_content": tailored,
                        "base_resume_name": "default"
                    }, timeout=5)
                except Exception:
                    pass

        except requests.exceptions.ConnectionError:
            prog.empty()
            st.error("❌ Backend not running. Run: `cd backend && python -m uvicorn main:app --reload`")
        except Exception as ex:
            prog.empty()
            st.error(f"Agent error: {ex}")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.agent_result:
    r            = st.session_state.agent_result
    match_score  = r.get("match_score",0)
    present_kw   = r.get("present_kw",[])
    missing_kw   = r.get("missing_kw",[])
    sel_projects = r.get("sel_projects",[])
    tailored     = r.get("tailored","")

    st.markdown("<hr class='divline'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:var(--font-display);font-size:22px;font-weight:800;color:var(--white);margin-bottom:20px'>📊 Results</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 ATS Score", "🔑 Keywords", "🗂 Projects", "📄 Resume"])

    # ── TAB 1: ATS Score ──────────────────────────────────────────────────────
    with tab1:
        if match_score >= 70:
            ring_color = "#76B900"; ring_bg = "rgba(118,185,0,0.12)"; verdict = "🟢 Strong match — ready to apply!"
        elif match_score >= 50:
            ring_color = "#fcd34d"; ring_bg = "rgba(252,211,77,0.1)";  verdict = "🟡 Decent match — a few tweaks needed."
        else:
            ring_color = "#ff5555"; ring_bg = "rgba(255,85,85,0.08)";  verdict = "🔴 Significant gaps — tailoring recommended."

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class='result-card score-wrap'>
              <div style='font-family:var(--font-mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>ATS Match Score</div>
              <div class='score-ring' style='border-color:{ring_color};background:{ring_bg}'>
                <div class='score-num' style='color:{ring_color}'>{match_score}</div>
                <div class='score-lbl' style='color:{ring_color}'>/ 100</div>
              </div>
              <div class='score-verdict' style='color:{ring_color}'>{verdict}</div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            total = len(present_kw) + len(missing_kw)
            pct   = int(len(present_kw)/max(total,1)*100)
            st.markdown(f"""
            <div class='result-card score-wrap'>
              <div style='font-family:var(--font-mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>Keyword Coverage</div>
              <div class='score-ring' style='border-color:{ring_color};background:{ring_bg}'>
                <div class='score-num' style='color:{ring_color}'>{pct}%</div>
                <div class='score-lbl' style='color:{ring_color}'>{len(present_kw)}/{total}</div>
              </div>
              <div style='font-size:13px;color:var(--muted);margin-top:8px'>{len(present_kw)} of {total} keywords found</div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class='result-card score-wrap'>
              <div style='font-family:var(--font-mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>Projects Selected</div>
              <div class='score-ring' style='border-color:var(--green);background:var(--green-dim)'>
                <div class='score-num' style='color:var(--green)'>{len(sel_projects)}</div>
                <div class='score-lbl' style='color:var(--green)'>/ 3</div>
              </div>
              <div style='font-size:13px;color:var(--muted);margin-top:8px'>Best-fit projects picked by Nemotron</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 2: Keywords ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        kb1, kb2 = st.columns(2)
        with kb1:
            st.markdown(f"""
            <div class='result-card'>
              <div style='color:var(--green);font-family:var(--font-mono);font-size:11px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:12px'>✅ Keywords You Have ({len(present_kw)})</div>
              <div>{"".join([f"<span class='kw-present'>✓ {k}</span>" for k in present_kw]) or "<span style='color:var(--muted);font-size:13px'>None detected</span>"}</div>
            </div>
            """, unsafe_allow_html=True)
        with kb2:
            st.markdown(f"""
            <div class='result-card'>
              <div style='color:var(--red);font-family:var(--font-mono);font-size:11px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:12px'>❌ Keywords Missing ({len(missing_kw)})</div>
              <div>{"".join([f"<span class='kw-missing'>✗ {k}</span>" for k in missing_kw]) or "<span style='color:var(--muted);font-size:13px'>None — great match!</span>"}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 3: Projects ───────────────────────────────────────────────────────
    with tab3:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if not sel_projects:
            st.info("No projects were selected. Make sure you added projects in your profile.")
        else:
            st.markdown(f"<div style='font-size:13px;color:var(--muted);margin-bottom:16px'>Nemotron selected these <b style='color:var(--white)'>{len(sel_projects)} projects</b> as the best fit for this role.</div>", unsafe_allow_html=True)
            for i, proj in enumerate(sel_projects):
                pname = proj.get("name","Project " + str(i+1))
                pdesc = proj.get("rewritten_description") or proj.get("description","")
                st.markdown(f"""
                <div class='proj-card'>
                  <div class='proj-num'>PROJECT {i+1} OF {len(sel_projects)} · SELECTED BY NEMOTRON</div>
                  <div class='proj-name'>{pname}</div>
                  <div class='proj-desc'>{pdesc[:300] if pdesc else "—"}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 4: Resume ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if not tailored:
            st.info("No tailored resume generated yet.")
        else:
            r1, r2 = st.columns(2)
            with r1:
                st.markdown("<div style='font-family:var(--font-mono);font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px'>ORIGINAL</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='resume-box'>{st.session_state.agent_result.get('original_resume','')[:3000]}</div>", unsafe_allow_html=True)
            with r2:
                st.markdown("<div style='font-family:var(--font-mono);font-size:11px;color:var(--green);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px'>✨ TAILORED BY NEMOTRON</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='resume-box'>{tailored[:3000]}</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            # Actions
            a1, a2, a3 = st.columns(3)
            with a1:
                st.download_button(
                    "⬇️ Download Tailored Resume (.txt)",
                    data=tailored,
                    file_name=f"{profile.get('name','resume').replace(' ','_')}_tailored.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with a2:
                if st.button("📄 Generate LaTeX PDF", type="primary", use_container_width=True):
                    st.session_state.resume_for_pdf  = tailored
                    st.session_state.profile_for_pdf = profile
                    # Generate LaTeX inline
                    st.session_state.show_latex = True
                    st.rerun()
            with a3:
                if st.button("💾 Save to Arsenal", use_container_width=True):
                    try:
                        company = selected_job.get("company","") if selected_job else ""
                        title   = selected_job.get("title","")   if selected_job else ""
                        requests.post(f"{API}/resumes/company", json={
                            "company": company, "job_title": title,
                            "tailored_content": tailored, "base_resume_name": "default"
                        }, timeout=5)
                        st.success("✅ Saved to Resume Arsenal!")
                    except Exception as ex:
                        st.error(f"Could not save: {ex}")

# ── LaTeX Generator ───────────────────────────────────────────────────────────
if st.session_state.get("show_latex") and st.session_state.get("resume_for_pdf"):
    st.markdown("<hr class='divline'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:var(--font-display);font-size:20px;font-weight:800;color:var(--white);margin-bottom:8px'>📄 Generate LaTeX Resume</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px;color:var(--muted);margin-bottom:20px'>Nemotron converts your tailored resume into a clean, 1-page ATS-ready LaTeX file.</div>", unsafe_allow_html=True)

    if not st.session_state.latex_code:
        gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
        with gen_col2:
            if st.button("🧠 Generate LaTeX with Nemotron", type="primary", use_container_width=True):
                with st.spinner("Generating LaTeX..."):
                    try:
                        from openai import OpenAI
                        client = OpenAI(
                            base_url="https://integrate.api.nvidia.com/v1",
                            api_key=NVIDIA_API_KEY or "YOUR_NVIDIA_API_KEY"
                        )
                        p = profile
                        prompt = f"""You are an expert LaTeX resume writer.
Convert the resume below into clean, professional, strictly 1-page LaTeX using Jake's Resume style.

OUTPUT RULES:
- Output ONLY compilable LaTeX code. No markdown, no backticks, no explanations.
- Do NOT fabricate any experience, metrics, or skills.
- Strictly 1 page.
- ATS-friendly: no tables for main content, no graphics, no colors except black.
- Sections: Summary, Education, Experience, Projects, Skills.

PERSONAL INFO:
Name: {p.get('name','Your Name')}
Email: {p.get('email','email@example.com')}
Phone: {p.get('phone','')}
LinkedIn: {p.get('linkedin','')}
GitHub: {p.get('github','')}
University: {p.get('university','')}
Degree: {p.get('degree','')}
Graduation: {p.get('graduation','')}

RESUME CONTENT:
{st.session_state.resume_for_pdf}

Output complete compilable LaTeX only:"""

                        resp = client.chat.completions.create(
                            model="nvidia/llama-3.3-nemotron-super-49b-v1",
                            messages=[{"role":"user","content":prompt}],
                            max_tokens=3000, temperature=0.2
                        )
                        raw = resp.choices[0].message.content.strip()
                        if raw.startswith("```"): raw = raw.split("\n",1)[1]
                        if raw.endswith("```"):   raw = raw.rsplit("```",1)[0]
                        st.session_state.latex_code = raw.strip()
                        st.success("✅ LaTeX generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"LaTeX generation failed: {e}")

    if st.session_state.latex_code:
        edited = st.text_area("LaTeX Code (editable)", value=st.session_state.latex_code, height=350, label_visibility="collapsed")
        st.session_state.latex_code = edited

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "⬇️ Download .tex File",
                data=st.session_state.latex_code,
                file_name=f"{profile.get('name','resume').replace(' ','_')}_resume.tex",
                mime="text/plain",
                use_container_width=True
            )
        with dl2:
            st.markdown("""
            <div style='background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;font-size:13px;color:var(--muted)'>
            🍃 <b style='color:var(--white)'>Compile on Overleaf:</b> Download the .tex file → 
            <a href='https://www.overleaf.com/project' target='_blank' style='color:var(--green)'>overleaf.com</a> → 
            New Project → Upload → Compile → Download PDF ✅
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)