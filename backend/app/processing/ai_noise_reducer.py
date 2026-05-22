import subprocess
import os

def apply_ai_noise_reduction(input_audio, output_audio):

    command = [
        "deepFilter",
        input_audio,
        "-o", output_audio
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(result.stderr)