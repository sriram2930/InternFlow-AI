import streamlit as st
import requests
import json
import re

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
    .section-title { color: #76B900; font-size: 20px; font-weight: 700; margin-bottom: 4px; margin-top: 24px; }
    .section-desc { color: #888; font-size: 14px; margin-bottom: 16px; }
    .result-card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; }
    .score-circle { background: linear-gradient(135deg, #76B900, #4a7500); border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 900; color: #000; margin: 0 auto; }
    .keyword-present { background: rgba(118,185,0,0.15); border: 1px solid #76B900; color: #76B900; padding: 4px 12px; border-radius: 20px; font-size: 12px; display: inline-block; margin: 3px; }
    .keyword-missing { background: rgba(255,80,80,0.1); border: 1px solid #ff5050; color: #ff5050; padding: 4px 12px; border-radius: 20px; font-size: 12px; display: inline-block; margin: 3px; }
    .project-selected { background: #1e1e1e; border-left: 3px solid #76B900; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; }
    .job-banner { background: linear-gradient(90deg, #1a1a1a, #1e2a10); border: 1px solid #76B900; border-radius: 12px; padding: 16px 24px; margin-bottom: 16px; }
    .success-box { background: #0a1a05; border: 1px solid #76B900; border-radius: 8px; padding: 10px 16px; font-size: 13px; color: #76B900; margin-top: 8px; }
    .warn-box { background: #1a1200; border: 1px solid #f0a500; border-radius: 8px; padding: 10px 16px; font-size: 13px; color: #f0a500; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Initialize all session state keys upfront ─────────────────────────────────
if "jd_content" not in st.session_state:
    st.session_state["jd_content"] = ""
if "fetch_msg" not in st.session_state:
    st.session_state["fetch_msg"] = ""
if "fetch_ok" not in st.session_state:
    st.session_state["fetch_ok"] = False

# ── Helpers ───────────────────────────────────────────────────────────────────
def try_parse_json(text: str):
    if not text or not isinstance(text, str):
        return {}
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def normalize_projects(selected, all_projects):
    if not selected:
        return []
    if selected and isinstance(selected[0], dict):
        return [{"name": p.get("name", ""), "description": p.get("description", ""),
                 "rewritten_description": p.get("rewritten_description", "")} for p in selected]
    if selected and isinstance(selected[0], str):
        name_set = set(selected)
        out = [{"name": p["name"], "description": p.get("description", ""), "rewritten_description": ""}
               for p in (all_projects or []) if p["name"] in name_set]
        return out or [{"name": n, "description": "", "rewritten_description": ""} for n in selected]
    return []


def do_fetch_jd(url: str):
    """Call backend /jobfetch/fetch-jd and store result in session state."""
    try:
        resp = requests.post(
            f"{API}/jobfetch/fetch-jd",
            json={"url": url.strip()},
            timeout=35
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success") and data.get("text"):
                st.session_state["jd_content"] = data["text"]
                st.session_state["fetch_msg"]   = f"✅ {data.get('message','JD fetched successfully')}"
                st.session_state["fetch_ok"]    = True
            else:
                st.session_state["jd_content"] = ""
                st.session_state["fetch_msg"]   = data.get("message", "❌ Could not extract JD.")
                st.session_state["fetch_ok"]    = False
        else:
            st.session_state["jd_content"] = ""
            st.session_state["fetch_msg"]   = f"❌ Backend error HTTP {resp.status_code}"
            st.session_state["fetch_ok"]    = False
    except Exception as e:
        st.session_state["jd_content"] = ""
        st.session_state["fetch_msg"]   = f"❌ Could not reach backend: {e}"
        st.session_state["fetch_ok"]    = False


def auto_extract_projects(resume_text: str) -> list:
    try:
        resp = requests.post(
            f"{API}/jobfetch/extract-projects",
            json={"resume_text": resume_text},
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json().get("projects", [])
    except Exception:
        pass
    return []


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
st.markdown("<h1 style='color:#fff'>🤖 AI Resume Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888'>Powered by NVIDIA Nemotron · Fetch a JD → Agent rewrites your resume for ATS.</p>",
            unsafe_allow_html=True)

# ── Selected Job Banner ───────────────────────────────────────────────────────
selected_job = st.session_state.get("selected_job")
if selected_job:
    st.markdown(f"""
    <div class='job-banner'>
        <b style='font-size:17px;color:#fff'>{selected_job.get('title','')}</b><br>
        <span style='color:#76B900'>{selected_job.get('company','')}</span>
        &nbsp;·&nbsp;<span style='color:#888'>📍 {', '.join(selected_job.get('locations',[]))}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — JOB DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>📋 Job Description</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>Enter the job URL and click Fetch JD — OR paste the JD directly below.</div>",
            unsafe_allow_html=True)

# URL input row
col_url, col_btn = st.columns([4, 1])
with col_url:
    job_url = st.text_input(
        "url",
        placeholder="Paste job URL here (Lever, Greenhouse, company careers page, LinkedIn...)",
        label_visibility="collapsed"
    )
with col_btn:
    fetch_clicked = st.button("🔍 Fetch JD", type="primary", use_container_width=True)

# Handle fetch click
if fetch_clicked:
    if not job_url.strip():
        st.warning("Please enter a job URL first.")
    else:
        with st.spinner("⏳ Fetching job description... (10–25 seconds)"):
            do_fetch_jd(job_url)

# Show status message
if st.session_state["fetch_msg"]:
    if st.session_state["fetch_ok"]:
        st.markdown(f"<div class='success-box'>{st.session_state['fetch_msg']}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='warn-box'>{st.session_state['fetch_msg']}<br><br>"
                    f"<b>Solution:</b> Manually copy the job description from the browser and paste it below.</div>",
                    unsafe_allow_html=True)

# ── THE FIX: use value= directly from session state, no key= ─────────────────
jd_text = st.text_area(
    "Job Description Text",
    value=st.session_state["jd_content"],   # <-- this is the fix
    height=350,
    placeholder=(
        "Step 1: Enter job URL above and click 'Fetch JD'\n\n"
        "— OR —\n\n"
        "Step 2: Manually paste the full job description here\n"
        "(Include: role overview, responsibilities, requirements, skills, qualifications)"
    ),
    label_visibility="collapsed"
)

# Update session state when user edits manually
st.session_state["jd_content"] = jd_text

# Action buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state["jd_content"]:
        char_count = len(st.session_state["jd_content"])
        st.markdown(f"<span style='color:#888;font-size:12px'>📝 {char_count} characters loaded</span>",
                    unsafe_allow_html=True)
with col2:
    if st.session_state["jd_content"]:
        if st.button("🗑️ Clear JD"):
            st.session_state["jd_content"] = ""
            st.session_state["fetch_msg"]  = ""
            st.session_state["fetch_ok"]   = False
            st.rerun()

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — RESUME
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>📄 Your Resume</div>", unsafe_allow_html=True)

resume_text = st.session_state.get("resume_text", "")
if not resume_text:
    try:
        res = requests.get(f"{API}/resumes", timeout=10)
        base = res.json().get("base_resumes", [])
        if base:
            resume_text = base[0].get("content", "") or ""
            st.session_state["resume_text"] = resume_text
    except Exception:
        pass

resume_text = st.text_area(
    "Resume",
    value=resume_text,
    height=260,
    placeholder="Upload your resume in the Profile page — it auto-loads here.",
    label_visibility="collapsed"
)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — PROJECTS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>🗂️ Your Projects & Experience</div>", unsafe_allow_html=True)

# Auto-extract when resume available
if resume_text and not st.session_state.get("projects_extracted"):
    with st.spinner("Extracting projects from resume..."):
        extracted = auto_extract_projects(resume_text)
        if extracted:
            existing = {p["name"] for p in st.session_state.get("projects", [])}
            new = [p for p in extracted if p["name"] not in existing]
            st.session_state["projects"] = new + st.session_state.get("projects", [])
            st.session_state["projects_extracted"] = True

projects = st.session_state.get("projects", [])

if projects:
    proj_count = len([p for p in projects if p.get("source") == "resume_projects"])
    exp_count  = len([p for p in projects if p.get("source") == "resume_experience"])
    st.markdown(
        f"<div class='section-desc'>✅ <b style='color:#76B900'>{len(projects)} items</b> extracted from resume "
        f"({proj_count} projects + {exp_count} work experiences). Nemotron picks best 3.</div>",
        unsafe_allow_html=True
    )
    with st.expander("👁️ View all extracted items"):
        for p in projects:
            icon = "📁" if p.get("source") == "resume_projects" else "💼"
            st.markdown(f"**{icon} {p['name']}**")
            st.markdown(
                f"<span style='color:#888;font-size:12px'>{p.get('description','')[:200]}</span>",
                unsafe_allow_html=True
            )
            st.markdown("---")
    if st.button("🔄 Re-extract from resume"):
        st.session_state.pop("projects_extracted", None)
        st.session_state.pop("projects", None)
        st.rerun()
else:
    if resume_text:
        if st.button("📄 Extract Projects from Resume Now"):
            with st.spinner("Extracting..."):
                extracted = auto_extract_projects(resume_text)
                if extracted:
                    st.session_state["projects"] = extracted
                    st.session_state["projects_extracted"] = True
                    st.rerun()
                else:
                    st.warning("Could not extract automatically. Add manually below.")
    else:
        st.warning("⚠️ Upload your resume in Profile first — projects auto-load from it.")

with st.expander("➕ Add project manually"):
    proj_input = st.text_area(
        "One per line: Name | Description",
        height=80,
        placeholder="Distributed Messaging | FastAPI, Docker, AWS, fault tolerance, leader election"
    )
    if proj_input:
        for line in proj_input.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 1)
                new_p = {"name": parts[0].strip(), "description": parts[1].strip(), "source": "manual"}
                if new_p["name"] not in {p["name"] for p in projects}:
                    projects.append(new_p)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# RUN AGENT
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_btn = st.button("⚡ Run Nemotron Agent", type="primary", use_container_width=True)

if run_btn:
    jd_final = st.session_state["jd_content"]
    if not jd_final.strip():
        st.warning("⚠️ No JD found! Fetch from URL or paste it above.")
    elif not resume_text.strip():
        st.warning("⚠️ No resume. Upload in Profile page first.")
    elif not projects:
        st.warning("⚠️ No projects found. Click 'Extract Projects' above.")
    else:
        with st.spinner("🧠 Nemotron analyzing... (15–60 seconds)"):
            try:
                payload = {
                    "job_description": jd_final,
                    "resume_text": resume_text,
                    "projects": [
                        {"name": p["name"], "description": p.get("description", "")}
                        for p in projects
                    ]
                }
                resp = requests.post(f"{API}/agent/analyze", json=payload, timeout=600)
                if resp.status_code != 200:
                    st.error(f"Agent failed: HTTP {resp.status_code}")
                    st.stop()

                result = resp.json()
                diag   = try_parse_json(result.get("diagnostic_report", ""))

                st.session_state["agent_result"] = {
                    "diagnostic": {
                        "match_score":       diag.get("match_score", 0),
                        "present_keywords":  diag.get("present_keywords", []),
                        "missing_keywords":  result.get("missing_keywords", []) or diag.get("missing_keywords", [])
                    },
                    "selected_projects": normalize_projects(result.get("selected_projects", []), projects),
                    "tailored_resume":   result.get("tailored_resume", "")
                }
                st.success("✅ Analysis complete! Scroll down for results.")

            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if "agent_result" in st.session_state:
    result = st.session_state["agent_result"]
    st.markdown("---")
    st.markdown("<h2 style='color:#76B900'>📊 Analysis Results</h2>", unsafe_allow_html=True)

    diag  = result.get("diagnostic", {})
    score = int(diag.get("match_score", 0) or 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        label = "Strong match!" if score >= 70 else "Needs improvement" if score >= 50 else "Significant gaps"
        st.markdown(f"""
        <div class='result-card' style='text-align:center'>
            <div style='color:#888;margin-bottom:12px;font-size:14px'>ATS Match Score</div>
            <div class='score-circle'>{score}%</div>
            <div style='color:#888;margin-top:12px;font-size:13px'>{label}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        present = diag.get("present_keywords", []) or []
        st.markdown(f"""
        <div class='result-card'>
            <div style='color:#76B900;font-weight:700;margin-bottom:8px'>✅ Present ({len(present)})</div>
            <div>{''.join([f"<span class='keyword-present'>{k}</span>" for k in present[:15]])}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        missing = diag.get("missing_keywords", []) or []
        st.markdown(f"""
        <div class='result-card'>
            <div style='color:#ff5050;font-weight:700;margin-bottom:8px'>❌ Missing ({len(missing)})</div>
            <div>{''.join([f"<span class='keyword-missing'>{k}</span>" for k in missing[:15]])}</div>
        </div>""", unsafe_allow_html=True)

    sel = result.get("selected_projects", [])
    if sel:
        st.markdown("<div class='section-title'>🎯 Best Projects for This Job</div>", unsafe_allow_html=True)
        for p in sel:
            st.markdown(f"""
            <div class='project-selected'>
                <b style='color:#76B900'>{p.get('name','')}</b><br>
                <span style='color:#ccc;font-size:13px'>{p.get('rewritten_description') or p.get('description','')}</span>
            </div>""", unsafe_allow_html=True)

    tailored = result.get("tailored_resume", "")
    if tailored:
        st.markdown("<div class='section-title'>📝 Tailored Resume</div>", unsafe_allow_html=True)
        with st.expander("📄 View Full Tailored Resume", expanded=True):
            st.text_area("", value=tailored, height=400, label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            company = selected_job["company"] if selected_job else "Company"
            if st.button(f"💾 Save ({company})", use_container_width=True):
                try:
                    requests.post(f"{API}/resumes/company", json={
                        "company": company,
                        "job_title": selected_job["title"] if selected_job else "Role",
                        "tailored_content": tailored,
                        "base_resume_name": "default"
                    }, timeout=10)
                    st.success("✅ Saved!")
                except Exception as e:
                    st.error(f"Save failed: {e}")
        with col2:
            if st.button("📄 Generate PDF →", type="primary", use_container_width=True):
                st.session_state["resume_for_pdf"]  = tailored
                st.session_state["profile_for_pdf"] = st.session_state.get("profile", {})
                st.switch_page("pages/5_resume_output.py")
