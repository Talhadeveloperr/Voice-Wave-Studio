#backend/app/controllers/upload_controller.py
from flask import request, jsonify
from app.services.video_service import save_video_file


def upload_video():

    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        video_data = save_video_file(file)

        return jsonify({
            "message": "Video uploaded successfully",
            "video_id": video_data["video_id"],
            "video_path": video_data["video_path"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500