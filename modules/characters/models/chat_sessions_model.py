from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from database.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    character_id = Column(
        UUID(as_uuid=True),
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255))

    last_message = Column(Text)

    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    @classmethod
    def create(cls, user_id, character_id, title=None,last_message=None):
        return cls(
            user_id=user_id,
            character_id=character_id,
            title=title,
            last_message=last_message,
        )
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "character_id": str(self.character_id),
            "title": self.title,
            "last_message": self.last_message,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }