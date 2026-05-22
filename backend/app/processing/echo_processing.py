#backend/app/procesing/echo_processing.py

def get_analog_delay(level):
    """
    Simulates vintage warmth with characteristic distortion and spread.
    Uses a combination of echo and slight saturation.
    """
    if level <= 0: return None
    delay = 35 + (level * 2)
    decay = min(0.5, level / 150)
    # Adds aecho + lowpass (warmth) + sidechain-like spread
    return f"aecho=0.8:0.9:{delay}:{decay},lowpass=f=3000"

def get_basic_delay(level):
    """
    Single discrete echoes or chorus-like effects (15-500ms).
    """
    if level <= 0: return None
    # Map level to a wider range of delay 15ms to 500ms
    delay = 15 + (level * 4.85)
    return f"aecho=0.9:0.8:{delay}:0.3"

def get_standard_echo(level):
    """
    Classic 'Hello-ello-llo' repeated decaying echoes.
    """
    if level <= 0: return None
    delay = 100 + (level * 3)
    decay = min(0.7, level / 100) # Higher decay for 'Grand Canyon' feel
    return f"aecho=0.8:0.88:{delay}:{decay}"



def get_flutter_echo(level):
    """
    Rapid, repetitive echoes.
    Fixed: Ensure gains are balanced to avoid clipping.
    """
    if level <= 0: return None
    # Adjust intensity based on level
    in_gain = 0.8
    out_gain = 0.7
    return f"aecho={in_gain}:{out_gain}:20|40|60:0.5|0.3|0.1"

def get_reverberation(level):
    """
    Simulates reverb using multiple dense aecho taps.
    Replaces 'freeverb' which is missing in your FFmpeg build.
    """
    if level <= 0: return None
    
    # Map level to decay and delays
    # As level increases, the echoes get closer and stay longer
    decay = min(0.5, level / 200)
    # Dense short delays (30ms to 90ms) simulate a room
    return f"aecho=0.8:0.85:35|45|65|85:0.4|0.3|0.2|{decay}"

















#def get_echo_filter(echo_level):
#    """
#    Generates an FFmpeg aecho filter string based on the echo level (0-100).
#    """
#    if echo_level <= 0:
#        return None
        
    # Logic: delay between 60ms and 260ms
#    delay = 60 + echo_level * 2
    # Logic: decay (feedback) maxing out at 0.4
#    decay = min(0.4, echo_level / 150)
    
    # Format: aecho=in_gain:out_gain:delay:decay
#    return f"aecho=0.8:0.9:{delay}:{decay}"
