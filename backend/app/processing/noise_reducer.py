# backend/app/processing/noise_reducer.py

import subprocess
import os
from app.processing.echo_processing import (
    get_analog_delay, 
    get_basic_delay, 
    get_standard_echo, 
    get_flutter_echo, 
    get_reverberation
)
from app.processing.bass_processing import get_bass_filter

# ------------------------------------------------------------
# 🎧 ANALYZE NOISE PROFILE
# ------------------------------------------------------------
def get_noise_floor(input_audio):
    command = [
        "ffmpeg",
        "-i", input_audio,
        "-af", "volumedetect",
        "-f", "null",
        "-"
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    for line in result.stderr.split("\n"):
        if "mean_volume" in line:
            return float(line.split(":")[1].strip().replace(" dB", ""))

    return -40.0


# ------------------------------------------------------------
# 🚀 MAIN PROCESSOR
# ------------------------------------------------------------
def apply_audio_effects(input_audio, output_audio, noise, bass, 
                        analog_echo, basic_echo, standard_echo, flutter_echo, reverb_echo,profile_path=None):

    filters = []

    # ------------------------------------------------------------
    # 🎯 STEP 1: BASE CLEANUP
    # ------------------------------------------------------------
    #filters.append("highpass=f=80")
    
    #filters.append("lowpass=f=16000")

    # ------------------------------------------------------------
    # 🎯 STEP 2: NOISE PROFILE BASED REDUCTION (CORE FIX)
    # ------------------------------------------------------------
    #
    #if profile_path and os.path.exists(profile_path):

    #    noise_floor = get_noise_floor(profile_path)

        # Strong but safe spectral subtraction
    #    nr = 15 + (noise / 100) * 25
    #    nf = noise_floor + 2  # slightly above noise

    #    filters.append(f"afftdn=nr={nr}:nf={nf}:tn=1")

    #    # Smart expander (NOT aggressive gate)
    #    threshold = noise_floor + 6
    #    filters.append(
    #        f"agate=threshold={threshold}dB:ratio=2:attack=20:release=200"
    #    )

    #else:
        # fallback
    #    nr = 10 + (noise / 100) * 20
    #    filters.append(f"afftdn=nr={nr}:nf=-30:tn=1")
    if noise > 0:
        # Phase A: Spectral Subtraction (Steady background hiss)
        # nr: Noise reduction intensity (Max 32dB)
        # tn=1: Transient noise reduction (kills keyboard clicks)
        nr_val = 12 + (noise / 100) * 20
        filters.append(f"afftdn=nr={nr_val}:nf=-35:tn=1:om=o")

        # Phase B: The 'Paid Software' Secret (Downward Expansion)
        # This acts like your VAD logic but in real-time. It pushes 
        # noise to 0 during silence but keeps the voice natural.
        gate_thresh = -45 + (noise / 5)
        filters.append(f"agate=threshold={gate_thresh}dB:ratio=2:attack=20:release=300:makeup=1.2")
    # ------------------------------------------------------------
    # 🎙️ STEP 3: VOICE ENHANCEMENT
    # ------------------------------------------------------------
    filters.append("equalizer=f=3000:t=q:w=1:g=3")   # clarity
    filters.append("equalizer=f=250:t=q:w=1:g=-2")  # remove mud

    # ------------------------------------------------------------
    # 🔊 STEP 4: BASS
    # ------------------------------------------------------------
    bass_filter = get_bass_filter(bass)
    if bass_filter:
        filters.append(bass_filter)    

    # ------------------------------------------------------------
    # 🌊 STEP 5: ECHO (SAFE)
    # ------------------------------------------------------------
    echo_funcs = [
            (get_analog_delay, analog_echo),
            (get_basic_delay, basic_echo),
            (get_standard_echo, standard_echo),
            (get_flutter_echo, flutter_echo),
            (get_reverberation, reverb_echo)
        ]
    for func, level in echo_funcs:
            effect_filter = func(level)
            if effect_filter:
                filters.append(effect_filter)    

    # ------------------------------------------------------------
    # 🎚️ STEP 6: COMPRESSION
    # ------------------------------------------------------------
    filters.append(
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=80:makeup=2"
    )

    # ------------------------------------------------------------
    # 🔇 STEP 7: LIMITER
    # ------------------------------------------------------------
    filters.append("alimiter=limit=0.95")

    # ------------------------------------------------------------
    # 📢 STEP 8: FINAL NORMALIZATION (LAST ALWAYS)
    # ------------------------------------------------------------
    filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")

    # ------------------------------------------------------------
    # FINAL COMMAND
    # ------------------------------------------------------------
    filter_chain = ",".join(filters)

    command = [
        "ffmpeg",
        "-i", input_audio,
        "-af", filter_chain,
        "-ar", "48000",
        "-ac", "2",
        "-c:v", "copy",
        "-y",
        output_audio
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Audio processing failed")