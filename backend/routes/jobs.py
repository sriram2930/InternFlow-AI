"""
Jobs route - uses JSearch API (RapidAPI) for real job listings.
Sign up FREE at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
Free tier: 200 requests/month - enough for development.
"""
import requests
import os
from fastapi import APIRouter
from typing import List

router = APIRouter()

# ── API Config ────────────────────────────────────────────────────────────────
# Get free key at https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
JSEARCH_URL  = "https://jsearch.p.rapidapi.com/search"

# ── ATS Scoring ───────────────────────────────────────────────────────────────
SDE_KEYWORDS = [
    "python", "java", "go", "golang", "typescript", "javascript", "c++", "sql",
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ci/cd",
    "microservices", "rest api", "fastapi", "flask", "spring boot",
    "distributed systems", "kafka", "spark", "redis",
    "postgresql", "mysql", "mongodb", "dynamodb",
    "pytorch", "tensorflow", "machine learning", "llm", "rag",
    "data structures", "algorithms", "system design", "agile",
]

DA_PENALTY_TITLES = [
    "data analyst", "business analyst", "business intelligence", "bi analyst"
]
SDE_BOOST_TITLES = [
    "software engineer", "sde", "backend", "full stack", "ml engineer",
    "ai engineer", "platform engineer", "devops", "cloud engineer"
]


def compute_ats_score(title: str, description: str, resume_keywords: List[str]) -> int:
    if not resume_keywords:
        return 50
    text = (title + " " + description).lower()
    matched = sum(1 for kw in resume_keywords if kw in text)
    base = int((matched / max(len(resume_keywords), 1)) * 100)
    boost   = 15 if any(kw in title.lower() for kw in SDE_BOOST_TITLES) else 0
    penalty = 40 if any(kw in title.lower() for kw in DA_PENALTY_TITLES) else 0
    return max(0, min(100, base + boost - penalty))


def extract_resume_keywords(resume_text: str) -> List[str]:
    lower = resume_text.lower()
    return [kw for kw in SDE_KEYWORDS if kw in lower]


# ── JSearch API (Real jobs from LinkedIn + Indeed + Glassdoor) ────────────────
def fetch_jsearch(query: str, location: str, page: int = 1) -> list:
    """
    Fetch real jobs using JSearch RapidAPI.
    Returns jobs from LinkedIn, Indeed, Glassdoor with full descriptions.
    """
    if not RAPIDAPI_KEY:
        return []

    q = query if query else "software engineer intern"
    if location:
        q = f"{q} in {location}"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": q,
        "page": str(page),
        "num_pages": "1",
        "date_posted": "today",      # only last 24hrs
        "employment_types": "INTERN" # internships only
    }

    try:
        resp = requests.get(JSEARCH_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [])
    except Exception as e:
        print(f"JSearch error: {e}")
        return []


def normalize_jsearch_job(job: dict) -> dict:
    """Convert JSearch job format to our standard format."""
    return {
        "id": job.get("job_id", "")[:80],
        "title": job.get("job_title", ""),
        "company": job.get("employer_name", ""),
        "locations": [f"{job.get('job_city','')}, {job.get('job_state','')}".strip(", ")],
        "url": job.get("job_apply_link") or job.get("job_google_link", "#"),
        "date_posted": job.get("job_posted_at_timestamp", 0),
        "description": job.get("job_description", "No description available."),
        "sponsorship": "Check posting",
        "terms": [],
        "source": f"jsearch:{job.get('job_publisher','')}"
    }


