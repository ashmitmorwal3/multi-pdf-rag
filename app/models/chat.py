from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):

    session_id: str

    question: str

    documents: Optional[list[str]] = None


class Source(BaseModel):

    file: str

    page: int


class ChatResponse(BaseModel):

    answer: str

    sources: list[Source]