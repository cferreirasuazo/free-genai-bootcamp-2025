import requests
from typing import List, Dict

from config import BACKEND_API_KEY

def get_words() -> List[Dict]:
    return requests.get(BACKEND_API_KEY).json()
