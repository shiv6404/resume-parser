"""
Flask web app for the Automated Resume Parser.
Run with: python app.py
Then open http://127.0.0.1:5000 to upload resumes and search candidates.
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from resume_parser import init_db, parse_resume, save_candidate, search_candidates

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET"])
def index():
    skill = request.args.get("skill", "")
    candidates = search_candidates(skill)
    return render_template("index.html", candidates=candidates, skill=skill)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("resume")
    if file and file.filename.lower().endswith(".pdf"):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        data = parse_resume(path)
        save_candidate(data)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
