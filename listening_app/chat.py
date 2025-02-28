from typing import Optional
import ollama

# Model ID
MODEL_ID = "deepseek-r1:1.5b"

class DeepSeekChat:
    def __init__(self, model_id:str = MODEL_ID):
        self.model_id = model_id

    def generate_response(self,message: str) -> Optional[str]:
        response = ollama.chat(
            model=self.model_id,
            messages=[{'role': 'user', 'content': message}]
        )
        return response.get('message', {}).get('content', '')


