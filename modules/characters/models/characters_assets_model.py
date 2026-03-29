from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
import uuid
from datetime import datetime
from modules.characters.models.characters_model import Character
from modules.user.models.user_model import User

from database.database import Base
from sqlalchemy import CheckConstraint

class CharacterAsset(Base):
    __tablename__ = "character_assets"
    __table_args__ = (
        CheckConstraint(
            "asset_type IN ('avatar', 'voice', 'image')",
            name="check_asset_type"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    character_id = Column(
        UUID(as_uuid=True),
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=True   # 允许先上传再绑定
    )
    asset_type = Column(String(20))  # avatar / voice / image
    file_url = Column(Text, nullable=False)
    is_temp = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=datetime.utcnow
    )
    @classmethod
    def create(
        cls,
        user_id,
        file_url,
        asset_type,
        character_id=None,
        is_temp=True
    ):
        return cls(
            user_id=user_id,
            character_id=character_id,
            asset_type=asset_type,
            file_url=file_url,
            is_temp=is_temp
        )
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "character_id": str(self.character_id) if self.character_id else None,
            "asset_type": self.asset_type,
            "file_url": self.file_url,
            "is_temp": self.is_temp,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }