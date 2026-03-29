from click import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR

from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column,String,Text,Boolean,TIMESTAMP

from datetime import datetime
from database.database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    #更改为user_name可以重名了
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(Text, nullable=True)
    #重要更新，password_hash可以为空
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    #时间会自动生成
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    updated_at = Column(
        TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    @classmethod
    def create(cls,username,email,password_hash):
        return cls(
            username=username,
            email=email,
            password_hash=password_hash,
            is_active=True,
            is_verified=False
        )
    @classmethod
    def create_oauth(cls,username,email):
        return cls(
            username=username,
            email=email,
            is_active=True,
            is_verified=False
        )
    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email
        }