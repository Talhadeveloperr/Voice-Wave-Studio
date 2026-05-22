#backend/app/services/noise_reduction_service.py
import os
from app.processing.audio_extractor import extract_audio
from app.processing.noise_reducer import apply_audio_effects
from app.processing.video_merger import merge_audio_video
import subprocess
import datetime

def process_video(video_id, noise, bass, analog_echo, basic_echo, standard_echo, flutter_echo, reverb_echo,clip_start=None, clip_end=None):
    # EXACT ABSOLUTE PATH based on your dir output
    upload_folder = r"D:\projects\vedio_voice_setup\backend\app\storage\uploads"
    
    # Deriving other folders from the same base
    base_storage = r"D:\projects\vedio_voice_setup\backend\app\storage"
    audio_folder = os.path.join(base_storage, "audio")
    processed_folder = os.path.join(base_storage, "processed")

    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    # Validate file existence manually first
    # We check if video_id already has .mp4 or needs it
    video_file = video_id if video_id.endswith('.mp4') else f"{video_id}.mp4"
    video_path = os.path.join(upload_folder, video_file)

    print(f"--- DEBUGGING ---")
    print(f"Target Path: {video_path}")
    
    if not os.path.exists(video_path):
        # Fallback: search for start of string if exact name fails
        found = False
        for f in os.listdir(upload_folder):
            if f.startswith(video_id):
                video_path = os.path.join(upload_folder, f)
                video_file = f
                found = True
                break
        if not found:
            raise Exception(f"File not found. Searched for: {video_id} in {upload_folder}")

    print(f"File confirmed at: {video_path}")

    base_id = video_id.split('.')[0]
    suffix = f"_seg_{clip_start}_{clip_end}" if clip_start else "_full"
    
    audio_path = os.path.join(audio_folder, f"{base_id}{suffix}.wav")
    clean_audio = os.path.join(audio_folder, f"{base_id}{suffix}_clean.wav")
    output_video_name = f"{base_id}{suffix}_processed.mp4"
    output_video_path = os.path.join(processed_folder, output_video_name)
    profile_path = None
    if clip_start is not None and clip_end is not None:
        profile_name = f"{video_id}_clip_{clip_start}_{clip_end}.wav"
        potential_profile = os.path.join(audio_folder, profile_name)
        if os.path.exists(potential_profile):
            profile_path = potential_profile

    # --- THE SUBPROCESS STEPS ---
    # Each of these calls FFmpeg. If FFmpeg isn't in PATH, WinError 2 happens here.
    extract_audio(video_path, audio_path, clip_start, clip_end)

    # 2. Handle Noise (TEMPORARILY DISABLE DEEPFILTER)
    # Even if noise > 30, we use audio_path because deepFilter isn't installed yet
    source_for_effects = audio_path 
    
    # 3. Apply Effects (FFmpeg will handle noise reduction here)
    apply_audio_effects(audio_path, clean_audio, noise, bass, analog_echo, 
                        basic_echo, standard_echo, flutter_echo, reverb_echo)

    # 4. Merge back
    merge_audio_video(video_path, clean_audio, output_video_path, clip_start, clip_end)

    

    # --- RETURN URL FORMAT ---
    # Result: http://localhost:5000/api/media/processed/filename.mp4
    # (Assuming your blueprint prefix is /api)
    #f"http://localhost:5000/api/processing_bp/media/{output_video_name}"
    return f"http://localhost:5000/api/media/processed/{output_video_name}"



