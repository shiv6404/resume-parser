"""
Automated Resume Parser
------------------------
Extracts candidate details (name, email, phone, skills, education)
from PDF resumes and stores them in a local SQLite database for search.
"""

import re
import sqlite3
import pdfplumber

DB_PATH = "resumes.db"

# A reasonably broad skill keyword list — extend as needed
SKILL_KEYWORDS = [
    "python", "java", "c++", "c", "javascript", "html", "css", "sql",
    "flask", "django", "react", "node.js", "node", "machine learning",
    "deep learning", "nlp", "pandas", "numpy", "tensorflow", "pytorch",
    "scikit-learn", "power bi", "excel", "tableau", "aws", "azure",
    "docker", "kubernetes", "git", "mongodb", "mysql", "postgresql",
    "data analysis", "data science", "rest api", "fastapi", "linux",
    "spring boot", "android", "kotlin", "r", "matlab", "communication",
    "leadership", "teamwork", "project management",
]

DEGREE_KEYWORDS = [
    "b.tech", "btech", "b.e", "be ", "m.tech", "mtech", "bachelor",
    "master", "msc", "bsc", "mca", "bca", "phd", "diploma", "12th", "10th",
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\d{10}")


def extract_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_name(text: str) -> str:
    """Heuristic: the first non-empty line that looks like a name
    (no digits, no @, 2-4 words, reasonable length)."""
    for line in text.split("\n")[:6]:
        line = line.strip()
        if not line or "@" in line or any(ch.isdigit() for ch in line):
            continue
        words = line.split()
        if 1 <= len(words) <= 4 and len(line) < 50:
            return line.title()
    return "Unknown"


def extract_email(text: str) -> str:
    m = EMAIL_RE.search(text)
    return m.group(0) if m else ""


def extract_phone(text: str) -> str:
    m = PHONE_RE.search(text)
    return m.group(0) if m else ""


def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for s in SKILL_KEYWORDS:
        pattern = r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])"
        if re.search(pattern, text_lower):
            found.append(s)
    return sorted(set(found))


def extract_education(text: str) -> list:
    text_lower = text.lower()
    found = [d for d in DEGREE_KEYWORDS if d in text_lower]
    return sorted(set(found))


def parse_resume(pdf_path: str) -> dict:
    text = extract_text(pdf_path)
    return {
        "file": pdf_path,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
    }


# ------------------- Database layer -------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_candidate(data: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO candidates (file, name, email, phone, skills, education) VALUES (?, ?, ?, ?, ?, ?)",
        (data["file"], data["name"], data["email"], data["phone"],
         ", ".join(data["skills"]), ", ".join(data["education"]))
    )
    conn.commit()
    conn.close()


def search_candidates(skill: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if skill:
        cur.execute("SELECT * FROM candidates WHERE skills LIKE ?", (f"%{skill}%",))
    else:
        cur.execute("SELECT * FROM candidates")
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
    print("Place resume PDFs in the 'sample_resumes' folder and run app.py to parse + search them.")
