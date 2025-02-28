from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

BACKEND_IMPORTER_URL = os.getenv("BACKEND_IMPORTER_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")