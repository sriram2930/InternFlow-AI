import streamlit as st
import requests

st.set_page_config(
    page_title="InternFlow AI – Jobs",
    page_icon="💼",
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

    .job-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
        transition: border 0.2s;
    }
    .job-card:hover { border: 1px solid #76B900; }
    .job-title { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
    .job-company { font-size: 15px; color: #76B900; font-weight: 600; }
    .job-location { font-size: 13px; color: #888; }
    .job-desc { font-size: 13px; color: #aaa; margin-top: 8px; line-height: 1.6; }
    .tag {
        background: #76B900;
        color: #000;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
        display: inline-block;
        margin-top: 8px;
    }
    .tag-gray {
        background: #2a2a2a;
        color: #aaa;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        margin-right: 6px;
        display: inline-block;
        margin-top: 8px;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        margin-bottom: 24px;
        border-bottom: 1px solid #2a2a2a;
    }
    .nav-logo { color: #76B900; font-size: 22px; font-weight: 900; }
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
    if st.button("📄 Resume Arsenal", use_container_width=True):
        st.switch_page("pages/4_agent.py")
with col4:
    if st.button("✅ Applications", use_container_width=True):
        st.switch_page("pages/5_resume_output.py")

st.markdown("---")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='color:#fff'>💼 Internship Listings</h1>", unsafe_allow_html=True)

# Show personalized greeting if profile exists
if st.session_state.get("profile", {}).get("name"):
    name = st.session_state.profile["name"]
    roles = st.session_state.profile.get("target_roles", [])
    st.markdown(f"<p style='color:#888'>Hey {name}! Showing internships matching your target roles: <span style='color:#76B900'>{', '.join(roles[:3])}</span></p>", unsafe_allow_html=True)

# ── Search & Filters ──────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    search = st.text_input("🔍 Search", placeholder="e.g. Machine Learning, Google, Data Science")
with col2:
    location = st.text_input("📍 Location", placeholder="e.g. San Francisco, Remote")
with col3:
    limit = st.selectbox("Show", [25, 50, 100], index=0)

# ── Fetch Jobs ────────────────────────────────────────────────────────────────
try:
    params = {"limit": limit}
    if search:
        params["search"] = search
    if location:
        params["location"] = location

    response = requests.get(f"{API}/jobs", params=params, timeout=10)
    data = response.json()
    jobs = data.get("jobs", [])

    st.markdown(f"<p style='color:#888'><b style='color:#76B900'>{len(jobs)}</b> internships found</p>", unsafe_allow_html=True)
    st.markdown("---")

    if not jobs:
        st.info("No internships found. Try a different search term.")

    for job in jobs:
        with st.container():
            st.markdown(f"""
            <div class='job-card'>
                <div class='job-title'>{job['title']}</div>
                <div class='job-company'>{job['company']} &nbsp;·&nbsp; <span class='job-location'>📍 {', '.join(job['locations'])}</span></div>
                <div class='job-desc'>{job['description'][:220]}...</div>
                <div>
                    <span class='tag'>{job.get('sponsorship', 'Sponsorship Unknown')}</span>
                    {''.join([f"<span class='tag-gray'>{t}</span>" for t in job.get('terms', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                if st.button("🤖 Analyze & Apply", key=f"analyze_{job['id']}", type="primary"):
                    # Save selected job to session state and redirect to agent
                    st.session_state.selected_job = job
                    st.switch_page("pages/4_agent.py")
            with col2:
                if st.button("✅ Quick Track", key=f"track_{job['id']}"):
                    try:
                        requests.post(f"{API}/applications", json={
                            "job_id": job["id"],
                            "company": job["company"],
                            "job_title": job["title"],
                            "location": ', '.join(job["locations"]),
                            "url": job["url"]
                        })
                        st.success(f"Tracked {job['company']}!")
                    except:
                        st.error("Could not track — is the backend running?")
            with col3:
                st.markdown(f"<a href='{job['url']}' target='_blank' style='color:#76B900;font-size:13px'>🔗 View Original Posting →</a>", unsafe_allow_html=True)

            st.markdown("<div style='border-bottom:1px solid #1e1e1e;margin:8px 0'></div>", unsafe_allow_html=True)

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend.")
    st.info("Make sure FastAPI is running in another terminal:\n```\ncd backend\nuvicorn main:app --reload\n```")
except Exception as e:
    st.error(f"Something went wrong: {e}")