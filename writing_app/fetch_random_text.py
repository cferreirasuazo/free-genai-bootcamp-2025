import random
from api_client import get_words
from llm import get_random_sentence


def fetch_random_text():
    try:
        words = get_words()
        print(words)
        random_number = random.randint(0, len(words) - 1)
        print(random_number)
        word = words[random_number]
        print(word)
        return get_random_sentence(word)
    except Exception as e:
        print(e)
    return "こんにちは"


if __name__ == "__main__":
    print(fetch_random_text())