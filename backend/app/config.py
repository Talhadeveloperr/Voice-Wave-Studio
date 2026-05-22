#backend/app/config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "storage", "uploads")
    AUDIO_FOLDER = os.path.join(BASE_DIR, "storage", "audio")
    PROCESSED_FOLDER = os.path.join(BASE_DIR, "storage", "processed")
    WAVEFORM_FOLDER = os.path.join(BASE_DIR, "storage", "waveform")

    MAX_CONTENT_LENGTH = 200 * 1024 * 1024 * 100