# ── Adzuna API (backup - free with key) ───────────────────────────────────────
def fetch_adzuna(query: str, location: str) -> list:
    """Fetch from Adzuna - free API, get key at developer.adzuna.com"""
    app_id  = os.getenv("ADZUNA_APP_ID", "")
    app_key = os.getenv("ADZUNA_APP_KEY", "")
    if not app_id or not app_key:
        return []

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 50,
        "what": query or "software engineer intern",
        "sort_by": "date",
        "content-type": "application/json",
    }
    if location:
        params["where"] = location

    try:
        resp = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params, timeout=15
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [{
            "id": f"{j.get('company',{}).get('display_name','')}-{j.get('title','')}".replace(" ","-").lower()[:80],
            "title": j.get("title", ""),
            "company": j.get("company", {}).get("display_name", ""),
            "locations": [j.get("location", {}).get("display_name", "")],
            "url": j.get("redirect_url", "#"),
            "date_posted": 0,
            "description": j.get("description", "No description available."),
            "sponsorship": "Check posting",
            "terms": [],
            "source": "adzuna"
        } for j in results]
    except Exception as e:
        print(f"Adzuna error: {e}")
        return []


# ── Simplify Jobs (GitHub, free, no key, but NO descriptions) ─────────────────
def fetch_simplify(search: str, location: str) -> list:
    """
    Fetch from Simplify Jobs GitHub repo.
    WARNING: These jobs have NO descriptions — only title/company/URL.
    The UI will show a 'View Original Posting' link instead.
    """
    URLS = [
        "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json",
        "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json",
    ]
    listings = []
    for url in URLS:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            listings = resp.json()
            if listings:
                break
        except Exception:
            continue

    if not listings:
        return []

    results = []
    for job in listings:
        if not job.get("active", True):
            continue
        title   = job.get("title", "")
        company = job.get("company_name", job.get("company", ""))
        locs    = job.get("locations", [])

        if search and search.lower() not in title.lower() and search.lower() not in company.lower():
            continue
        if location and location.lower() not in " ".join(locs).lower():
            continue

        results.append({
            "id": f"{company}-{title}".replace(" ","-").lower()[:80],
            "title": title,
            "company": company,
            "locations": locs,
            "url": job.get("url", "#"),
            "date_posted": job.get("date_posted", 0),
            "description": "Click 'View Original Posting →' to see the full job description on the company's careers page.",
            "sponsorship": job.get("sponsorship", "Unknown"),
            "terms": job.get("terms", []),
            "source": "simplify"
        })
    return results


