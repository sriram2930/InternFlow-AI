import streamlit as st
import requests
import json

st.set_page_config(
    page_title="InternFlow AI – Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}

    .stApp { background: #0f0f0f; color: #fff; }

    .nav-logo { color: #76B900; font-size: 22px; font-weight: 900; }

    .section-title {
        color: #76B900;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
        margin-top: 24px;
    }
    .section-desc { color: #888; font-size: 14px; margin-bottom: 16px; }

    .result-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .score-circle {
        background: linear-gradient(135deg, #76B900, #4a7500);
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        font-weight: 900;
        color: #000;
        margin: 0 auto;
    }
    .keyword-present {
        background: rgba(118,185,0,0.15);
        border: 1px solid #76B900;
        color: #76B900;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
        margin: 3px;
    }
    .keyword-missing {
        background: rgba(255,80,80,0.1);
        border: 1px solid #ff5050;
        color: #ff5050;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
        margin: 3px;
    }
    .project-selected {
        background: #1e1e1e;
        border-left: 3px solid #76B900;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .job-banner {
        background: linear-gradient(90deg, #1a1a1a, #1e2a10);
        border: 1px solid #76B900;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Navbar ────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown("<div class='nav-logo'>🚀 InternFlow AI</div>", unsafe_allow_html=True)
with col2:
    if st.button("📝 Profile", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")
with col3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with col4:
    if st.button("✅ Applications", use_container_width=True):
        st.switch_page("pages/5_resume_output.py")

st.markdown("---")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='color:#fff'>🤖 AI Resume Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888'>Powered by NVIDIA Nemotron · Analyzes JD, selects best projects, rewrites your resume.</p>", unsafe_allow_html=True)

# ── Show selected job banner if came from jobs page ───────────────────────────
selected_job = st.session_state.get("selected_job", None)
if selected_job:
    st.markdown(f"""
    <div class='job-banner'>
        <div style='font-size:18px;font-weight:700;color:#fff'>{selected_job['title']}</div>
        <div style='color:#76B900;font-weight:600'>{selected_job['company']} &nbsp;·&nbsp;
        <span style='color:#888'>📍 {', '.join(selected_job['locations'])}</span></div>
        <div style='color:#aaa;font-size:13px;margin-top:8px'>{selected_job['description'][:300]}...</div>
    </div>
    """, unsafe_allow_html=True)
    default_jd = selected_job.get("description", "")
else:
    default_jd = ""

st.markdown("---")

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-title'>📋 Job Description</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>Paste the full JD here for best results.</div>", unsafe_allow_html=True)
    jd_text = st.text_area("Job Description", height=280,
        value=default_jd,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed")

with col2:
    st.markdown("<div class='section-title'>📄 Your Resume</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>Auto-loaded from onboarding, or paste manually.</div>", unsafe_allow_html=True)

    # Try to load from session state first
    saved_resume = st.session_state.get("resume_text", "")

    # Also try to load from backend
    if not saved_resume:
        try:
            res = requests.get(f"{API}/resumes", timeout=5)
            resumes = res.json().get("resumes", [])
            base_resumes = [r for r in resumes if r.get("type") == "base"]
            if base_resumes:
                saved_resume = base_resumes[0]["content"]
        except:
            pass

    resume_text = st.text_area("Resume Text", height=280,
        value=saved_resume,
        placeholder="Your resume will auto-load if you uploaded it in onboarding. Or paste it here...",
        label_visibility="collapsed")

# ── Projects ──────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>🗂️ Your Projects Portfolio</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>Nemotron will pick the best 3 for this role. Add more for better selection.</div>", unsafe_allow_html=True)

# Load from session state
projects = st.session_state.get("projects", [])

if projects:
    st.success(f"✅ {len(projects)} projects loaded from your profile")
    with st.expander("View your projects"):
        for p in projects:
            st.markdown(f"**{p['name']}** — {p['description'][:100]}...")
else:
    st.info("No projects in session. Add them in your profile or paste below.")

# Allow manual project input as fallback
with st.expander("➕ Add/Edit projects for this analysis"):
    proj_input = st.text_area("Paste projects (one per line: Name | Description)",
        height=120,
        placeholder="PAMAP2 HAR | Built activity recognition system with 94.2% accuracy using Random Forest on 2.8M records\nIPL Analytics | Flask + MySQL dashboard with advanced SQL window functions")
    if proj_input:
        manual_projects = []
        for line in proj_input.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 1)
                manual_projects.append({"name": parts[0].strip(), "description": parts[1].strip()})
        if manual_projects:
            projects = manual_projects + projects

st.markdown("---")

# ── Run Agent ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_btn = st.button("⚡ Run Nemotron Agent", type="primary", use_container_width=True)

if run_btn:
    if not jd_text.strip():
        st.warning("Please paste a job description first!")
    elif not resume_text.strip():
        st.warning("Please add your resume text!")
    elif not projects:
        st.warning("Please add at least one project!")
    else:
        with st.spinner("🧠 Nemotron is analyzing... This may take 15-30 seconds..."):
            try:
                payload = {
                    "job_description": jd_text,
                    "resume_text": resume_text,
                    "projects": [{"name": p["name"], "description": p["description"]} for p in projects]
                }
                response = requests.post(f"{API}/agent/analyze", json=payload, timeout=120)
                result = response.json()

                if result.get("status") == "success":
                    st.session_state.agent_result = result
                    st.session_state.agent_jd = jd_text
                    st.session_state.agent_resume = resume_text
                    st.success("✅ Analysis complete!")
                else:
                    st.error(f"Agent error: {result.get('error', 'Unknown error')}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ── Display Results ───────────────────────────────────────────────────────────
if "agent_result" in st.session_state:
    result = st.session_state.agent_result
    st.markdown("---")
    st.markdown("<h2 style='color:#76B900'>📊 Analysis Results</h2>", unsafe_allow_html=True)

    # ── Match Score ───────────────────────────────────────────────────────────
    diagnostic = result.get("diagnostic", {})
    match_score = diagnostic.get("match_score", 0)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f"""
        <div class='result-card' style='text-align:center'>
            <div style='color:#888;margin-bottom:12px;font-size:14px'>ATS Match Score</div>
            <div class='score-circle'>{match_score}%</div>
            <div style='color:#888;margin-top:12px;font-size:13px'>
                {'🟢 Strong match!' if match_score >= 70 else '🟡 Needs improvement' if match_score >= 50 else '🔴 Significant gaps'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        present = diagnostic.get("present_keywords", [])
        st.markdown(f"""
        <div class='result-card'>
            <div style='color:#76B900;font-weight:700;margin-bottom:8px'>✅ Keywords Present ({len(present)})</div>
            <div>{''.join([f"<span class='keyword-present'>{k}</span>" for k in present[:15]])}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        missing = diagnostic.get("missing_keywords", [])
        st.markdown(f"""
        <div class='result-card'>
            <div style='color:#ff5050;font-weight:700;margin-bottom:8px'>❌ Missing Keywords ({len(missing)})</div>
            <div>{''.join([f"<span class='keyword-missing'>{k}</span>" for k in missing[:15]])}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Selected Projects ─────────────────────────────────────────────────────
    selected_projects = result.get("selected_projects", [])
    if selected_projects:
        st.markdown("<div class='section-title'>🎯 Nemotron Selected These Projects</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-desc'>Chosen because they best match this job description.</div>", unsafe_allow_html=True)
        for p in selected_projects:
            st.markdown(f"""
            <div class='project-selected'>
                <b style='color:#76B900'>{p.get('name', 'Project')}</b><br>
                <span style='color:#ccc;font-size:13px'>{p.get('rewritten_description', p.get('description', ''))}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Tailored Resume ───────────────────────────────────────────────────────
    tailored_resume = result.get("tailored_resume", "")
    if tailored_resume:
        st.markdown("<div class='section-title'>📝 Tailored Resume</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-desc'>Rewritten by Nemotron to match this specific JD.</div>", unsafe_allow_html=True)

        with st.expander("📄 View Full Tailored Resume", expanded=True):
            st.text_area("Tailored Resume", value=tailored_resume, height=400,
                label_visibility="collapsed")

        # Save to arsenal
        col1, col2 = st.columns(2)
        with col1:
            company_name = selected_job["company"] if selected_job else "Company"
            if st.button(f"💾 Save to Resume Arsenal ({company_name})", use_container_width=True):
                try:
                    requests.post(f"{API}/resumes/company", json={
                        "company": company_name,
                        "job_title": selected_job["title"] if selected_job else "Role",
                        "content": tailored_resume
                    })
                    st.success("✅ Saved to Resume Arsenal!")
                except:
                    st.error("Could not save — is backend running?")

        with col2:
            if st.button("📄 Generate PDF Resume →", type="primary", use_container_width=True):
                st.session_state.resume_for_pdf = tailored_resume
                st.session_state.profile_for_pdf = st.session_state.get("profile", {})
                st.switch_page("pages/5_resume_output.py")