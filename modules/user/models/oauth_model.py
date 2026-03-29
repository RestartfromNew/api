from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint

from datetime import datetime
from database.database import Base
class Oauth(Base):
    __tablename__ = "oauth"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    # user_id=和主表记录一一对应
    provider_user_id = Column(Text, nullable=False)
    provider=Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    __table_args__ = (
        UniqueConstraint('provider', 'provider_user_id', name='uq_provider_user'),
    )
    @classmethod
    def create(cls,provider_user_id,provider,user_id):
        return cls(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
        )
    def to_dict(self):
        return {
            "provider_user_id": str(self.provider_user_id),
            "provider":str(self.provider),
            "user_id":str(self.user_id),
        }