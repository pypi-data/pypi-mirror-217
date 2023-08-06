from __future__ import annotations
from typing import *
import wave
import contextlib

def get_wav_duration(filename: str) -> Tuple[int, int]:
    with contextlib.closing(wave.open(filename, "rb")) as f:
        return f.getnframes(), f.getframerate()

