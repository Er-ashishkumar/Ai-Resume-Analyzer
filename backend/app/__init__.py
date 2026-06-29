from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../resume_analyzer.db"
    db.init_app(app)

    from app.routes.health import health_bp
    from app.routes.upload import upload_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)

    from app import models

    with app.app_context():
        db.create_all()

    return app