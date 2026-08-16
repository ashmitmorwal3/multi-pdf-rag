from app.core.config import (
    LLM_PROVIDER,
    GOOGLE_API_KEY,
)


def get_llm():

    if LLM_PROVIDER == "ollama":

        from langchain_ollama import ChatOllama

        return ChatOllama(
            model="llama3.2:3b",
            temperature=0.3,
        )


    if LLM_PROVIDER == "gemini":

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set."
            )

        from langchain_google_genai import (
            ChatGoogleGenerativeAI
        )

        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=GOOGLE_API_KEY,
        )


    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}"
    )