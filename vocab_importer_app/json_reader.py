import json
import requests

from config import BACKEND_IMPORTER_URL

def read_json(path): 
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)



