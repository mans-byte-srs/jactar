import pygame
import math
import struct

_SAMPLE_RATE = 44100
_initialized = False
_enabled     = False
_sounds: dict = {}
_music_channel: pygame.mixer.Channel | None = None

def init(enabled: bool = True) -> None:
    global _initialized, _enabled, _music_channel
    _enabled = enabled
    try:
        # Standard 16-bit signed, 1 channel (mono)
        pygame.mixer.init(frequency=_SAMPLE_RATE, size=-16, channels=1, buffer=512)
        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(1)
        _generate_sounds()
        _initialized = True
        _music_channel = pygame.mixer.Channel(0)
    except Exception as exc:
        print(f"[sound] mixer init failed: {exc}")
        _initialized = False

def set_enabled(value: bool) -> None:
    global _enabled
    _enabled = value
    if not value: stop_music()

def play(name: str) -> None:
    if _initialized and _enabled and name in _sounds:
        _sounds[name].play()

def play_music() -> None:
    if _initialized and _enabled and _music_channel:
        s = _sounds.get("music")
        if s and not _music_channel.get_busy():
            _music_channel.play(s, loops=-1)

def stop_music() -> None:
    if _music_channel: _music_channel.stop()

# ── internal synthesis (no numpy) ──────────────────────────────────────────

def _make_sound(samples: list[float], volume: float) -> pygame.mixer.Sound:
    """Converts a list of floats (-1.0 to 1.0) into a Pygame Sound object."""
    # Determine if mixer is mono or stereo
    mixer_conf = pygame.mixer.get_init()
    num_channels = mixer_conf[2] if mixer_conf else 1
    
    byte_data = bytearray()
    for s in samples:
        # Clamp and scale to 16-bit signed integer (-32768 to 32767)
        val = max(-1.0, min(1.0, s * volume))
        packed = struct.pack('<h', int(val * 32767))
        # Add to buffer once for mono, twice for stereo
        byte_data.extend(packed * num_channels)
        
    return pygame.mixer.Sound(buffer=byte_data)

def _apply_fade(samples: list[float], fade_ms: int = 20):
    n = len(samples)
    fade_len = int(_SAMPLE_RATE * fade_ms / 1000)
    if fade_len * 2 > n: fade_len = n // 2
    
    for i in range(fade_len):
        # Fade In
        samples[i] *= (i / fade_len)
        # Fade Out
        samples[n - 1 - i] *= (i / fade_len)
    return samples

def _tone(freq: float, duration: float, volume: float = 0.35, wave: str = "sine") -> pygame.mixer.Sound:
    n = int(_SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / _SAMPLE_RATE
        if wave == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif wave == "square":
            val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif wave == "sawtooth":
            val = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        else:
            val = math.sin(2 * math.pi * freq * t)
        samples.append(val)
    
    return _make_sound(_apply_fade(samples), volume)

def _chord(freqs: list[float], duration: float, volume: float = 0.25) -> pygame.mixer.Sound:
    n = int(_SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / _SAMPLE_RATE
        val = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
        samples.append(val)
    
    return _make_sound(_apply_fade(samples, fade_ms=30), volume)

def _noise_burst(duration: float, volume: float = 0.3) -> pygame.mixer.Sound:
    import random
    n = int(_SAMPLE_RATE * duration)
    # Generate white noise
    samples = [random.uniform(-1, 1) for _ in range(n)]
    
    # Simple low-pass filter (moving average) to make it less "harsh"
    smoothed = []
    for i in range(len(samples)):
        prev = samples[i-1] if i > 0 else 0
        nxt = samples[i+1] if i < n-1 else 0
        smoothed.append((prev + samples[i] + nxt) / 3)
        
    return _make_sound(_apply_fade(smoothed, fade_ms=40), volume)

def _engine_loop(duration: float = 0.5) -> pygame.mixer.Sound:
    n = int(_SAMPLE_RATE * duration)
    samples = []
    # Use 56Hz for a seamless loop at 0.5s (exact cycles)
    for i in range(n):
        t = i / _SAMPLE_RATE
        val = (0.6 * math.sin(2 * math.pi * 56 * t) +
               0.3 * (1.0 if math.sin(2 * math.pi * 56 * t) >= 0 else -1.0) +
               0.1 * math.sin(2 * math.pi * 112 * t))
        samples.append(val)
    return _make_sound(samples, 0.18)

def _generate_sounds() -> None:
    global _sounds
    _sounds = {
        "click":   _tone(520,  0.07, volume=0.30),
        "coin":    _tone(880,  0.10, volume=0.40),
        "crash":   _noise_burst(0.40, volume=0.55),
        "nitro":   _chord([660, 880, 1100], 0.22, volume=0.35),
        "shield":  _tone(440,  0.20, volume=0.30, wave="square"),
        "repair":  _chord([523, 659, 784], 0.25, volume=0.35),
        "win":     _chord([523, 659, 784, 1047], 0.55, volume=0.45),
        "lose":    _chord([220, 185, 147], 0.55, volume=0.45),
        "music":   _engine_loop(0.5),
    }