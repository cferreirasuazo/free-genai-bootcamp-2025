import os
from typing import Dict, Optional

import openai
from prompts.question_generator import prompt
from response_example import response_n5
from config import OPENAI_API_KEY
class TranscriptStructurer:
    def __init__(self):
        self.prompt = prompt
        self.openai = openai.OpenAI(
            api_key=OPENAI_API_KEY
        )
        
    def _invoke_openai(self,prompt: str ,transcript: str):
        full_prompt = f"{prompt}\n\nHere's the transcript:\n{transcript}"
        messages = [
            {"role": "user", "content": full_prompt},
        ]

        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error invoking OpenAI: {str(e)}")
            return None
        

    def structure_transcript(self, transcript: str):
        """Structure the transcript into three sections using separate prompts"""
        result = self._invoke_openai(self.prompt, transcript)
        return result
    
    def save_questions(self, structured_sections: Dict[int, str], base_filename: str) -> bool:
        """Save each section to a separate file"""
        print("save_questions")
        try:
            # Create questions directory if it doesn't exist
            os.makedirs(os.path.dirname(base_filename), exist_ok=True)
            
            # Save each section
            filename = f"{os.path.splitext(base_filename)[0]}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(structured_sections)

            return True
        except Exception as e:
            print(f"Error saving questions: {str(e)}")
            return False

    def load_transcript(self, filename: str) -> Optional[str]:
        """Load transcript from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return None


class TranscriptStructurerService:
    def __init__(self):
        self.structurer = TranscriptStructurer()

    def get_transcript_id(self, transcript_url: str) -> str:
        """Extract the ID from the transcript URL"""
        return os.path.splitext(os.path.basename(transcript_url))[0]
    
    def get_question_filename(self,transcripton_id: str) -> str:
        return f"questions/{transcripton_id}.txt"

    def structure_transcript(self, transcript_url: str):
        transcription_id = self.get_transcript_id(transcript_url=transcript_url)
        transcript = self.structurer.load_transcript(transcript_url)
        structure_transcript = self.structurer.structure_transcript(transcript)
        print("structure_transcript", structure_transcript)
        self.structurer.save_questions(structure_transcript, self.get_question_filename(transcription_id))

