import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SERVER_URL_BASE = 'http://127.0.0.1:4723'
OPENAI_API_KEY = os.getenv("OPENAI_KEY")