# ── High-quality seed data (always available, no API needed) ──────────────────
def get_seed_data() -> list:
    return [
        {
            "id": "google-swe-intern-2026",
            "title": "Software Engineering Intern, BS 2026",
            "company": "Google",
            "locations": ["Mountain View, CA"],
            "url": "https://careers.google.com/jobs/results/?category=ENGINEERING&employment_type=INTERN",
            "date_posted": 1741000000,
            "description": "Build real products used by billions. Work with experienced engineers on Python/Java/Go systems at massive scale. Strong data structures, algorithms, distributed systems, REST APIs, Docker/Kubernetes required.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "microsoft-swe-intern-2026",
            "title": "Software Engineer Intern",
            "company": "Microsoft",
            "locations": ["Redmond, WA"],
            "url": "https://careers.microsoft.com/students/us/en/job/internship",
            "date_posted": 1741000000,
            "description": "Build Azure cloud microservices using Python, Java, C#, Go. REST APIs, Docker, Kubernetes, CI/CD, distributed systems experience required. Full feature ownership in agile teams.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "meta-swe-intern-2026",
            "title": "Software Engineer Intern",
            "company": "Meta",
            "locations": ["Menlo Park, CA"],
            "url": "https://www.metacareers.com/jobs/internships/",
            "date_posted": 1741000000,
            "description": "Large-scale distributed systems, backend infrastructure. Python, C++, Java required. Kafka, Spark, MySQL, Cassandra experience preferred. Strong system design fundamentals essential.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "amazon-sde-intern-2026",
            "title": "SDE Intern (Summer 2026)",
            "company": "Amazon",
            "locations": ["Seattle, WA"],
            "url": "https://www.amazon.jobs/en/jobs?category=software-development&job_type=Internship",
            "date_posted": 1741000000,
            "description": "Production code in Java, Python, Go. Microservices on AWS (EC2, Lambda, S3, DynamoDB). Docker, Kubernetes, CI/CD. Strong data structures, algorithms, system design required.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "openai-research-intern-2026",
            "title": "Research Engineer Intern",
            "company": "OpenAI",
            "locations": ["San Francisco, CA"],
            "url": "https://openai.com/careers#internships",
            "date_posted": 1741000000,
            "description": "LLM training, RLHF, model evaluation in PyTorch. LoRA fine-tuning, RAG pipelines, distributed training (FSDP, DeepSpeed). Strong Python and ML research background required.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "stripe-backend-intern-2026",
            "title": "Backend Engineer Intern",
            "company": "Stripe",
            "locations": ["San Francisco, CA"],
            "url": "https://stripe.com/jobs/search?query=intern",
            "date_posted": 1741000000,
            "description": "Payment infrastructure in Ruby, Python, Go, Java. REST APIs, PostgreSQL, distributed systems, microservices, fault tolerance. Full ownership from design to CI/CD deployment.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "databricks-data-intern-2026",
            "title": "Software Engineer Intern - Data Platform",
            "company": "Databricks",
            "locations": ["San Francisco, CA"],
            "url": "https://www.databricks.com/company/careers/open-positions",
            "date_posted": 1741000000,
            "description": "Spark, Delta Lake, distributed query engines in Scala/Python/Java. Kafka, cloud (AWS/Azure/GCP), large-scale data pipelines, SQL optimization. Distributed systems fundamentals required.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
        {
            "id": "cloudflare-swe-intern-2026",
            "title": "Software Engineer Intern - Distributed Systems",
            "company": "Cloudflare",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://www.cloudflare.com/careers/jobs/",
            "date_posted": 1741000000,
            "description": "Global distributed infrastructure in Go/Rust/Python. Consensus, replication, leader election, fault tolerance. Docker, Kubernetes, Terraform, AWS/GCP experience preferred.",
            "sponsorship": "Does Sponsor", "terms": ["Summer 2026"], "source": "seed"
        },
    ]


# ── Main endpoint ─────────────────────────────────────────────────────────────
@router.get("/")
def get_jobs(
    search: str = "",
    location: str = "",
    limit: int = 50,
    resume_text: str = "",
    ats_threshold: int = 0,
):
    jobs_raw = []
    data_source = "none"

    # Priority 1: JSearch (real LinkedIn/Indeed jobs with full descriptions)
    if RAPIDAPI_KEY:
        jobs_raw = fetch_jsearch(search, location)
        if jobs_raw:
            jobs_raw = [normalize_jsearch_job(j) for j in jobs_raw]
            data_source = "jsearch"

    # Priority 2: Adzuna (free with key, real descriptions)
    if not jobs_raw:
        jobs_raw = fetch_adzuna(search, location)
        if jobs_raw:
            data_source = "adzuna"

    # Priority 3: Simplify Jobs (real companies, no descriptions)
    if not jobs_raw:
        jobs_raw = fetch_simplify(search, location)
        if jobs_raw:
            data_source = "simplify"

    # Priority 4: Seed data (always works, good descriptions)
    if not jobs_raw:
        jobs_raw = get_seed_data()
        data_source = "seed"
        if search:
            jobs_raw = [
                j for j in jobs_raw
                if search.lower() in j["title"].lower()
                or search.lower() in j["company"].lower()
            ]

    # ATS scoring
    resume_keywords = extract_resume_keywords(resume_text) if resume_text else []
    results = []
    for job in jobs_raw:
        score = compute_ats_score(job["title"], job["description"], resume_keywords)
        if resume_keywords and ats_threshold > 0 and score < ats_threshold:
            continue
        matched = [kw for kw in resume_keywords
                   if kw in (job["title"] + " " + job["description"]).lower()]
        results.append({**job, "ats_score": score, "matched_keywords": matched})

    results.sort(key=lambda x: x["ats_score"], reverse=True)

    return {
        "jobs": results[:limit],
        "total": len(results),
        "source": data_source,
        "has_descriptions": data_source != "simplify"
    }
