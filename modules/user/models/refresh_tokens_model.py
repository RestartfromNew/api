from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import datetime


from database.database import Base
from modules.user.models.user_model import User

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    token_hash = Column(String, nullable=False)

    expires_at = Column(TIMESTAMP, nullable=False)

    revoked = Column(Boolean, nullable=False, default=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


    @classmethod
    def create(cls, token_info):
        return cls(
            user_id=token_info.get("user_id"),
            token_hash=token_info.get("token_hash"),
            expires_at=token_info.get("expires_at"),
            revoked=token_info.get("revoked"),
        )