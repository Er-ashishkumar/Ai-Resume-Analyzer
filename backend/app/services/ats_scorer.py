import re


def score_formatting(text):
    """Check for presence of standard resume sections and basic structure."""
    score = 0
    max_score = 25

    sections = ["education", "experience", "skills", "project"]
    found_sections = sum(1 for s in sections if s in text.lower())
    score += min(found_sections * 5, 20)

    has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text))
    has_phone = bool(re.search(r"(\+?\d[\d\-\s]{8,}\d)", text))
    if has_email:
        score += 3
    if has_phone:
        score += 2

    return min(score, max_score)


def score_keywords(skills):
    """Score based on number of skills found across categories."""
    max_score = 30
    total_skills = sum(len(v) for v in skills.values())
    score = min(total_skills * 2, max_score)
    return score


def score_education(text):
    max_score = 20
    text_lower = text.lower()
    keywords = [
        "bachelor", "b.tech", "btech", "b.e", "master", "m.tech",
        "university", "college", "degree", "school"
    ]
    matches = sum(1 for k in keywords if k in text_lower)
    score = min(matches * 5, max_score)
    return score


def score_experience(text):
    max_score = 25
    text_lower = text.lower()
    keywords = [
        "experience", "internship", "intern", "project", "developed",
        "built", "implemented", "designed", "created"
    ]
    matches = sum(1 for k in keywords if k in text_lower)
    score = min(matches * 3, max_score)
    return score


def generate_suggestions(formatting, keywords, education, experience):
    suggestions = []

    if formatting < 15:
        suggestions.append(
            "Add clear section headings like Education, Experience, and Skills."
        )
    if keywords < 15:
        suggestions.append(
            "Include more relevant technical skills and keywords."
        )
    if education < 10:
        suggestions.append(
            "Make sure your education details are clearly listed."
        )
    if experience < 10:
        suggestions.append(
            "Add more detail about your projects, internships, or work experience."
        )
    if not suggestions:
        suggestions.append("Your resume covers the key sections well.")

    return suggestions


def calculate_ats_score(text, skills):
    formatting = score_formatting(text)
    keywords = score_keywords(skills)
    education = score_education(text)
    experience = score_experience(text)

    total = formatting + keywords + education + experience

    suggestions = generate_suggestions(formatting, keywords, education, experience)

    return {
        "total_score": total,
        "breakdown": {
            "formatting": formatting,
            "keywords": keywords,
            "education": education,
            "experience": experience,
        },
        "suggestions": suggestions,
    }