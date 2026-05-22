#backend/app/processing/video_merger.py
import subprocess
def merge_audio_video(video_path, audio_path, output_path, start=None, end=None):
    command = ["ffmpeg", "-y"]
    if start and end:
        duration = float(end) - float(start)
        command.extend(["-ss", str(start), "-t", str(duration)])
    
    command.extend([
        "-i", video_path, 
        "-i", audio_path, 
        "-map", "0:v:0", "-map", "1:a:0", 
        "-c:v", "copy", "-c:a", "aac", output_path
    ])
    subprocess.run(command, check=True, shell=True)
"""
def merge_audio_video(video_path, audio_path, output_path):

    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


"""    