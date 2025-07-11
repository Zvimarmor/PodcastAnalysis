# transcriber.py

import os
import whisper

def transcribe_audio(mp3_path: str) -> list[dict]:
    """
    Transcribes an MP3 file using OpenAI's Whisper model.
    
    Returns:
        A list of dicts with 'start', 'end', and 'text' for each segment.
    """
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path, verbose=False)
    
    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })
    
    return segments
