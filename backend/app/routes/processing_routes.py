#backend/app/routes/processing_routes.py
import subprocess

from flask import Blueprint, current_app, jsonify, request, send_file, send_from_directory
from app.controllers.noise_controller import process_video_effects
import os
from app.processing.audio_extractor import extract_audio
from app.services.noise_reduction_service import compile_processed_segments,compile_processed_subtitles
processing_bp = Blueprint("processing_bp", __name__)

@processing_bp.route('/media/<path:filename>')
def serve_media(filename):
    # This points to backend/app/storage
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_folder = os.path.join(base_dir, "storage")
    return send_from_directory(media_folder, filename)

# Changed to GET for easier testing
@processing_bp.route("/video/process", methods=["GET"])
def process_video_route():
    return process_video_effects()
@processing_bp.route("/video/preview", methods=["POST"])
def preview_video():
    return process_video_effects(preview=True)
@processing_bp.route("/video/audio/<video_id>", methods=["GET"])
def get_audio(video_id):

    audio_path = os.path.join(
        current_app.config["AUDIO_FOLDER"],
        f"{video_id}.wav"
    )

    return send_file(audio_path)


@processing_bp.route("/video/cut-audio", methods=["GET"])
def cut_audio_route():
    video_id = request.args.get('video_id')
    start = request.args.get('start', type=float)
    end = request.args.get('end', type=float)

    if not video_id or start is None or end is None:
        return jsonify({"error": "Missing parameters"}), 400

    # Folders
    base_storage = r"D:\projects\vedio_voice_setup\backend\app\storage"
    upload_folder = os.path.join(base_storage, "uploads")
    audio_folder = os.path.join(base_storage, "audio")
    
    # Path for the .wav we NEED
    input_path = os.path.join(audio_folder, f"{video_id}.wav")
    output_name = f"{video_id}_clip_{start}_{end}.wav"
    output_path = os.path.join(audio_folder, output_name)

    # 1. If .wav doesn't exist, we must find the .mp4 and extract it
    if not os.path.exists(input_path):
        print(f"DEBUG: .wav missing for {video_id}. Searching for .mp4...")
        
        # FIND THE FILE (Fallback logic like in your service)
        video_path = None
        for f in os.listdir(upload_folder):
            if f.startswith(video_id):
                video_path = os.path.join(upload_folder, f)
                break
        
        if video_path and os.path.exists(video_path):
            print(f"DEBUG: Found video at {video_path}. Extracting audio...")
            try:
                from app.processing.audio_extractor import extract_audio
                extract_audio(video_path, input_path)
            except Exception as e:
                return jsonify({"error": f"Extraction failed: {str(e)}"}), 500
        else:
            print(f"DEBUG: Could not find any file starting with {video_id} in {upload_folder}")
            return jsonify({"error": "Original video file not found on server"}), 404

    # 2. Proceed with cutting
    duration = end - start
    try:
        command = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", input_path,
            "-t", str(duration),
            "-acodec", "pcm_s16le",
            output_path
        ]
        
        import subprocess
        subprocess.run(command, check=True, capture_output=True)
        return send_file(output_path, mimetype="audio/wav")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@processing_bp.route("/video/segment_process", methods=["GET"])
def process_segment_route():
    # Reuse the logic from noise_controller
    return process_video_effects()

@processing_bp.route("/video/compile", methods=["POST"])
def compile_video_route():
    data = request.json
    video_id = data.get("video_id")
    segments = data.get("segments") # List of segment filenames/paths
    
    if not video_id or not segments:
        return jsonify({"error": "Missing video_id or segments"}), 400
        
    try:
        
        download_url = compile_processed_segments(video_id, segments)
        return jsonify({"status": "success", "download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@processing_bp.route("/video/subtitled", methods=["POST"])
def subtitled_video_route():
    data = request.json
    video_id = data.get("video_id")
    subtitles = data.get("subtitles") 
    
    if not video_id or not subtitles:
        return jsonify({"error": "Missing video_id or subtitles"}), 400
        
    try:
        
        download_url = compile_processed_subtitles(video_id, subtitles)
        return jsonify({"status": "success", "download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