def compile_processed_segments(video_id, segments):
    processed_dir = r"D:\projects\vedio_voice_setup\backend\app\storage\processed"
    uploads_dir = r"D:\projects\vedio_voice_setup\backend\app\storage\uploads"
    
    video_file = video_id if video_id.endswith('.mp4') else f"{video_id}.mp4"
    original_video_path = os.path.join(uploads_dir, video_file)

    if not os.path.exists(original_video_path):
        # Search fallback logic remains the same
        for f in os.listdir(uploads_dir):
            if f.startswith(video_id):
                original_video_path = os.path.join(uploads_dir, f)
                break
        else:
            raise Exception(f"Source file not found: {video_id}")

    base_id = video_id.split('.')[0]
    final_output_path = os.path.join(processed_dir, f"{base_id}_final_master.mp4")
    concat_file_path = os.path.join(processed_dir, f"{base_id}_concat.txt")

    try:
        with open(concat_file_path, "w") as f:
            for seg in segments:
                index = seg.get("index")
                start = seg.get("start")
                end = seg.get("end")
                url = seg.get("url")
                is_edited = seg.get("is_edited", False)

                # We create a "ready-to-concat" version of every segment
                temp_segment_path = os.path.join(processed_dir, f"ready_{index}_{base_id}.mp4")

                if is_edited and url:
                    # Input is your already-processed segment
                    raw_filename = url.split('/')[-1].split('?')[0]
                    source_path = os.path.join(processed_dir, raw_filename)
                    seek_input = False # Already a clip
                else:
                    # Input is the original full video
                    source_path = original_video_path
                    seek_input = True

                # --- THE NORMALIZATION STEP (The Fix) ---
                # We force everything to the same timebase and resolution
                duration = float(end) - float(start)
                norm_cmd = ["ffmpeg", "-y"]
                
                if seek_input:
                    norm_cmd.extend(["-ss", str(start), "-t", str(duration)])
                
                norm_cmd.extend([
                    "-i", source_path,
                    # Force scale to even numbers, set SAR to 1:1, and force constant 30fps
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1/1,fps=30",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                    "-c:a", "aac", "-ar", "48000", "-ac", "2",
                    "-avoid_negative_ts", "make_zero", # Resets timestamps for concat
                    temp_segment_path
                ])
                
                subprocess.run(norm_cmd, check=True, capture_output=True, shell=True)
                
                f.write(f"file '{temp_segment_path.replace('\\', '/')}'\n")

        # FINAL CONCAT
        concat_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file_path, "-c", "copy", final_output_path
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True, shell=True)

        return f"http://localhost:5000/api/media/processed/{os.path.basename(final_output_path)}"

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
    


def compile_processed_subtitles(video_id, subtitles):
    processed_dir = r"D:\projects\vedio_voice_setup\backend\app\storage\processed"
    uploads_dir = r"D:\projects\vedio_voice_setup\backend\app\storage\uploads"
    
    # 1. Locate Original Video
    video_file = video_id if video_id.endswith('.mp4') else f"{video_id}.mp4"
    video_path = os.path.join(uploads_dir, video_file)
    
    if not os.path.exists(video_path):
        for f in os.listdir(uploads_dir):
            if f.startswith(video_id):
                video_path = os.path.join(uploads_dir, f)
                break
        else:
            raise Exception(f"Video file {video_id} not found")

    base_id = video_id.split('.')[0]
    srt_path = os.path.join(processed_dir, f"{base_id}_subs.srt")
    output_video_name = f"{base_id}_subtitled.mp4"
    output_video_path = os.path.join(processed_dir, output_video_name)

    # 2. Generate SRT Content (UTF-8 with BOM for Arabic support)
    def format_time(seconds):
        td = datetime.timedelta(seconds=float(seconds))
        hours, remainder = divmod(td.seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        millis = int(td.microseconds / 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

    try:
        # Using utf-8-sig adds the BOM which helps some versions of FFmpeg recognize Arabic
        with open(srt_path, "w", encoding="utf-8-sig") as f:
            for i, sub in enumerate(subtitles):
                start_t = format_time(sub['start'])
                end_t = format_time(sub['end'])
                text = sub['text'].replace('\n', ' ') # Ensure no raw newlines in text
                f.write(f"{i+1}\n{start_t} --> {end_t}\n{text}\n\n")

        # 3. Path Escaping for Windows (THE FIX)
        # FFmpeg filter paths on Windows need backslashes escaped or replaced with forward slashes
        # AND colons need to be escaped as '\:'
        clean_srt_path = srt_path.replace('\\', '/').replace(':', '\\:')
        
        # 4. Use libx264 re-encoding (Burning subtitles requires re-encoding the video)
        command = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles='{clean_srt_path}':force_style='FontSize=24,FontName=Arial'",
            "-c:v", "libx264", 
            "-preset", "ultrafast", 
            "-c:a", "copy", 
            output_video_path
        ]
        
        # We use shell=True but pass the command as a list for better handling of spaces in filenames
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            print(f"FFMPEG ERROR: {result.stderr}")
            raise Exception(f"FFmpeg failed with: {result.stderr}")

        return f"http://localhost:5000/api/media/processed/{output_video_name}"

    except Exception as e:
        raise Exception(f"Subtitle burn-in failed: {str(e)}")