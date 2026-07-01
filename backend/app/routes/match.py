from flask import Blueprint, request, jsonify
from app.models import Resume
from app.services.jd_matcher import calculate_match, find_missing_keywords
import json

match_bp = Blueprint("match", __name__)


@match_bp.route("/match", methods=["POST"])
def match_resume():
    data = request.get_json()

    if not data or "resume_id" not in data or "job_description" not in data:
        return jsonify({"error": "resume_id and job_description are required"}), 400

    resume_id = data["resume_id"]
    job_description = data["job_description"]

    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    match_percentage = calculate_match(resume.extracted_text, job_description)

    skills = json.loads(resume.skills_json) if resume.skills_json else {}
    keyword_comparison = find_missing_keywords(skills, job_description)

    return jsonify({
        "resume_id": resume_id,
        "match_percentage": match_percentage,
        "skills_matching_jd": keyword_comparison["skills_matching_jd"],
        "resume_skills_not_in_jd": keyword_comparison["resume_skills_not_in_jd"],
    }), 200