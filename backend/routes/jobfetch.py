"""
jobfetch.py - Universal JD Fetcher
Based on actual API testing:
- Lever: content field is a STRING like "<li>text</li><li>text</li>"
- Greenhouse: content field is double-encoded HTML string
- Others: use Jina.ai renderer
"""
import requests
import re
from fastapi import APIRouter
from pydantic import BaseModel
from urllib.parse import urlparse

router = APIRouter()


class FetchRequest(BaseModel):
    url: str


# ── Skip these section headers ────────────────────────────────────────────────
SKIP_KW = [
    "what we offer", "we offer", "benefits", "perks",
    "compensation", "salary", "about the company", "about us",
    "who we are", "our culture", "our values", "why join",
    "life at", "equal opportunity", "diversity", "eeo",
    "apply now", "how to apply", "privacy", "cookie",
]

# ── Keywords making a bullet relevant ────────────────────────────────────────
RELEVANT_KW = [
    "python", "java", "javascript", "c++", "c#", "go", "golang",
    "rust", "scala", "sql", "bash", "r ", "matlab", "typescript",
    "aws", "gcp", "azure", "cloud", "docker", "kubernetes",
    "terraform", "jenkins", "git", "linux", "ci/cd",
    "machine learning", "deep learning", "ml", "ai", "nlp", "llm",
    "pytorch", "tensorflow", "pandas", "numpy", "spark", "kafka",
    "database", "postgresql", "mysql", "mongodb", "redis",
    "api", "rest", "microservices", "distributed", "algorithms",
    "data structures", "system design", "backend", "frontend",
    "experience", "degree", "bachelor", "master", "phd",
    "years", "knowledge", "proficiency", "familiar", "strong",
    "required", "preferred", "minimum", "skills", "ability",
    "develop", "design", "build", "implement", "optimize",
    "analyze", "collaborate", "contribute", "research",
    "programming", "software", "engineering", "computer science",
    "mathematics", "statistics", "quantitative", "analytical",
    "xgboost", "lightgbm", "causal", "verilog", "vhdl", "fpga",
    "compiler", "risc", "processor", "hardware", "parallel",
    "gpa", "university", "coding", "problem solving",
]


def decode_html(text: str) -> str:
    """Decode HTML entities."""
    pairs = [
        ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
        ('&nbsp;', ' '), ('&#39;', "'"), ('&quot;', '"'),
        ('&rsquo;', "'"), ('&lsquo;', "'"),
        ('&rdquo;', '"'), ('&ldquo;', '"'),
        ('&ndash;', '-'), ('&mdash;', '-'),
        ('&bull;', '•'), ('&hellip;', '...'),
        ('&#x27;', "'"), ('&#x2F;', '/'),
        ('&apos;', "'"),
    ]
    for entity, char in pairs:
        text = text.replace(entity, char)
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'&#\d+;', '', text)
    return text


def strip_tags(html: str) -> str:
    """Remove all HTML tags and decode entities."""
    html = decode_html(html)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s{2,}', ' ', html)
    return html.strip()


def extract_li_items(html_string: str) -> list:
    """
    Extract all <li> items from an HTML string.
    Handles: <li>text</li>, <li class="...">text</li>
    """
    # Decode entities first (handles double-encoded HTML)
    decoded = decode_html(html_string)
    # Extract li content
    items = re.findall(r'<li[^>]*>(.*?)</li>', decoded, flags=re.DOTALL)
    result = []
    for item in items:
        text = strip_tags(item).strip()
        if text and len(text) >= 2:
            result.append(text)
    return result


