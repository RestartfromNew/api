#
# from sqlalchemy.dialects.postgresql import UUID
# import uuid
# from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, ForeignKey
# from datetime import datetime
# from database.database import Base
# from pgvector.sqlalchemy import Vector
# class Voice(Base):
#     __tablename__ = "Voice"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     voice_name = Column(String(100), nullable=False, unique=True)
#     reference_audio_path = Column(Text, nullable=False)
#     embedding = Column(Vector(256))
#     #时间会自动生成
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)
#     updated_at = Column(
#         TIMESTAMP,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow
#     )
#     @classmethod
#     def create(cls,user_id,voice_name,reference_audio_path,embedding):
#         return cls(
#             user_id=user_id,
#             voice_name=voice_name,
#             reference_audio_path=reference_audio_path,
#             embedding=embedding,
#         )
#     def get_vector(self):
#         return self.embedding.tolist()