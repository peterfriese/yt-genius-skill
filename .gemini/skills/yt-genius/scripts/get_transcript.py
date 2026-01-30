import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    else:
        return f"[{minutes:02d}:{secs:02d}]"

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = get_video_id(url)

    if not video_id:
        print(f"Error: Could not extract video ID from URL: {url}")
        sys.exit(1)

    try:
        # Must be run in an env with youtube-transcript-api installed
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        # Try to get manually created transcripts first, then generated
        # Prefer English, but fallback to whatever is available
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # If no english, just take the first one
                transcript = next(iter(transcript_list))

        fetched_transcript = transcript.fetch()
        
        # Output as compact text with timestamps
        for entry in fetched_transcript:
            timestamp = format_timestamp(entry.start)
            print(f"{timestamp} {entry.text}")

    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
