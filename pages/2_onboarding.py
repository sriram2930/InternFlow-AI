import streamlit as st
import requests
import json
import PyPDF2
import io
import re

st.set_page_config(
    page_title="InternFlow AI – Setup",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = "http://127.0.0.1:8000"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');"
    "#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}"
    "[data-testid='collapsedControl']{display:none;}"
    "* {box-sizing:border-box;}"
    ":root{--lav200:#e9d5ff;--lav300:#d8b4fe;--lav400:#c084fc;--lav500:#a855f7;--lav600:#9333ea;--lav700:#7e22ce;--bg:#08080f;--bg2:#0e0e1a;--bg3:#131325;--txt:#f1f0f8;--muted:#7c7a9a;--bdr:rgba(168,85,247,0.18);}"
    ".stApp{background:#08080f !important;font-family:'Outfit',sans-serif;color:#f1f0f8;}"
    ".block-container{padding:32px 48px 80px !important;max-width:1100px !important;margin:0 auto !important;}"
    # Inputs
    ".stTextInput > div > div > input{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;font-family:'Outfit',sans-serif !important;font-size:15px !important;}"
    ".stTextInput label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;}"
    ".stTextArea > div > textarea{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;}"
    ".stTextArea label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;}"
    ".stMultiSelect > div > div{background:rgba(255,255,255,0.03) !important;border:1px solid rgba(168,85,247,0.22) !important;border-radius:10px !important;color:#f1f0f8 !important;}"
    ".stMultiSelect label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;}"
    ".stFileUploader > div{background:rgba(255,255,255,0.02) !important;border:1px dashed rgba(168,85,247,0.3) !important;border-radius:12px !important;}"
    ".stFileUploader label{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;}"
    # Buttons
    ".stButton > button{background:linear-gradient(135deg,#7c3aed,#6d28d9) !important;color:#fff !important;border:none !important;border-radius:10px !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;font-weight:600 !important;padding:9px 20px !important;height:auto !important;transition:opacity 0.2s !important;}"
    ".stButton > button:hover{opacity:0.82 !important;}"
    ".stButton > button[kind='secondary']{background:rgba(168,85,247,0.08) !important;border:1px solid rgba(168,85,247,0.25) !important;color:#c084fc !important;}"
    # Tabs
    ".stTabs [data-baseweb='tab-list']{background:transparent !important;border-bottom:1px solid rgba(168,85,247,0.18) !important;}"
    ".stTabs [data-baseweb='tab']{color:#7c7a9a !important;font-family:'Outfit',sans-serif !important;font-size:14px !important;font-weight:500 !important;}"
    ".stTabs [aria-selected='true']{color:#c084fc !important;border-bottom:2px solid #a855f7 !important;}"
    # Expander
    ".streamlit-expanderHeader{background:rgba(255,255,255,0.02) !important;border:1px solid rgba(168,85,247,0.18) !important;border-radius:12px !important;color:#c084fc !important;font-family:'Outfit',sans-serif !important;}"
    # Nav
    ".nav-logo-btn{background:none !important;border:none !important;padding:0 !important;box-shadow:none !important;cursor:pointer;}.nav-logo{font-family:'Outfit',sans-serif;font-size:22px;font-weight:800;background:linear-gradient(135deg,#c4b5fd,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:inline-block;}.nav-tagline{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:0.18em;text-transform:uppercase;color:#3d3a55;margin-top:2px;}a:has(.nav-logo){text-decoration:none;display:inline-block;transition:opacity 0.2s;}a:has(.nav-logo):hover{opacity:0.72;}"
    # Page header
    ".page-hd{font-family:'Instrument Serif',serif;font-size:clamp(32px,4vw,52px);font-weight:400;color:var(--txt);letter-spacing:-1px;margin:0 0 8px;text-align:center;}"
    ".page-hd em{font-style:italic;color:var(--lav300);}"
    ".page-sub{font-size:16px;color:var(--muted);font-weight:300;text-align:center;margin:0 0 32px;}"
    # Divider
    ".div{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.22),transparent);margin:28px 0;}"
    # Section headers
    ".sec-eyebrow{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;color:var(--lav400);margin-bottom:6px;display:flex;align-items:center;gap:10px;}"
    ".sec-eyebrow::before{content:'';display:inline-block;width:20px;height:1px;background:var(--lav500);}"
    ".sec-title{font-family:'Outfit',sans-serif;font-size:20px;font-weight:700;color:var(--txt);margin:0 0 4px;}"
    ".sec-desc{font-size:14px;color:var(--muted);margin:0 0 20px;font-weight:300;}"
    # Section card wrapper
    ".sec-card{background:var(--bg2);border:1px solid var(--bdr);border-radius:16px;padding:28px 32px;margin-bottom:24px;position:relative;overflow:hidden;}"
    ".sec-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.3),transparent);}"
    # Project card
    ".proj-card{background:var(--bg3);border:1px solid rgba(168,85,247,0.25);border-left:3px solid #7c3aed;border-radius:10px;padding:14px 18px;margin-bottom:10px;}"
    ".proj-name{font-size:15px;font-weight:700;color:var(--txt);margin-bottom:4px;}"
    ".proj-meta{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--lav400);margin-bottom:6px;}"
    ".proj-desc{font-size:13px;color:var(--muted);line-height:1.6;}"
    ".nav-home-col button{background:none !important;border:none !important;box-shadow:none !important;padding:2px 4px !important;font-family:'Outfit',sans-serif !important;font-size:22px !important;font-weight:800 !important;color:transparent !important;background-image:linear-gradient(135deg,#c4b5fd,#a78bfa) !important;-webkit-background-clip:text !important;background-clip:text !important;}.nav-home-col button:hover{opacity:0.75 !important;}</style>",
    unsafe_allow_html=True
)