def html_to_plain(html: str) -> str:
    """Convert HTML to plain text with structure preserved."""
    html = decode_html(html)
    html = re.sub(r'<li[^>]*>', '\n• ', html, flags=re.IGNORECASE)
    html = re.sub(r'</li>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>',
                  r'\n\1\n', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'</?p[^>]*>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    html = re.sub(r' {2,}', ' ', html)
    return html.strip()


def should_skip(header: str) -> bool:
    hl = header.lower()
    return any(kw in hl for kw in SKIP_KW)


def is_relevant(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in RELEVANT_KW)


def format_result(sections: list) -> str:
    parts = []
    for sec in sections:
        if not sec.get("bullets"):
            continue
        h = sec["header"].strip()
        parts.append(f"\n{h}\n{'─' * min(len(h), 55)}")
        for b in sec["bullets"]:
            parts.append(f"• {b}")
    return '\n'.join(parts).strip()


# ─────────────────────────────────────────────────────────────────────────────
# LEVER
# Confirmed: content is a STRING "<li>text</li><li>text</li>"
# ─────────────────────────────────────────────────────────────────────────────
def fetch_lever(url: str) -> str:
    # Strip /apply and any query params
    url = re.sub(r'/apply(/.*)?$', '', url.strip())
    url = url.split('?')[0]

    match = re.search(r'jobs\.lever\.co/([^/?#\s]+)/([a-f0-9\-]{30,})', url)
    if not match:
        return ""

    company = match.group(1)
    job_id  = match.group(2)
    api_url = f"https://api.lever.co/v0/postings/{company}/{job_id}"

    try:
        resp = requests.get(
            api_url, timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if resp.status_code != 200:
            return ""

        data = resp.json()
        lists = data.get("lists", [])
        sections = []

        for lst in lists:
            header  = strip_tags(lst.get("text") or "").strip()
            content = lst.get("content") or ""

            if not header:
                continue

            # Skip benefits/company sections
            if should_skip(header):
                continue

            # content is a STRING of HTML — extract <li> items
            if isinstance(content, str):
                bullets = extract_li_items(content)
            elif isinstance(content, list):
                # Rare case: list of strings
                combined = "".join(str(x) for x in content)
                bullets = extract_li_items(combined)
                if not bullets:
                    bullets = [strip_tags(str(x)) for x in content
                               if strip_tags(str(x)) and len(strip_tags(str(x))) > 3]
            else:
                bullets = []

            if bullets:
                sections.append({"header": header, "bullets": bullets})

        result = format_result(sections)

        # Fallback to descriptionPlain if sections empty
        if len(result) < 100:
            plain = data.get("descriptionPlain", "") or ""
            if plain:
                result = extract_from_plain_text(plain)

        return result

    except Exception as e:
        print(f"Lever error: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# GREENHOUSE
# Confirmed: content is double-encoded HTML "&lt;div&gt;&lt;p&gt;..."
# ─────────────────────────────────────────────────────────────────────────────
def fetch_greenhouse(url: str) -> str:
    match = re.search(
        r'(?:boards|job-boards)\.greenhouse\.io/([^/?#\s]+)/jobs/(\d+)', url
    )
    if not match:
        return ""

    company = match.group(1)
    job_id  = match.group(2)
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs/{job_id}"

    try:
        resp = requests.get(
            api_url, timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if resp.status_code != 200:
            return ""

        data = resp.json()
        raw = data.get("content", "")
        if not raw:
            return ""

        # Decode double-encoded HTML: &lt;li&gt; → <li>
        decoded_once = decode_html(raw)

        # Convert HTML to plain text
        plain = html_to_plain(decoded_once)

        result = extract_from_plain_text(plain)

        if len(result) < 150:
            result = plain[:4000]

        return result

    except Exception as e:
        print(f"Greenhouse error: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# JINA.AI for all other URLs
# ─────────────────────────────────────────────────────────────────────────────
def fetch_via_jina(url: str) -> str:
    try:
        resp = requests.get(
            f"https://r.jina.ai/{url}",
            headers={
                "Accept": "text/plain",
                "X-Return-Format": "text",
                "X-Remove-Selector": "header,nav,footer,.cookie-notice,.banner",
                "X-Timeout": "25",
            },
            timeout=30
        )
        if resp.status_code == 200 and len(resp.text) > 100:
            return resp.text
    except Exception:
        pass
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# EXTRACT JD SECTIONS FROM PLAIN TEXT
# ─────────────────────────────────────────────────────────────────────────────
JD_HEADER_KW = [
    "responsibilities", "what you'll do", "what you will do",
    "requirements", "qualifications", "experience & qualifications",
    "skills", "looking for", "you have", "you bring",
    "nice to have", "bonus", "preferred", "minimum",
    "technical", "must have", "duties", "about you",
    "ideal candidate", "quantitative abilities",
    "you will", "we need", "we require",
]


def has_bullets_near(lines: list, idx: int, window: int = 6) -> bool:
    for j in range(idx + 1, min(idx + window, len(lines))):
        s = lines[j].strip()
        if s and s[0] in ('•', '-', '*', '–'):
            return True
        if s and re.match(r'^\d+[\.\)]\s', s):
            return True
        if s and len(s) > 25:
            break
    return False


def is_bullet_line(line: str) -> bool:
    s = line.strip()
    return bool(s and (
        s[0] in ('•', '-', '*', '–', '◦', '▪') or
        re.match(r'^\d+[\.\)]\s+\S', s)
    ))


def strip_bullet_char(line: str) -> str:
    s = line.strip()
    s = re.sub(r'^[•\-\*–◦▪]\s*', '', s)
    s = re.sub(r'^\d+[\.\)]\s+', '', s)
    return s.strip()


def extract_from_plain_text(text: str) -> str:
    lines = text.split('\n')

    # Pass 1: Known JD section headers
    sections, current, stopped = [], None, False
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        sl = s.lower()

        if should_skip(s) and sections:
            stopped = True
        if stopped:
            continue

        is_jd = any(kw in sl for kw in JD_HEADER_KW) and len(s) < 160
        if is_jd and (has_bullets_near(lines, i) or s.endswith(':')):
            current = {"header": s.rstrip(':'), "bullets": []}
            sections.append(current)
            continue

        if current and is_bullet_line(s):
            b = strip_bullet_char(s)
            if b and len(b) > 5:
                current["bullets"].append(b)

    result = format_result([x for x in sections if x["bullets"]])
    if len(result) >= 200:
        return result

    # Pass 2: Any header followed by bullets
    sections2, current2, stopped2 = [], None, False
    SKIP_NAV = {'home', 'menu', 'search', 'contact', 'careers',
                'jobs', 'back', 'next', 'apply', 'login'}
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if should_skip(s) and sections2:
            stopped2 = True
        if stopped2:
            continue
        if (len(s) < 160 and not is_bullet_line(s) and len(s) > 10
                and has_bullets_near(lines, i)
                and s.strip(':').strip().lower() not in SKIP_NAV):
            current2 = {"header": s.rstrip(':'), "bullets": []}
            sections2.append(current2)
            continue
        if current2 and is_bullet_line(s):
            b = strip_bullet_char(s)
            if b and len(b) > 5 and is_relevant(b):
                current2["bullets"].append(b)

    result2 = format_result([x for x in sections2 if x["bullets"]])
    if len(result2) >= 150:
        return result2

    # Pass 3: All relevant bullets
    bullets, stopped3 = [], False
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if should_skip(s) and len(bullets) > 3:
            stopped3 = True
        if stopped3:
            continue
        if is_bullet_line(s):
            b = strip_bullet_char(s)
            if b and len(b) > 5 and is_relevant(b):
                bullets.append(b)

    if bullets:
        return format_result([{"header": "Requirements & Skills", "bullets": bullets}])
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def fetch_jd(url: str) -> tuple:
    url = url.strip()
    if not url or url == '#':
        return "", "❌ No URL provided."

    domain = urlparse(url).netloc
    url_lower = url.lower()
    result = ""

    if 'lever.co' in url_lower:
        result = fetch_lever(url)
        if not result:
            raw = fetch_via_jina(url)
            if raw:
                result = extract_from_plain_text(raw)

    elif 'greenhouse.io' in url_lower:
        result = fetch_greenhouse(url)
        if len(result) < 200:
            raw = fetch_via_jina(url)
            if raw:
                jina_r = extract_from_plain_text(raw)
                if len(jina_r) > len(result):
                    result = jina_r

    else:
        raw = fetch_via_jina(url)
        if raw:
            result = extract_from_plain_text(raw)

    if not result or len(result) < 100:
        return "", (
            f"⚠️ Could not auto-extract JD from {domain}.\n\n"
            "Please paste manually:\n"
            "1. Open job page in browser\n"
            "2. Ctrl+A → Ctrl+C\n"
            "3. Paste in the box below"
        )

    result = re.sub(r'\n{3,}', '\n\n', result).strip()
    return result, f"✅ JD extracted ({len(result)} chars) from {domain}"


# ─────────────────────────────────────────────────────────────────────────────
# API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/fetch-jd")
def fetch_job_description(req: FetchRequest):
    text, message = fetch_jd(req.url.strip())
    return {"success": bool(text), "text": text, "message": message}


@router.post("/extract-projects")
def extract_projects_from_resume(body: dict):
    resume_text = body.get("resume_text", "")
    if not resume_text:
        return {"projects": []}

    projects = []

    proj_match = re.search(
        r"(academic projects?|projects?)(.*?)"
        r"(professional experience|work experience|skills|education|certifications|\Z)",
        resume_text, flags=re.IGNORECASE | re.DOTALL
    )
    if proj_match:
        for entry in re.split(
            r'\n(?=[A-Z][^\n]{5,80}(?:\s*[–\-]\s*|\s*\(|\s+(?:'
            r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})))',
            proj_match.group(2)
        ):
            entry = entry.strip()
            if len(entry) < 30:
                continue
            lines = [l.strip() for l in entry.splitlines() if l.strip()]
            if not lines:
                continue
            name = re.sub(
                r'[\-–]?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*$',
                '', lines[0]).strip()
            name = re.sub(
                r'\s*(Research Associate|Course Project|Capstone).*$',
                '', name, flags=re.IGNORECASE).strip()
            desc = " ".join(lines[1:])[:600]
            if name and 5 < len(name) < 100:
                projects.append({"name": name, "description": desc,
                                  "source": "resume_projects"})

    exp_match = re.search(
        r"(professional experience|work experience|experience)(.*?)"
        r"(academic projects?|education|skills|certifications|\Z)",
        resume_text, flags=re.IGNORECASE | re.DOTALL
    )
    if exp_match:
        for entry in re.split(
            r'\n(?=[A-Z][^\n]{5,100}(?:,\s*[A-Z]|–|-)\s*(?:[A-Z][a-zA-Z]+|[A-Z]{2,}))',
            exp_match.group(2)
        ):
            entry = entry.strip()
            if len(entry) < 50:
                continue
            lines = [l.strip() for l in entry.splitlines() if l.strip()]
            if not lines:
                continue
            parts = re.split(r',\s*', lines[0])
            if len(parts) >= 2:
                company = re.sub(
                    r'\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*$',
                    '', parts[2] if len(parts) > 2 else '').strip()
                name = f"{parts[0].strip()} — {parts[1].strip()}"
                if company:
                    name += f" @ {company}"
            else:
                name = re.sub(
                    r'\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*$',
                    '', lines[0]).strip()
            desc = " ".join(lines[1:])[:600]
            if name and len(name) > 5 and desc:
                projects.append({"name": name[:100], "description": desc,
                                  "source": "resume_experience"})

    seen, unique = set(), []
    for p in projects:
        key = p["name"].lower()[:40]
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return {"projects": unique[:15]}
