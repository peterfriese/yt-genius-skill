import os
import sys
import subprocess
import json
import argparse

def timestamp_to_seconds(timestamp):
    # Handles [MM:SS] or [HH:MM:SS]
    ts = timestamp.strip('[]')
    parts = ts.split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return int(parts[0]) * 60 + int(parts[1])

def cut_clip(video_url, start_time, end_time, output_path):
    print(f"Cutting clip from {start_time} to {end_time} -> {output_path}")
    
    # Using yt-dlp to get the direct stream URL
    # We use -g to get the URL without downloading the whole thing
    # Then we use ffmpeg to download only the segment
    try:
        # Get formats
        cmd_get_url = [
            "yt-dlp",
            "-g",
            "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
            video_url
        ]
        urls = subprocess.check_output(cmd_get_url).decode().split('\n')
        video_url_stream = urls[0]
        audio_url_stream = urls[1] if len(urls) > 1 else None

        # Build ffmpeg command
        # -ss BEFORE -i for fast seeking (imprecise but fast)
        # -to for duration
        cmd_ffmpeg = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", video_url_stream,
        ]
        
        if audio_url_stream:
            cmd_ffmpeg += ["-ss", str(start_time), "-i", audio_url_stream]
            
        cmd_ffmpeg += [
            "-t", str(end_time - start_time),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "experimental",
            "-y",
            output_path
        ]
        
        subprocess.run(cmd_ffmpeg, check=True)
        print(f"Successfully created: {output_path}")
    except Exception as e:
        print(f"Error cutting clip: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and cut clips from YouTube")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--clips", help="JSON string of clips: '[{\"start\": \"00:10\", \"end\": \"00:20\", \"name\": \"clip.mp4\"}]'")
    
    args = parser.parse_args()
    
    if not args.clips:
        print("No clips specified.")
        sys.exit(1)
        
    clips_data = json.loads(args.clips)
    
    # Ensure tmp directory exists
    tmp_dir = "tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        
    for clip in clips_data:
        start_secs = timestamp_to_seconds(clip['start'])
        end_secs = timestamp_to_seconds(clip['end'])
        output_name = clip['name']
        output_path = os.path.join(tmp_dir, output_name)
        
        cut_clip(args.url, start_secs, end_secs, output_path)
