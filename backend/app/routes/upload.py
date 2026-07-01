import os
import uuid
import json
from flask import Blueprint, request, jsonify
from app import db
from app.models import Resume
from app.services.parser import extract_text
from app.services.skill_extractor import extract_skills
from app.services.ats_scorer import calculate_ats_score

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@upload_bp.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Only PDF and DOCX files are allowed"}), 400

    session_id = request.form.get("session_id", str(uuid.uuid4()))

    saved_filename = f"{uuid.uuid4()}{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, saved_filename)
    file.save(save_path)

    try:
        extracted_text = extract_text(save_path)
    except Exception as e:
        return jsonify({"error": f"Failed to parse file: {str(e)}"}), 500

    skills = extract_skills(extracted_text)
    ats_result = calculate_ats_score(extracted_text, skills)

    resume = Resume(
        session_id=session_id,
        filename=file.filename,
        extracted_text=extracted_text,
        skills_json=json.dumps(skills),
        ats_score=ats_result["total_score"],
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify({
        "id": resume.id,
        "session_id": session_id,
        "filename": resume.filename,
        "extracted_text": extracted_text,
        "skills": skills,
        "ats_score": ats_result["total_score"],
        "ats_breakdown": ats_result["breakdown"],
        "suggestions": ats_result["suggestions"],
    }), 201