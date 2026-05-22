#backend/app/controllers/noise_controller.py
from flask import request, jsonify
from app.services.noise_reduction_service import process_video

def process_video_effects():
    # Get parameters from URL query: ?video_id=...&noiseLevel=50
    video_id = request.args.get("video_id")
    clip_start = request.args.get("clipStart")
    clip_end = request.args.get('clipEnd')
    params = {
        "noise": int(request.args.get("noiseLevel", 0)),
        "bass": int(request.args.get("bassLevel", 0)),
        "analog_echo": int(request.args.get("analogLevel", 0)),
        "basic_echo": int(request.args.get("basicLevel", 0)),
        "standard_echo": int(request.args.get("standardLevel", 0)),
        "flutter_echo": int(request.args.get("flutterLevel", 0)),
        "reverb_echo": int(request.args.get("reverbLevel", 0)),
        "clip_start": clip_start,
        "clip_end": clip_end
    }

    if not video_id:
        return jsonify({"error": "video_id is required"}), 400

    try:
        # Service now returns a web-friendly URL path
        video_url = process_video(
            video_id=video_id,
            noise=params["noise"],
            bass=params["bass"],
            analog_echo=params["analog_echo"],
            basic_echo=params["basic_echo"],
            standard_echo=params["standard_echo"],
            flutter_echo=params["flutter_echo"],
            reverb_echo=params["reverb_echo"],
            clip_start=params["clip_start"],
            clip_end=params["clip_end"]
        )

        return jsonify({
            "status": "success",
            "processed_video_url": video_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500