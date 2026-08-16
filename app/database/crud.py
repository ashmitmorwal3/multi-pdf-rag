from sqlalchemy.orm import Session

from app.database.models import Conversation
from app.database.models import Message


def get_or_create_conversation(
    db: Session,
    session_id: str,
    title: str
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.session_id == session_id
        )
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation(
        session_id=session_id,
        title=title
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation


def save_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
):

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


def get_chat_history(
    db: Session,
    conversation_id: int
):

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.id)
        .all()
    )


def get_all_conversations(db: Session):

    return (
        db.query(Conversation)
        .order_by(Conversation.id.desc())
        .all()
    )


def get_conversation_by_session(
    db: Session,
    session_id: str
):

    return (
        db.query(Conversation)
        .filter(
            Conversation.session_id == session_id
        )
        .first()
    )


def delete_conversation(
    db: Session,
    conversation: Conversation
):

    db.delete(conversation)

    db.commit()