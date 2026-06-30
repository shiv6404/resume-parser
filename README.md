# Automated Resume Parser

A system that extracts and categorizes candidate information (name, email,
phone, skills, education) from PDF resumes and stores it in a searchable
SQLite database, with a simple web dashboard for upload and search.

## Features
- Upload PDF resumes through a web interface
- Extracts name, email, phone number, skills, and education using
  regex + keyword matching (spaCy-style heuristics, no heavy NLP model needed)
- Stores parsed candidates in a local SQLite database
- Search candidates by skill keyword
- Dark-themed dashboard UI

## Tech Stack
Python, Flask, pdfplumber, SQLite

## Project Structure
```
resume-parser/
├── app.py                # Flask routes (upload + search)
├── resume_parser.py      # Extraction logic + database layer
├── templates/
│   └── index.html        # Dashboard UI
├── sample_resumes/       # Put sample PDFs here for testing
├── uploads/               # Uploaded resumes are saved here
├── requirements.txt
└── README.md
```

## Setup & Run
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000**, upload a PDF resume, and search by skill
(e.g. "python", "sql").

## How it works
1. `pdfplumber` extracts raw text from the uploaded PDF.
2. The first valid name-like line (no digits/@) is taken as the candidate name.
3. Regex patterns extract email and phone number.
4. The text is checked against curated skill and degree keyword lists using
   word-boundary matching (avoids false positives like matching "C" inside
   "Science").
5. Parsed data is saved to `resumes.db` and is searchable from the dashboard.

## Example
```python
from resume_parser import parse_resume

data = parse_resume("sample_resumes/sample.pdf")
print(data)
# {'name': 'Rohit Sharma', 'email': 'rohit.sharma@example.com',
#  'phone': '9876543210', 'skills': ['python', 'flask', 'sql', ...],
#  'education': ['b.tech']}
```

## Future Improvements
- Replace keyword matching with spaCy NER for more robust name/entity extraction
- Support .docx resumes
- Add candidate ranking based on job description match

---
Built as part of a Data Science Internship project.
