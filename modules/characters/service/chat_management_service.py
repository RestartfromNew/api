from database.database import SessionLocal
from modules.characters.dao.charactersDAO import charactersDAO
from  modules.characters.dao.chat_messagesDAO import ChatMessagesDAO
from modules.characters.dao.chat_sessionDAO import ChatSessionDAO
from sqlalchemy.orm import Session, relationship
class ChatManagementService:
    def create_chat_session(db:Session,user_id,data):
        try:
            #创建新会话，返回session类型json形式
            chat_session={
                "user_id":user_id,
                "character_id":data["character_id"],
                "title":data["title"],
                "last_message":data["last_message"],
            }
            created_session=ChatSessionDAO.create_session(db,chat_session)
            created_session=created_session.to_dict()
            created_session["session_id"]=created_session["id"]
            del created_session["id"]
            print(created_session)
            return created_session
        except Exception as e:
            print(e)
            raise e

    def get_chat_session(db, user_id, character_id):
        try:
            #获取会话，如果会话存在返回记录的Json结果,如果不存在返回None
            print(character_id)
            session_result=ChatSessionDAO.get_session_by_user_and_character_id(db,user_id,character_id)
            print("查找session")
            if session_result is None:
                return None
            session_result=session_result.to_dict()
            session_result["session_id"]=session_result["id"]
            del session_result["id"]
            return session_result
        except Exception as e:
            print(e)
            raise e


    def get_chat_history(db,user_id,session_id):
        session_record=ChatSessionDAO.get_session_by_session_id(db,session_id)
        if not session_record:
            raise ValueError("Session not found")
        if str(session_record.user_id) != str(user_id):
            print(session_record.user_id, user_id)
            raise PermissionError("Unauthorized")
        results= ChatMessagesDAO.get_chat_history(db,session_id)
        history=[]
        for item in results:
            history.append(item.to_dict())
        return history

    def save_message(db,user_id,session_id,data):
        #在每次写数据前都要验证
        try:
            session_record = ChatSessionDAO.get_session_by_session_id(db, session_id)
            if not session_record:
                raise ValueError("Session not found")
            if str(session_record.user_id) != str(user_id):
                print(session_record.user_id, user_id)
                raise PermissionError("Unauthorized")
            data={
                'session_id':data["session_id"],
                'role':data["role"],
                'content':data["content"],
            }
            message=ChatMessagesDAO.save_new_message(db,message_info=data)
            ChatSessionDAO.update_last_message(db,session_id,data["content"])
            return message.to_dict()
        except Exception as e:
            print(e)
            raise e