# ── Navbar ────────────────────────────────────────────────────────────────────
n1, n2, n3, n4, n5, n6 = st.columns([3, 1, 1, 1, 1, 1])
with n1:
    st.markdown(
        "<a href='/' target='_self' style='text-decoration:none'>"
        "<div class='nav-logo'>🚀 InternFlow AI</div>"
        "<div class='nav-tagline'>AI-POWERED CAREER PLATFORM</div>"
        "</a>",
        unsafe_allow_html=True
    )
with n2:
    if st.button("📝 Profile", use_container_width=True, type="primary"):
        pass  # already here
with n3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with n4:
    if st.button("🤖 Agent", use_container_width=True):
        st.switch_page("pages/4_agent.py")
with n5:
    if st.button("📋 Tracker", use_container_width=True):
        st.switch_page("pages/6_applications.py")
with n6:
    if st.button("📄 Resume", use_container_width=True):
        st.switch_page("pages/7_resume_output.py")

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(
    "<div class='page-hd'>Let's set you <em>up.</em></div>"
    "<p class='page-sub'>Tell us about yourself so Nemotron can personalize everything for you.</p>",
    unsafe_allow_html=True
)

# ── Initialize session state ──────────────────────────────────────────────────
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "projects" not in st.session_state:
    st.session_state.projects = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ══════════════════════════════════════════════════════════
# SECTION 1 — Basic Info
# ══════════════════════════════════════════════════════════
st.markdown("<div class='sec-card'>", unsafe_allow_html=True)
st.markdown("<div class='sec-eyebrow'>Step 1</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-title'>👤 Basic Information</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-desc'>This populates your resume header and personalizes AI recommendations.</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    name       = st.text_input("Full Name",             placeholder="e.g. Sreeram Achutuni",          value=st.session_state.profile.get("name", ""))
    email      = st.text_input("Email",                 placeholder="e.g. sreeram@sjsu.edu",           value=st.session_state.profile.get("email", ""))
    phone      = st.text_input("Phone",                 placeholder="e.g. +1 (408) 123-4567",          value=st.session_state.profile.get("phone", ""))
with c2:
    university = st.text_input("University",            placeholder="e.g. San José State University",  value=st.session_state.profile.get("university", ""))
    degree     = st.text_input("Degree & Major",        placeholder="e.g. MS Data Analytics",          value=st.session_state.profile.get("degree", ""))
    graduation = st.text_input("Expected Graduation",   placeholder="e.g. May 2027",                   value=st.session_state.profile.get("graduation", ""))

linkedin       = st.text_input("LinkedIn URL",          placeholder="https://linkedin.com/in/yourname", value=st.session_state.profile.get("linkedin", ""))
github_profile = st.text_input("GitHub Profile URL",    placeholder="https://github.com/yourusername",  value=st.session_state.profile.get("github", ""))

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SECTION 2 — Target Roles
# ══════════════════════════════════════════════════════════
st.markdown("<div class='sec-card'>", unsafe_allow_html=True)
st.markdown("<div class='sec-eyebrow'>Step 2</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-title'>🎯 Target Roles</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-desc'>Used to rank jobs and select the best projects for each application.</div>", unsafe_allow_html=True)

role_options = [
    "ML Engineer", "Data Scientist", "Data Analyst", "Data Engineer",
    "AI Engineer", "Research Engineer", "Software Engineer", "Backend Engineer",
    "Computer Vision Engineer", "NLP Engineer", "Quantitative Analyst", "GenAI Engineer"
]
target_roles = st.multiselect(
    "Select your target roles",
    role_options,
    default=st.session_state.profile.get("target_roles", ["ML Engineer", "Data Scientist"])
)
custom_role = st.text_input("Add a custom role (optional)", placeholder="e.g. Robotics Engineer")
if custom_role and custom_role not in target_roles:
    target_roles.append(custom_role)

preferred_locations = st.multiselect(
    "Preferred Locations",
    ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
     "Remote", "Boston, MA", "Los Angeles, CA", "Chicago, IL", "San Jose, CA"],
    default=st.session_state.profile.get("preferred_locations", ["San Francisco, CA", "Remote"])
)

