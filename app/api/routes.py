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

from app.services.retriever import get_retriever

from app.chains.rag_chain import create_rag_chain
from app.chains.history_chain import create_history_chain
from app.chains.retrieval_chain import create_chain


router = APIRouter()


# ============================================================
# ASK QUESTION
# ============================================================

@router.post(
    "/ask",
    response_model=ChatResponse
)
def ask(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # ========================================================
    # GET OR CREATE CONVERSATION
    # ========================================================

    conversation = get_or_create_conversation(
        db=db,
        session_id=request.session_id,
        title=request.question
    )


    # ========================================================
    # LOAD PREVIOUS MESSAGES
    # ========================================================

    messages = get_chat_history(
        db,
        conversation.id
    )


    # ========================================================
    # CONVERT DATABASE HISTORY
    # TO LANGCHAIN MESSAGES
    # ========================================================

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


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    save_message(
        db,
        conversation.id,
        "human",
        request.question
    )


    # ========================================================
    # CREATE SESSION-SPECIFIC RETRIEVER
    # ========================================================

    retriever = get_retriever(
        embeddings=state.embeddings,
        session_id=request.session_id,
        documents=request.documents
    )


    # ========================================================
    # BUILD DOCUMENT CHAIN
    # ========================================================

    document_chain = create_rag_chain(
        state.llm
    )


    # ========================================================
    # BUILD HISTORY-AWARE RETRIEVER
    # ========================================================

    history_retriever = create_history_chain(
        state.llm,
        retriever
    )


    # ========================================================
    # BUILD RAG CHAIN
    # ========================================================

    rag_chain = create_chain(
        history_retriever,
        document_chain
    )


    # ========================================================
    # RUN RAG
    # ========================================================

    response = rag_chain.invoke(
        {
            "input": request.question,
            "chat_history": chat_history
        }
    )


    answer = response["answer"]


    # ========================================================
    # BUILD CITATIONS
    # ========================================================

    sources = []

    for doc in response["context"]:

        sources.append(
            {
                "file": doc.metadata.get(
                    "source",
                    "Unknown"
                ),

                "page": doc.metadata.get(
                    "page",
                    0
                ) + 1
            }
        )


    # ========================================================
    # SAVE AI RESPONSE
    # ========================================================

    save_message(
        db,
        conversation.id,
        "ai",
        answer
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return ChatResponse(
        answer=answer,
        sources=sources
    )


# ============================================================
# GET ALL CONVERSATIONS
# ============================================================

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
            created_at=str(
                conversation.created_at
            )
        )

        for conversation in conversations
    ]


# ============================================================
# GET CHAT MESSAGES
# ============================================================

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


# ============================================================
# DELETE CONVERSATION
# ============================================================

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
            "message":
                "Conversation not found."
        }


    delete_conversation(
        db,
        conversation
    )


    return {
        "message":
            "Conversation deleted."
    }