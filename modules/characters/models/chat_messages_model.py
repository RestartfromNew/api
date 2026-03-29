from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from database.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False
    )

    role = Column(String(10), nullable=False)  # user / character

    content = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
    @classmethod
    def create(cls, session_id, role, content):
        return cls(
            session_id=session_id,
            role=role,
            content=content
        )

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": str(self.session_id),
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }