## backend/app/processing/bass_processing.py

def get_bass_filter(bass_level):
    """
    Generates an FFmpeg bass filter string based on the bass level (0-100).
    """
    if bass_level <= 0:
        return None

    # Logic: gain between 0 and 10
    gain = (bass_level / 100) * 10

    # Format: bass=gain:frequency
    return f"bass=g={gain}:f=100"
        
    