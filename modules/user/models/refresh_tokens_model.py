from click import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR

from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, ForeignKey


class RefreshTokensModel(SQLAlchemy):
    __tablename__ = 'refresh_tokens'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID,ForeignKey("users.id"),nullable=False)
    token_hash = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    revoked=Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=DateTime.now)