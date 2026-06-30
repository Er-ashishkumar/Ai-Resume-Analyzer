import json
import os
import re

SKILLS_DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "skills_db.json"
)


def load_skills_db():
    with open(SKILLS_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_skills(text):
    skills_db = load_skills_db()
    text_lower = text.lower()

    found_skills = {}

    for category, skills_list in skills_db.items():
        matched = []
        for skill in skills_list:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_lower):
                matched.append(skill)
        if matched:
            found_skills[category] = matched

    return found_skills