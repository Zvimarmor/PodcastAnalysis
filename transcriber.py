# transcriber.py

import sys
import os
import whisper
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tempfile import NamedTemporaryFile
from typing import List, Dict


def download_mp3_from_url(url: str) -> str:
    """
    Downloads the first .mp3 file found at the given URL (HTML page or direct link).
    Returns the local path to the downloaded file.
    """
    # Case 1: URL points directly to an mp3 file
    if url.lower().endswith(".mp3"):
        response = requests.get(url)
        response.raise_for_status()
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

    # Case 2: URL is an HTML page — we crawl for .mp3 links
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    mp3_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".mp3")]

    if not mp3_links:
        raise ValueError("No MP3 files found at the provided URL.")

    mp3_url = urljoin(url, mp3_links[0])
    response = requests.get(mp3_url)
    response.raise_for_status()
    temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name


def transcribe_audio(mp3_path: str) -> List[Dict]:
    """
    Transcribes an MP3 file using OpenAI's Whisper model (in Hebrew).
    Returns a list of segments with 'start', 'end', and 'text'.
    """
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path, verbose=False, language="he")

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })
    return segments


def get_transcript(source: str) -> List[Dict]:
    """
    Handles either a local MP3 file or a URL (HTML or direct link),
    downloads/transcribes it and returns the segment list.
    
    Args:
        source: Path to MP3 file or URL containing an MP3.

    Returns:
        List of dicts with 'start', 'end', 'text'.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print("Downloading MP3 from URL...")
        local_mp3 = download_mp3_from_url(source)
    elif os.path.isfile(source) and source.lower().endswith(".mp3"):
        local_mp3 = source
    else:
        raise ValueError("Invalid source: must be an MP3 file path or a URL to a page with an MP3.")

    print("Transcribing audio...")
    return transcribe_audio(local_mp3)


if __name__ == "__main__":
    #source is a link
    # source = "https://podcastim.org.il/%D7%94%D7%99%D7%A1%D7%98%D7%95%D7%A8%D7%99%D7%94-%D7%90%D7%99%D7%A0%D7%98%D7%9C%D7%A7%D7%98%D7%95%D7%90%D7%9C%D7%99%D7%AA-%D7%92%D7%A1%D7%94/"  # Replace with your MP3 URL or local path
    #source is a mp3 file
    source = "HIS.mp3"  # Replace with your MP3 URL or local path
    try:
        transcript_segments = get_transcript(source)
        for segment in transcript_segments:
            print(f"{segment['text']} ({round(segment['start'], 2)}s - {round(segment['end'], 2)}s)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)