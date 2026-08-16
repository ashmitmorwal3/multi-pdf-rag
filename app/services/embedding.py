from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY


def get_embedding_model():

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=GOOGLE_API_KEY,
    )