from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class File(Base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, unique=True, nullable=False, index=True)
    hash = Column(String, index=True)
    type = Column(String, index=True)
    size = Column(Integer)
    ctime = Column(DateTime)
    mtime = Column(DateTime, index=True)
    indexed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending", index=True)
    retry = Column(Integer, default=0)
    summary = Column(Text)
    keywords = Column(Text)
    category = Column(String)
    confidence = Column(Float)
    source_model = Column(String)
    cost_tokens = Column(Integer, default=0)
    error = Column(Text)

    slides = relationship("Slide", back_populates="file", cascade="all, delete-orphan")
    context = relationship("Context", back_populates="file", uselist=False, cascade="all, delete-orphan")


class Slide(Base):
    __tablename__ = "slides"

    slide_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.file_id"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    title = Column(String)
    summary = Column(Text)
    keywords = Column(Text)
    notes = Column(Text)
    thumbnail_path = Column(String)
    layout_hints = Column(Text)
    confidence = Column(Float)
    hash = Column(String, index=True)
    indexed_at = Column(DateTime, default=datetime.utcnow)
    source_model = Column(String)
    cost_tokens = Column(Integer, default=0)

    file = relationship("File", back_populates="slides")


class Context(Base):
    __tablename__ = "context"

    context_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.file_id"), unique=True, nullable=False)
    dir_summary = Column(Text)
    sibling_files = Column(Text)
    inference_reason = Column(Text)

    file = relationship("File", back_populates="context")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.file_id"), index=True)
    status = Column(String, default="pending", index=True)
    priority = Column(Integer, default=0, index=True)
    retry_count = Column(Integer, default=0)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CostTracking(Base):
    __tablename__ = "cost_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    operation = Column(String)
    model = Column(String)
    tokens = Column(Integer)
    cost_usd = Column(Float)
    file_id = Column(Integer)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan",
                            order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    sources = Column(Text)  # JSON array of source file references
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


def init_db(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
