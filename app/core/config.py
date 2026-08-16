import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Multi Document AI Assistant"
APP_VERSION = "1.0"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")