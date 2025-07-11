# main.py

import sys
import json
from pathlib import Path

from transcriber import transcribe_audio
from splitter import split_segments_to_minutes
from llm_analyzer import analyze_minute_chunk

def process_podcast(mp3_path: str, output_json: str = "analysis_output.json"):
    """
    Full pipeline: transcribe → split → analyze → export.

    Args:
        mp3_path: Path to the podcast MP3 file.
        output_json: Where to save the results as JSON.
    """
    print(f"Transcribing {mp3_path}...")
    segments = transcribe_audio(mp3_path)

    print("Splitting transcript into minute-long chunks...")
    chunks = split_segments_to_minutes(segments)

    print(f"Analyzing {len(chunks)} chunks via LLM...")
    results = []
    for i, chunk in enumerate(chunks):
        print(f"→ Analyzing chunk {i + 1}/{len(chunks)} ({chunk['start']}s–{chunk['end']}s)")
        try:
            analysis = analyze_minute_chunk(
                start=chunk["start"],
                end=chunk["end"],
                text=chunk["text"]
            )
            results.append(analysis.to_dict())
        except Exception as e:
            print(f"⚠️ Failed to analyze chunk {i + 1}: {e}")

    print(f"Saving results to {output_json}...")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("✅ Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/podcast.mp3")
        sys.exit(1)

    mp3_file = sys.argv[1]
    if not Path(mp3_file).exists():
        print(f"❌ File not found: {mp3_file}")
        sys.exit(1)

    process_podcast(mp3_file)
