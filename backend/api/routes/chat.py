import json
import logging
from typing import Optional, List

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from src.api.app import get_services, get_db_session
from src.core.database import Conversation, Message

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[str] = None
    created_at: str


# ── REST Endpoints ───────────────────────────────────────────

@router.post("/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    session, search_service, chat_engine = get_services()
    try:
        conversation_id = req.conversation_id

        if not conversation_id:
            conv = Conversation(title=req.message[:50])
            session.add(conv)
            session.commit()
            conversation_id = conv.id

        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=req.message,
        )
        session.add(user_msg)
        session.commit()

        response_text, sources = await chat_engine.generate_response(
            req.message, conversation_id
        )

        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=response_text,
            sources=json.dumps(sources) if sources else None,
        )
        session.add(assistant_msg)
        session.commit()

        return {
            "conversation_id": conversation_id,
            "message": response_text,
            "sources": sources,
        }
    except Exception as e:
        logger.error("Chat error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@router.websocket("/chat/stream")
async def chat_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            message = data.get("message", "")
            conversation_id = data.get("conversation_id")

            if not message.strip():
                await ws.send_json({"error": "Message is required"})
                continue

            session, search_service, chat_engine = get_services()
            try:
                if not conversation_id:
                    conv = Conversation(title=message[:50])
                    session.add(conv)
                    session.commit()
                    conversation_id = conv.id

                user_msg = Message(
                    conversation_id=conversation_id,
                    role="user",
                    content=message,
                )
                session.add(user_msg)
                session.commit()

                await ws.send_json({
                    "type": "start",
                    "conversation_id": conversation_id,
                })

                full_response = ""
                sources = []

                async for chunk_type, chunk_data in chat_engine.generate_response_stream(
                    message, conversation_id
                ):
                    if chunk_type == "text":
                        full_response += chunk_data
                        await ws.send_json({"type": "text", "content": chunk_data})
                    elif chunk_type == "sources":
                        sources = chunk_data
                        await ws.send_json({"type": "sources", "sources": chunk_data})

                assistant_msg = Message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=full_response,
                    sources=json.dumps(sources) if sources else None,
                )
                session.add(assistant_msg)
                session.commit()

                await ws.send_json({"type": "done"})
            finally:
                session.close()

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("WebSocket error: %s", e)
        try:
            await ws.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass


@router.get("/conversations")
async def list_conversations():
    session = get_db_session()
    try:
        convs = (
            session.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(50)
            .all()
        )
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat() if c.updated_at else c.created_at.isoformat(),
            }
            for c in convs
        ]
    finally:
        session.close()


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: int):
    session = get_db_session()
    try:
        msgs = (
            session.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .all()
        )
        return [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "sources": json.loads(m.sources) if m.sources else None,
                "created_at": m.created_at.isoformat(),
            }
            for m in msgs
        ]
    finally:
        session.close()


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    session = get_db_session()
    try:
        conv = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        session.delete(conv)
        session.commit()
        return {"status": "deleted"}
    finally:
        session.close()
