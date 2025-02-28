from openai import OpenAI
from config import OPENAI_API_KEY, load_prompts
class LLMClient:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key
        )

    def generate_text(self,messages, max_tokens=100):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response
    
llm_client = LLMClient(OPENAI_API_KEY)

def get_random_sentence(word: str):
    prompts = load_prompts()
    messages = [
        {"role": "system", "content": prompts['sentence_generation']['system']},
        {"role": "user", "content": prompts['sentence_generation']['user'].format(word=word.get('kanji', ''))}
    ]

    response = llm_client.generate_text(messages)
    return response.choices[0].message.content