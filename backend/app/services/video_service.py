#backend/app/services/video_service.py
import uuid
import os
from flask import current_app
from app.utils.file_manager import save_file


def save_video_file(file):

    video_id = str(uuid.uuid4())

    filename = f"{video_id}_{file.filename}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    video_path = os.path.join(upload_folder, filename)

    save_file(file, video_path)

    return {
        "video_id": video_id,
        "video_path": video_path
    }