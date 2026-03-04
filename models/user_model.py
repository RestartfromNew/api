from click import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR

from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column,String,Text,Boolean,TIMESTAMP


db=SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=DateTime)
    updated_at= Column(TIMESTAMP, nullable=False, default=DateTime)