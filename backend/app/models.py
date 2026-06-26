from app import db
from datetime import datetime

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    extracted_text = db.Column(db.Text, nullable=True)
    ats_score = db.Column(db.Integer, nullable=True)
    skills_json = db.Column(db.Text, nullable=True)