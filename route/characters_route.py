import hashlib
from datetime import datetime
from flask import Flask, request, jsonify,Blueprint
from sqlalchemy.exc import NoResultFound

from database.database import SessionLocal
from modules.characters.service.chat_management_service import ChatManagementService
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.auth.auth_middleware import auth_required
from modules.user.auth.jwt_handler import JWTHandler
from datetime import datetime, timezone
from modules.user.auth.auth_middleware import auth_required
from modules.user.auth.jwt_handler import JWTHandler
bp = Blueprint('characters_route', __name__)
from flask import g
from modules.user.dao.userDAO import UserDAO
import json
from modules.characters.service.upload_character_assets_service import UploadCharacterAssetsService
from modules.characters.service.get_characters_service import GetCharactersService

@bp.route('/characters/upload_character_assets', methods=['POST'])
@auth_required
def upload_character_assets():
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id

        file = request.files.get("file")
        if not file:
            return {"error": "no file"}, 400
        data_str = request.form.get("data")
        if not data_str:
            return {"error": "no data"}, 400
        data = json.loads(data_str)
        data["user_id"] = user_id
        asset_id=UploadCharacterAssetsService.save_assets_record(db_session, file,data)
        db_session.commit()
        return {
            "asset_id": asset_id
        }
    except Exception as e:
        db_session.rollback()
        print(e)
        return {"error": str(e)}, 500
    finally:
        db_session.close()
@bp.route('/characters/create_character', methods=['POST'])
@auth_required
def create_character():
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id
        data=request.get_json()
        do_rules = data.get("do_rules", [])
        dont_rules = data.get("dont_rules", [])
        assets_id=[data.get("voice_asset_id"),data.get("image_asset_id")]
        assets_id = [aid for aid in assets_id if aid is not None]
        #改为JSON
        do_rules = json.loads(do_rules)
        dont_rules = json.loads(dont_rules)
        data["do_rules"] = do_rules
        data["dont_rules"] = dont_rules
        data["user_id"] = user_id
        UploadCharacterAssetsService.create_character(db_session,data,assets_id)
        db_session.commit()
        return {"message": "success"},200
    except Exception as e:
        db_session.rollback()
        print(e)
        return {"message": str(e)}, 500
    finally:
        db_session.close()

@bp.route('/characters/get_character_list', methods=['POST'])
@auth_required
def get_character_list():
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id
        character_list=GetCharactersService.get_characters_list(db_session,user_id)
        print(character_list)
        db_session.commit()
        return {"message": "success","data":{"characters": character_list}},200
    except Exception as e:
        db_session.rollback()
        print(e)
        return {"message": str(e)}, 500
    finally:
        db_session.close()

@bp.route('/characters/get_or_create_chat_session', methods=['POST'])
@auth_required
def get_or_create_chat_session():
    #建立或者获取对话session
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id
        data = request.get_json()
        character_id = data.get("character_id")
        chat_session = ChatManagementService.get_chat_session(db_session, user_id, character_id)
        if chat_session is None:
            #如果没有会话，就创建会话，title默认为chat,last_message为空
            data['title']="New Chat"
            data['last_message']=""
            chat_session = ChatManagementService.create_chat_session(db_session,user_id, data)
            db_session.commit()
            return {"message": "New chat session created","data":chat_session},200
        else:
            return {"message": "Success,Session Linked","data":chat_session},200
    except Exception as e:
        db_session.rollback()
        print(e)
        return {"message": str(e)}, 500
    finally:
        db_session.close()
@bp.route('/characters/history', methods=['POST'])
@auth_required
def history():
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id
        data = request.get_json()
        session_id=data.get("session_id")
        history=ChatManagementService.get_chat_history(db_session,user_id, session_id)
        return {"message": "success","data":history},200
    except ValueError as e:
        return {"message": str(e)}, 500
    except PermissionError as e:
        return {"message": str(e)}, 500
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500
    finally:
        db_session.close()
@bp.route('/characters/save_new_message', methods=['POST'])
@auth_required
def save_new_message():
    db_session = SessionLocal()
    try:
        user_id = g.current_user_id
        data=request.get_json()
        session_id=data["session_id"]
        message=ChatManagementService.save_message(db_session,user_id, session_id, data)
        db_session.commit()
        return {"message": "success","data":message},200
    except Exception as e:
        db_session.rollback()
        return {"message": str(e)}, 500
    finally:
        db_session.close()


