from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from modules.user.models.user_model import User #依赖User表

from database.database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(100), nullable=False)
    gender = Column(String(10))
    relationship = Column(String(50))
    personality = Column(Text)
    background_story = Column(Text)
    speak_style = Column(Text)
    do_rules = Column(JSONB)
    dont_rules = Column(JSONB)
    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
    @classmethod
    def create(
        cls,
        user_id,
        name,
        gender=None,
        relationship=None,
        personality=None,
        background_story=None,
        speak_style=None,
        do_rules=None,
        dont_rules=None
    ):
        return cls(
            user_id=user_id,
            name=name,
            gender=gender,
            relationship=relationship,
            personality=personality,
            background_story=background_story,
            speak_style=speak_style,
            do_rules=do_rules,
            dont_rules=dont_rules
        )
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "gender": self.gender,
            "relationship": self.relationship,
            "personality": self.personality,
            "background_story": self.background_story,
            "speak_style": self.speak_style,
            "do_rules": self.do_rules,
            "dont_rules": self.dont_rules,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }