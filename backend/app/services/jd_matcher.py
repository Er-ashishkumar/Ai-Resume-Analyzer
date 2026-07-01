from sentence_transformers import SentenceTransformer, util

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def calculate_match(resume_text, job_description):
    model = get_model()

    embeddings = model.encode(
        [resume_text, job_description], convert_to_tensor=True
    )
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    match_percentage = round(similarity * 100, 2)

    return match_percentage


def find_missing_keywords(resume_skills, job_description):
    jd_lower = job_description.lower()

    all_resume_skills = []
    for skill_list in resume_skills.values():
        all_resume_skills.extend(skill_list)

    matched_in_jd = [s for s in all_resume_skills if s.lower() in jd_lower]
    not_in_jd = [s for s in all_resume_skills if s.lower() not in jd_lower]

    return {
        "skills_matching_jd": matched_in_jd,
        "resume_skills_not_in_jd": not_in_jd,
    }