skills_raw = st.text_input(
    "Your Skills (comma-separated)",
    placeholder="e.g. Python, PyTorch, SQL, LangChain, React, Docker",
    value=", ".join(st.session_state.profile.get("skills", []))
)
skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SECTION 3 — Resume Upload
# ══════════════════════════════════════════════════════════
st.markdown("<div class='sec-card'>", unsafe_allow_html=True)
st.markdown("<div class='sec-eyebrow'>Step 3</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-title'>📄 Upload Your Resume</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-desc'>Upload your base resume as PDF. We parse it and use it to tailor each application.</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        raw_pages = []
        for page in pdf_reader.pages:
            raw_pages.append(page.extract_text() or "")
        raw_text = "\n".join(raw_pages)
        # Fix hyphenated line breaks: "computa-\ntional" -> "computational"
        raw_text = re.sub(r'-\n(\S)', r'\1', raw_text)
        # Join lines split mid-sentence (lowercase/bracket continuation)
        raw_text = re.sub(r'(?<![.,:;|\u2022\-])\n(?=[a-z(@/])', r' ', raw_text)
        # Collapse multiple spaces
        raw_text = re.sub(r' {2,}', ' ', raw_text)
        # Max 2 consecutive newlines
        raw_text = re.sub(r'\n{3,}', '\n\n', raw_text)
        resume_text = raw_text.strip()
        st.session_state.resume_text = resume_text
        st.success(f"✅ Parsed {len(pdf_reader.pages)} page(s) — {len(resume_text):,} characters extracted.")
        with st.expander("Preview extracted text"):
            st.text(resume_text[:1200] + "..." if len(resume_text) > 1200 else resume_text)
        # Auto-save to backend
        try:
            resume_name = f"{name}'s Resume" if name else "Base Resume"
            requests.post(f"{API}/resumes/base", json={
                "name": resume_name,
                "content": resume_text,
                "tags": target_roles[:3]
            }, timeout=5)
        except Exception:
            pass
    except Exception as e:
        st.error(f"Could not parse PDF: {e}")
elif st.session_state.resume_text:
    st.success("✅ Resume already loaded from this session.")

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SECTION 4 — Projects
# ══════════════════════════════════════════════════════════
st.markdown("<div class='sec-card'>", unsafe_allow_html=True)
st.markdown("<div class='sec-eyebrow'>Step 4</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-title'>🗂️ Projects Portfolio</div>", unsafe_allow_html=True)
st.markdown("<div class='sec-desc'>Add all your projects — Nemotron picks the best 3 per job automatically.</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🐙 Import from GitHub", "✏️ Add Manually"])

with tab1:
    github_url = st.text_input(
        "GitHub Profile URL",
        placeholder="https://github.com/yourusername",
        key="gh_import"
    )
    if st.button("🔍 Scrape GitHub Projects"):
        if github_url:
            with st.spinner("Fetching your GitHub repos..."):
                try:
                    username = github_url.rstrip("/").split("/")[-1]
                    repos_resp = requests.get(
                        f"https://api.github.com/users/{username}/repos?sort=updated&per_page=20",
                        headers={"Accept": "application/vnd.github.v3+json"},
                        timeout=10
                    )
                    if repos_resp.status_code == 200:
                        repos = repos_resp.json()
                        imported = 0
                        existing_names = [p["name"] for p in st.session_state.projects]
                        for repo in repos:
                            if repo.get("fork"):
                                continue
                            repo_name   = repo["name"]
                            description = repo.get("description", "") or ""
                            stars       = repo.get("stargazers_count", 0)
                            language    = repo.get("language", "Unknown")
                            readme_text = ""
                            try:
                                readme_resp = requests.get(
                                    f"https://api.github.com/repos/{username}/{repo_name}/readme",
                                    headers={"Accept": "application/vnd.github.v3.raw"},
                                    timeout=5
                                )
                                if readme_resp.status_code == 200:
                                    readme_text = readme_resp.text[:500]
                            except Exception:
                                pass
                            proj_desc = f"{description}. " if description else ""
                            proj_desc += f"Language: {language}. Stars: {stars}. "
                            if readme_text:
                                proj_desc += f"Details: {readme_text[:300]}"
                            if repo_name not in existing_names and proj_desc.strip():
                                st.session_state.projects.append({
                                    "name":        repo_name,
                                    "description": proj_desc.strip(),
                                    "source":      "github",
                                    "language":    language,
                                    "stars":       stars
                                })
                                imported += 1
                        st.success(f"✅ Imported {imported} projects from GitHub!")
                        st.rerun()
                    else:
                        st.error(f"Could not fetch repos (status {repos_resp.status_code}). Check the username.")
                except Exception as e:
                    st.error(f"GitHub scraping failed: {e}")
        else:
            st.warning("Please enter a GitHub URL.")

