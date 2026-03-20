from typing import List, Dict
from sqlalchemy.orm import Session
from src.core.database import Message
from src.core.config import settings


def get_conversation_history(session: Session, conversation_id: int) -> List[Dict[str, str]]:
    messages = (
        session.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )

    max_messages = settings.chat_max_history
    recent = messages[-max_messages:] if len(messages) > max_messages else messages

    return [{"role": m.role, "content": m.content} for m in recent]


def format_history_for_rewrite(history: List[Dict[str, str]]) -> str:
    lines = []
    for msg in history[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:200]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
