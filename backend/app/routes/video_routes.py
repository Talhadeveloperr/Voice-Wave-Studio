#backend/app/routes/video_routes.py
from flask import Blueprint
from app.controllers.upload_controller import upload_video

video_bp = Blueprint("video_bp", __name__)

@video_bp.route("/video/upload", methods=["POST"])
def upload():
    return upload_video()