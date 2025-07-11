# splitter.py

from typing import List, Dict

def split_segments_to_minutes(segments: List[Dict], window_sec: int = 60) -> List[Dict]:
    """
    Splits the transcript segments into fixed-length windows (default: 60 seconds).
    
    Args:
        segments: List of dicts with 'start', 'end', 'text'
        window_sec: Length of each window in seconds (default is 60)

    Returns:
        A list of dicts, each with:
            - 'start': start time of window
            - 'end': end time of window
            - 'text': concatenated transcript in this time window
    """
    result = []
    current_window_start = 0
    current_window_end = window_sec
    current_text = []

    for segment in segments:
        seg_start = segment['start']
        seg_end = segment['end']
        seg_text = segment['text']

        while seg_end > current_window_end:
            # Partial segment fits in current window
            if seg_start < current_window_end:
                current_text.append(seg_text)

            # Save current window
            result.append({
                "start": current_window_start,
                "end": current_window_end,
                "text": " ".join(current_text).strip()
            })

            # Move to next window
            current_window_start += window_sec
            current_window_end += window_sec
            current_text = []

            # If this segment goes into the next window too, don't skip it
            if seg_end > current_window_start:
                current_text.append(seg_text)
                break
        else:
            current_text.append(seg_text)

    # Append final chunk if anything remains
    if current_text:
        result.append({
            "start": current_window_start,
            "end": current_window_end,
            "text": " ".join(current_text).strip()
        })

    return result
