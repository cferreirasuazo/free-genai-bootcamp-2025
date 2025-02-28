from typing import Dict, List, Optional
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, TooManyRequests

class YoutubeTranscriptClient:
    def __init__(self, languages: List[str] = ["ja"]):
        self.languages = languages

    def _get_transcript_by_id(self, video_id:str):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=self.languages)
        except NoTranscriptFound:
            print("Transcript not found.")
            return None
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video.")
            return None
        except VideoUnavailable:
            print("Video is unavailable.")
            return None
        except TooManyRequests:
            print("Too many requests. Try again later.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        return transcript
    
    def _get_video_id(self, url:str):
        if "v=" in url:
            return url.split("v=")[1][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        raise ValueError("Invalid URL format. Please provide a valid YouTube URL.")

    def get_transcript(self, url:str, languages: Optional[List[str]] = None):
        if languages:
            self.languages = languages
        video_id = self._get_video_id(url)
        transcript = self._get_transcript_by_id(video_id)
        return transcript
        
    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            filename (str): Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        filename = f"./transcripts/{filename}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return filename
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return None
        
class YoutubeTranscriptService:
    def __init__(self):
        self.client = YoutubeTranscriptClient()

    def download_video_transcript(self, video_url: str):
        video_id = self.client._get_video_id(video_url)
        transcript = self.client._get_transcript_by_id(video_id)
        file_path = self.client.save_transcript(transcript, video_id)
        print("download_video_transcript",file_path)
        return file_path


