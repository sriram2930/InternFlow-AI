import requests
from fastapi import APIRouter

router = APIRouter()

SIMPLIFY_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json"

def fetch_listings():
    try:
        response = requests.get(SIMPLIFY_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return get_seed_data()

def get_seed_data():
    return [
        # ── ML / AI ──────────────────────────────────────────────────────────
        {
            "company_name": "Google",
            "title": "Software Engineering Intern – Machine Learning",
            "locations": ["Mountain View, CA"],
            "url": "https://careers.google.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Work on ML infrastructure and model training pipelines at scale. Python, TensorFlow, distributed systems experience preferred. Build tools that power Search, Ads, and YouTube recommendations."
        },
        {
            "company_name": "OpenAI",
            "title": "Research Engineer Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://openai.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Work on LLM training, RLHF, and evaluation infrastructure. Strong Python, PyTorch, and distributed training skills required. Help push the frontier of AI safety and capability research."
        },
        {
            "company_name": "Microsoft",
            "title": "AI/ML Engineering Intern",
            "locations": ["Redmond, WA"],
            "url": "https://careers.microsoft.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build and deploy ML models for Azure AI services. Experience with PyTorch, model optimization, ONNX, and cloud platforms required. Work alongside the Copilot team."
        },
        {
            "company_name": "Netflix",
            "title": "Machine Learning Intern",
            "locations": ["Los Gatos, CA"],
            "url": "https://jobs.netflix.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Improve recommendation systems using collaborative filtering, deep learning, and real-time ML pipelines. Python, Spark, and experimentation frameworks required."
        },
        {
            "company_name": "Snap",
            "title": "ML Research Intern – Computer Vision",
            "locations": ["Santa Monica, CA"],
            "url": "https://snap.com/jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Research and develop computer vision models for AR features in Snapchat. Experience with CNNs, transformers, PyTorch, and real-time inference on mobile devices."
        },
        {
            "company_name": "NVIDIA",
            "title": "Deep Learning Engineer Intern",
            "locations": ["Santa Clara, CA"],
            "url": "https://nvidia.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Develop deep learning frameworks, GPU-accelerated training pipelines, and model optimization techniques. CUDA, TensorRT, PyTorch experience required."
        },
        {
            "company_name": "Anthropic",
            "title": "Research Engineer Intern – LLM Safety",
            "locations": ["San Francisco, CA"],
            "url": "https://anthropic.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Work on interpretability, alignment, and evaluation of large language models. Strong Python, PyTorch, and ML research background required."
        },
        # ── Data Science / Analytics ──────────────────────────────────────────
        {
            "company_name": "Meta",
            "title": "Data Science Intern",
            "locations": ["Menlo Park, CA"],
            "url": "https://metacareers.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Analyze large-scale datasets to drive product decisions across Facebook, Instagram, and WhatsApp. SQL, Python, A/B testing, statistical modeling required."
        },
        {
            "company_name": "Uber",
            "title": "Data Science Intern – Marketplace",
            "locations": ["San Francisco, CA"],
            "url": "https://uber.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Apply ML to pricing, matching, and demand forecasting for the Uber marketplace. Python, SQL, causal inference, and experimentation experience preferred."
        },
        {
            "company_name": "Airbnb",
            "title": "Data Analyst Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://careers.airbnb.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Partner with product and growth teams to analyze user behavior, build dashboards, and run experiments. Strong SQL, Python, Tableau, and A/B testing skills."
        },
        {
            "company_name": "Stripe",
            "title": "Data Scientist Intern – Risk",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://stripe.com/jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build fraud detection and risk scoring models using transaction data. ML, SQL, Python, and knowledge of payments or fintech a plus."
        },
        {
            "company_name": "LinkedIn",
            "title": "Data Science Intern – Feed Ranking",
            "locations": ["Sunnyvale, CA"],
            "url": "https://linkedin.com/jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Improve LinkedIn's feed and notification ranking algorithms. Experience with ML, SQL, Python, and large-scale experimentation platforms."
        },
        # ── Data Engineering ──────────────────────────────────────────────────
        {
            "company_name": "Airbnb",
            "title": "Data Engineering Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://careers.airbnb.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build scalable data pipelines using Spark, Airflow, and Presto. Design data models and ETL workflows to support analytics and ML teams."
        },
        {
            "company_name": "Databricks",
            "title": "Data Engineering Intern",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://databricks.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build features for the Databricks Lakehouse platform. Apache Spark, Delta Lake, Python, and distributed systems knowledge required."
        },
        {
            "company_name": "Snowflake",
            "title": "Data Engineering Intern",
            "locations": ["San Mateo, CA", "Remote"],
            "url": "https://snowflake.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Design and build data infrastructure on the Snowflake cloud data platform. SQL, Python, dbt, and cloud experience preferred."
        },
        # ── Software Engineering ──────────────────────────────────────────────
        {
            "company_name": "Apple",
            "title": "Software Engineer Intern",
            "locations": ["Cupertino, CA"],
            "url": "https://apple.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build software for macOS, iOS, or developer tools. Strong proficiency in Swift, Python, or C++. Passion for quality, performance, and user experience."
        },
        {
            "company_name": "Amazon",
            "title": "Software Development Engineer Intern",
            "locations": ["Seattle, WA", "New York, NY"],
            "url": "https://amazon.jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Design and implement features for Amazon's services at scale. Java, Python, distributed systems, and AWS experience preferred."
        },
        {
            "company_name": "Salesforce",
            "title": "Software Engineer Intern",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://salesforce.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build features for the Salesforce CRM platform and Einstein AI products. Java, JavaScript, Python, and Apex experience."
        },
        # ── Backend ───────────────────────────────────────────────────────────
        {
            "company_name": "Twilio",
            "title": "Backend Engineer Intern",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://twilio.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build APIs and microservices for Twilio's communication platform. Node.js, Java, Go, and REST API design experience preferred."
        },
        {
            "company_name": "DoorDash",
            "title": "Backend Software Engineer Intern",
            "locations": ["San Francisco, CA", "New York, NY"],
            "url": "https://doordash.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build scalable backend systems for DoorDash's logistics and marketplace platform. Python, Java, Kotlin, microservices, and Kafka experience."
        },
        # ── Frontend / Full Stack ─────────────────────────────────────────────
        {
            "company_name": "Figma",
            "title": "Frontend Engineer Intern",
            "locations": ["San Francisco, CA"],
            "url": "https://figma.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build UI components and real-time collaboration features in Figma. React, TypeScript, WebAssembly, and WebGL experience preferred."
        },
        {
            "company_name": "Vercel",
            "title": "Full Stack Engineer Intern",
            "locations": ["Remote"],
            "url": "https://vercel.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Work on the Vercel platform and Next.js framework. React, TypeScript, Node.js, edge computing, and developer tooling experience."
        },
        # ── GenAI ─────────────────────────────────────────────────────────────
        {
            "company_name": "Cohere",
            "title": "GenAI Engineer Intern",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://cohere.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build production GenAI applications using Cohere's LLM APIs. RAG pipelines, LangChain, vector databases, prompt engineering, and Python required."
        },
        {
            "company_name": "Hugging Face",
            "title": "ML Engineer Intern – Generative AI",
            "locations": ["New York, NY", "Remote"],
            "url": "https://huggingface.co/jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Contribute to open-source LLM tools, diffusion models, and the Transformers library. Python, PyTorch, and deep understanding of transformer architectures."
        },
        # ── NLP ───────────────────────────────────────────────────────────────
        {
            "company_name": "Apple",
            "title": "NLP Engineer Intern – Siri",
            "locations": ["Cupertino, CA"],
            "url": "https://apple.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build NLP models for Siri's natural language understanding. Experience with transformer models, BERT, text classification, NER, and PyTorch."
        },
        {
            "company_name": "Grammarly",
            "title": "NLP Research Intern",
            "locations": ["San Francisco, CA", "Remote"],
            "url": "https://grammarly.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Research and develop NLP models for grammar correction, style suggestions, and tone detection. Python, transformers, and computational linguistics experience."
        },
        # ── Quantitative ─────────────────────────────────────────────────────
        {
            "company_name": "Jane Street",
            "title": "Quantitative Research Intern",
            "locations": ["New York, NY"],
            "url": "https://janestreet.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Develop trading strategies and quantitative models. Strong math, statistics, probability, Python/OCaml, and financial markets knowledge."
        },
        {
            "company_name": "Citadel",
            "title": "Quantitative Analyst Intern",
            "locations": ["Chicago, IL", "New York, NY"],
            "url": "https://citadel.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Apply statistical modeling, ML, and data analysis to financial data. Python, R, statistics, econometrics, and finance experience preferred."
        },
        # ── Cloud / DevOps ────────────────────────────────────────────────────
        {
            "company_name": "AWS",
            "title": "Cloud Engineer Intern",
            "locations": ["Seattle, WA", "Austin, TX"],
            "url": "https://amazon.jobs",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Build and operate cloud infrastructure on AWS. Terraform, Kubernetes, Docker, CI/CD, Python, and distributed systems experience required."
        },
        {
            "company_name": "Cloudflare",
            "title": "DevOps / Infrastructure Intern",
            "locations": ["San Francisco, CA", "Austin, TX", "Remote"],
            "url": "https://cloudflare.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Work on globally distributed systems serving millions of requests per second. Go, Rust, Kubernetes, networking, and systems programming experience."
        },
        # ── Research ──────────────────────────────────────────────────────────
        {
            "company_name": "DeepMind",
            "title": "Research Scientist Intern",
            "locations": ["New York, NY"],
            "url": "https://deepmind.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Conduct fundamental AI research in areas including RL, planning, reasoning, and multimodal models. PhD-track or strong research background required."
        },
        {
            "company_name": "IBM Research",
            "title": "Research Engineer Intern – AI",
            "locations": ["New York, NY", "Remote"],
            "url": "https://ibm.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Research AI and ML topics including foundation models, enterprise AI, and trustworthy AI. Python, PyTorch, and research publication experience."
        },
        # ── Product Management ────────────────────────────────────────────────
        {
            "company_name": "Google",
            "title": "Associate Product Manager Intern",
            "locations": ["Mountain View, CA", "New York, NY"],
            "url": "https://careers.google.com",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Define product strategy and roadmap for Google products. Strong analytical thinking, user empathy, SQL, and cross-functional collaboration skills."
        },
        {
            "company_name": "Atlassian",
            "title": "Product Manager Intern",
            "locations": ["Austin, TX", "Remote"],
            "url": "https://atlassian.com/careers",
            "active": True, "date_posted": 1710000000,
            "terms": ["Summer 2025"], "sponsorship": "Does Sponsor",
            "description": "Drive product development for Jira and Confluence. Data-driven decision-making, user research, roadmapping, and Agile/Scrum experience."
        },
    ]


@router.get("/")
def get_jobs(search: str = "", location: str = "", limit: int = 50):
    listings = fetch_listings()

    results = []
    for job in listings:
        title       = job.get("title", "")
        company     = job.get("company_name", job.get("company", ""))
        locations   = job.get("locations", [])
        description = job.get("description", "")
        active      = job.get("active", True)

        if not active:
            continue

        # Search filter — match against title, company, OR description
        if search:
            s = search.lower()
            haystack = (title + " " + company + " " + description).lower()
            if s not in haystack:
                continue

        # Location filter — strip state suffix for broader matching
        if location and location.lower() not in ("any location (usa)", ""):
            loc_str = " ".join(locations).lower()
            # Try city-only match (e.g. "san francisco" matches "San Francisco, CA")
            loc_key = location.lower().split(",")[0].strip()
            if loc_key not in loc_str and "remote" not in loc_str:
                continue

        # Include first location in ID to prevent duplicates for same role in multiple cities
        loc_key    = (locations[0] if locations else "").replace(" ", "-").replace(",", "").lower()
        results.append({
            "id":          (company + "-" + title + "-" + loc_key).replace(" ", "-").lower()[:100],
            "title":       title,
            "company":     company,
            "locations":   locations,
            "url":         job.get("url", "#"),
            "date_posted": job.get("date_posted", 0),
            "sponsorship": job.get("sponsorship", ""),
            "terms":       job.get("terms", []),
            "description": description,
        })

    return {"jobs": results[:limit], "total": len(results)}
