from pydantic import BaseModel


class ConversationResponse(BaseModel):
    session_id: str
    title: str
    created_at: str