with tab2:
    pc1, pc2 = st.columns(2)
    with pc1:
        proj_name = st.text_input("Project Name", placeholder="e.g. PAMAP2 Activity Recognition")
    with pc2:
        proj_lang = st.text_input("Tech Stack",   placeholder="e.g. Python, PyTorch, Streamlit")
    proj_desc_input = st.text_area(
        "Project Description", height=100,
        placeholder="e.g. Built HAR system using Random Forest on 2.8M records achieving 94.2% accuracy."
    )
    if st.button("➕ Add Project"):
        if proj_name and proj_desc_input:
            existing_names = [p["name"] for p in st.session_state.projects]
            if proj_name in existing_names:
                st.warning("A project with this name already exists.")
            else:
                full_desc = f"{proj_desc_input} Tech: {proj_lang}" if proj_lang else proj_desc_input
                st.session_state.projects.append({
                    "name":        proj_name,
                    "description": full_desc,
                    "source":      "manual",
                    "language":    proj_lang,
                    "stars":       0
                })
                st.success(f"✅ Added: {proj_name}")
                st.rerun()
        else:
            st.warning("Please fill in both project name and description.")

# ── Current projects list ─────────────────────────────────────────────────────
if st.session_state.projects:
    st.markdown(f"<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-family:JetBrains Mono,monospace;font-size:11px;color:#a855f7;"
        f"letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px'>"
        f"Portfolio — {len(st.session_state.projects)} project(s)</div>",
        unsafe_allow_html=True
    )
    for i, p in enumerate(st.session_state.projects):
        col_p, col_rm = st.columns([10, 1])
        with col_p:
            badge  = "🐙" if p.get("source") == "github" else "✏️"
            lang   = f" · {p.get('language', '')}" if p.get("language") else ""
            stars  = f" · ⭐ {p.get('stars', 0)}" if p.get("stars", 0) > 0 else ""
            desc   = p["description"][:160] + "..." if len(p["description"]) > 160 else p["description"]
            st.markdown(
                f"<div class='proj-card'>"
                f"<div class='proj-name'>{badge} {p['name']}</div>"
                f"<div class='proj-meta'>{lang.lstrip(' · ')}{stars}</div>"
                f"<div class='proj-desc'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_rm:
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            if st.button("✕", key=f"rm_{i}", use_container_width=True):
                st.session_state.projects.pop(i)
                st.rerun()
else:
    st.markdown(
        "<div style='background:rgba(168,85,247,0.05);border:1px dashed rgba(168,85,247,0.2);"
        "border-radius:10px;padding:20px;text-align:center;color:#7c7a9a;font-size:14px;margin-top:16px'>"
        "No projects yet — import from GitHub or add manually above."
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SAVE & CONTINUE
# ══════════════════════════════════════════════════════════
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    if st.button("💾  Save Profile & Browse Jobs →", type="primary", use_container_width=True):
        if not name:
            st.warning("Please enter your name.")
        elif not st.session_state.resume_text and not st.session_state.projects:
            st.warning("Please upload a resume or add at least one project.")
        else:
            st.session_state.profile = {
                "name":               name,
                "email":              email,
                "phone":              phone,
                "university":         university,
                "degree":             degree,
                "graduation":         graduation,
                "linkedin":           linkedin,
                "github":             github_profile,
                "target_roles":       target_roles,
                "preferred_locations":preferred_locations,
                "skills":             skills,
            }
            st.success("✅ Profile saved! Heading to jobs...")
            st.switch_page("pages/3_jobs.py")
