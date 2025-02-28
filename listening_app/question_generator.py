
from transcriber import YoutubeTranscriptService
from transcript_structurer import TranscriptStructurerService
from utils import find_matching_files, get_video_id
from vector_store import QuestionVectorStore

class QuestionGenerator:
    def __init__(self):
        self.vector_store = QuestionVectorStore()

    def download_video_transcript(self, video_url: str):
        print(video_url)
        youtube_transcript_service = YoutubeTranscriptService()
        transcript_file_url = youtube_transcript_service.download_video_transcript(video_url)
        transcrpt_structurer_service = TranscriptStructurerService()
        transcrpt_structurer_service.structure_transcript(transcript_file_url)

    def index_questions(self,filname:str):
        self.vector_store.index_questions_file(filname)

        
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=7HfHdb5J3f4"
    video_id = get_video_id(video_url)
    question_generator = QuestionGenerator()
    question_generator.download_video_transcript(f"{video_url}_*")
    files = find_matching_files(f"{video_id}*.txt", "./questions")
    for file in files:
        question_generator.index_questions(file)

