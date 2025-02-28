import openai
import json
import os
from typing import List, Dict
from config import OPENAI_API_KEY

# Ensure to set your OpenAI API key
openai.api_key = OPENAI_API_KEY  # Replace with your actual OpenAI API key

class  LLMService:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.client =  openai.OpenAI( api_key=os.environ.get("OPENAI_API_KEY"))

    def generate_vocab(self, prompt: str) -> Dict:
        """
        Calls OpenAI's GPT API to generate vocabulary based on the prompt.

        Args:
            prompt (str): The prompt provided by the user to generate vocabulary.

        Returns:
            dict: A JSON-like dictionary containing the generated vocabulary.
        """
        try:
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": prompt}
            #     ]
            # )

            system_content = """
            Here's a refined version of the prompt for better understanding and clarity:

---

You are a language processing tool that generates a list of Japanese vocabulary based on user input. The output should be structured as a JSON array containing groups of words. Each group consists of a list of words, with each word having the following details:

1. **kanji**: The Japanese kanji character(s) for the word.
2. **romaji**: The romanized version of the word.
3. **english**: The English meaning of the word.
4. **parts**: A list of components that break down the word into smaller parts (like kanji or syllables). Each component should have:
   - **kanji**: The kanji or character in the component.
   - **romaji**: A list of the romanized syllables corresponding to the kanji.

### Example:
Input: A user provides the word "払う" (harau), which means "to pay" in English.

Output should look like:

  {
    "name_of_the_group": [
      {
        "kanji": "払う",
        "romaji": "harau",
        "english": "to pay",
        "parts": [
          { "kanji": "払", "romaji": ["ha", "ra"] },
          { "kanji": "う", "romaji": ["u"] }
        ]
      }
    ]
  }

Your goal is to structure the generated word list in a similar manner, breaking down each word into its components and providing the corresponding romaji for each part. The JSON should contain a list of groups, with each group including one or more words as shown in the example but return the data as a string for store it later as a json.

            """

            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_content},
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            model=self.model,
            )


            # Assuming the response contains the generated vocabulary in a specific format
            generated_text = response.choices[0].message.content
            # You can choose to parse the generated text into a structured format here
            # For simplicity, we'll just return the raw text as is
            return generated_text
        except Exception as e:
            print(f"Error generating vocabulary: {e}")
            return {}

    def store_vocab_json(self, vocab_data: Dict, file_path: str = 'vocab.json'):
        """
        Store the generated vocabulary JSON data in a file.

        Args:
            vocab_data (dict): The vocabulary data to store.
            file_path (str): The path to the JSON file where data should be saved.
        """
        try:
            # Writing to the JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(vocab_data, f, ensure_ascii=False, indent=4)
            print(f"Vocabulary stored successfully at {file_path}")
        except Exception as e:
            print(f"Error storing vocabulary: {e}")


llm_service = LLMService()

# #Example usage of the LLMService
# if __name__ == "__main__":
#     llm_service = LLMService()

#     # Example prompt
#     prompt = "Generate a list of birds."



