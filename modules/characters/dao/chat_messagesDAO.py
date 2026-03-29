from sqlalchemy.testing import db

from modules.characters.models.chat_messages_model import ChatMessage
class ChatMessagesDAO:
    @staticmethod
    def save_new_message(db,message_info):
        message = ChatMessage.create(
            session_id=message_info["session_id"],
            role=message_info["role"],
            content=message_info["content"]
        )
        db.add(message)
        db.flush()
        return message
    @staticmethod
    def get_chat_history(db,session_id):
        return db.query(ChatMessage)\
        .filter(ChatMessage.session_id == session_id)\
        .order_by(ChatMessage.created_at.asc())\
        .all()