from datetime import datetime

from modules.characters.models.chat_sessions_model import ChatSession
class ChatSessionDAO:
    @staticmethod
    def create_session(db, chat_session_info):
        try:
            session =ChatSession.create(
                user_id=chat_session_info['user_id'],
                character_id=chat_session_info['character_id'],
                title=chat_session_info['title'],
                last_message=chat_session_info['last_message']
            )
            db.add(session)
            db.flush()
            return session
        except Exception as e:
            print(e)
            raise e
    @staticmethod
    def get_session_by_user_and_character_id(db, user_id,character_id):
        try:
            session = db.query(ChatSession).filter_by(user_id=user_id,character_id=character_id).first()
            return session
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def get_session_by_session_id(db, session_id):
        try:
            session = db.query(ChatSession).filter_by(id=session_id).first()
            return session
        except Exception as e:
            print(e)
            raise e
    @staticmethod
    def update_last_message(db,session_id,last_message):
        try:
            session = db.query(ChatSession) \
                .filter(ChatSession.id == session_id) \
                .first()

            if not session:
                return None

            session.last_message = last_message
            session.update_at=datetime.now()

            return session

        except Exception as e:
            print(e)
            raise e