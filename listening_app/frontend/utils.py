# Function to validate YouTube URL
import re

def is_valid_youtube_url(url):
    youtube_regex = (
        r"^(https?://)?(www\.)?"
        r"(youtube\.com/watch\?v=|youtu\.be/)"
        r"([a-zA-Z0-9_-]{11})"
    )
    return re.match(youtube_regex, url) is not None