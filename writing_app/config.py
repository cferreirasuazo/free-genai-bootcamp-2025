from dotenv import load_dotenv
import os

import yaml

def load_prompts():
    """Load prompts from YAML file"""
    with open('prompts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")