from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

from app.core import state

from app.models.chat import ChatRequest, ChatResponse

from app.database.database import get_db

from app.models.conversation import ConversationResponse
from app.models.message import MessageResponse

from app.database.crud import (
    get_or_create_conversation,
    save_message,
    get_chat_history,
    get_all_conversations,
    get_conversation_by_session,
    delete_conversation,
)

router = APIRouter()


@router.post(
    "/ask",
    response_model=ChatResponse
)
def ask(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # Get existing conversation or create a new one
    conversation = get_or_create_conversation(
        db=db,
        session_id=request.session_id,
        title=request.question
    )

    # Load previous messages
    messages = get_chat_history(
        db,
        conversation.id
    )

    # Convert database messages to LangChain messages
    chat_history = []

    for message in messages:

        if message.role == "human":

            chat_history.append(
                HumanMessage(
                    content=message.content
                )
            )

        else:

            chat_history.append(
                AIMessage(
                    content=message.content
                )
            )

    # Save user message
    save_message(
        db,
        conversation.id,
        "human",
        request.question
    )

    # Run RAG
    response = state.rag_chain.invoke(
        {
            "input": request.question,
            "chat_history": chat_history
        }
    )

    answer = response["answer"]

    # Build citations
    sources = []

    for doc in response["context"]:

        sources.append(
            {
                "file": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0) + 1
            }
        )

    # Save AI response
    save_message(
        db,
        conversation.id,
        "ai",
        answer
    )

    return ChatResponse(
        answer=answer,
        sources=sources
    )


@router.get(
    "/conversations",
    response_model=List[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):

    conversations = get_all_conversations(db)

    return [

        ConversationResponse(
            session_id=conversation.session_id,
            title=conversation.title,
            created_at=str(conversation.created_at)
        )

        for conversation in conversations
    ]


@router.get(
    "/messages/{session_id}",
    response_model=List[MessageResponse]
)
def get_messages(
    session_id: str,
    db: Session = Depends(get_db)
):

    conversation = get_conversation_by_session(
        db,
        session_id
    )

    if conversation is None:
        return []

    messages = get_chat_history(
        db,
        conversation.id
    )

    return [

        MessageResponse(
            role=message.role,
            content=message.content
        )

        for message in messages
    ]


@router.delete(
    "/conversation/{session_id}"
)
def remove_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):

    conversation = get_conversation_by_session(
        db,
        session_id
    )

    if conversation is None:

        return {
            "message": "Conversation not found."
        }

    delete_conversation(
        db,
        conversation
    )

    return {
        "message": "Conversation deleted."
    }