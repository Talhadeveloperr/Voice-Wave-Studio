# backend/app/__init__.py
from flask import Flask
from .routes.video_routes import video_bp
from .config import Config
from .routes.processing_routes import processing_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(video_bp, url_prefix="/api")
    app.register_blueprint(processing_bp, url_prefix="/api")

    return app