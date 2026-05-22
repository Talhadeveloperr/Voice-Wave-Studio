#backend/app/processing/audio_extractor.py
import subprocess
def extract_audio(video_path, audio_output_path, start=None, end=None):
    command = ["ffmpeg", "-y"]
    if start and end:
        duration = float(end) - float(start)
        command.extend(["-ss", str(start), "-t", str(duration)])
    
    command.extend(["-i", video_path, "-vn", "-ar", "44100", "-ac", "2", audio_output_path])
    subprocess.run(command, check=True, shell=True)
"""
def extract_audio(video_path, audio_path):

    command = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        audio_path,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
"""    