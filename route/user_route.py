import hashlib
from datetime import datetime

from flask import Flask, request, jsonify,Blueprint
from database.database import SessionLocal
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.service.create_new_user_service import CreateNewUserService
from modules.user.service.login_service import LoginService
from modules.user.auth.auth_middleware import auth_required
from modules.user.auth.jwt_handler import JWTHandler
from datetime import datetime, timezone
GOOGLE_CLIENT_ID  = "557921543964-5fviq7q9spg7uhhmrpkei3fkgfhkfnnr.apps.googleusercontent.com"
import  logging
bp = Blueprint('user_route', __name__)
from flask import g
from modules.user.dao.userDAO import UserDAO

@bp.route('/register', methods=['POST'])
def register():
    db_session = SessionLocal()
    try:
        data = request.get_json()
        print("Session received:", data)
        new_user=CreateNewUserService.create_new_user_service(db_session,data)
        print(new_user)
        db_session.commit()
        return jsonify({"message": "success"}),201

    except ValueError as e:
        print(e)
        db_session.rollback()
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        print(e)
        db_session.rollback()
        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()

@bp.route('/login', methods=['POST'])
def login():
    db_session = SessionLocal()
    print("login触发")
    try:

        print(db_session)
        data = request.get_json()
        print("Session received:", data)
        result = LoginService.login_service(db_session, data)
        logging.info("login触发")
        logging.info(f"Session received: {data}")
        print("登陆成功")
        db_session.commit()
        return jsonify({"message": "success","data":result}), 200
    except ValueError as e:
        db_session.rollback()
        return jsonify({
            "error": str(e)
        }), 400
    except Exception as e:

        print(e)
        db_session.rollback()
        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()
# @bp.route('/google', methods=['POST'])
# def google():
#     data = request.get_json()
#     data = request.get_json()
#
#     if not data or "id_token" not in data:
#         return jsonify({"error": "id_token missing"}), 400
#
#     google_token = data["id_token"]
#     idinfo = id_token.verify_oauth2_token(
#         google_token,
#         requests.Request(),
#         GOOGLE_CLIENT_ID
#     )
#     google_user_id = idinfo["sub"]
#     email = idinfo["email"]
#     name = idinfo.get("name", email.split("@")[0])
#     picture = idinfo.get("picture")
#     print("Google user:", email)


@bp.route('/get_user_talk', methods=['GET'])
@auth_required
def get_user_talk():
    #注意，如果access token失效，直接会给前端发消息，要求触发refresh
    user_id = g.current_user_id
    db_session = SessionLocal()
    user = UserDAO.get_by_id(db_session, user_id)
    print(user)
    return {"user_id": str(user_id)}
@bp.route('/refresh', methods=['POST'])
def refresh():
    print("refresh触发")
    db_session = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return jsonify({"error": "Missing refresh token"}), 400
        # hash token
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        # 查数据库
        record = RefreshTokensDAO.get_record_by_token_hash(db_session, token_hash)
        if not record:
            return jsonify({"error": "Refresh token not found"}), 404
        # 如果已经 revoked
        if record.revoked:
            return jsonify({"error": "Refresh token revoked"}), 401
        # JWT 验证
        payload = JWTHandler.verify_refresh_token(refresh_token)
        # JWT 过期
        if not payload:
            record.revoked = True
            db_session.commit()
            return jsonify({
                "error": "Refresh token expired, please login again"
            }), 401
        # 数据库 expires 检查
        if record.expires_at < datetime.now(timezone.utc):
            record.revoked = True
            db_session.commit()
            return jsonify({
                "error": "Refresh token expired"
            }), 401
        # 获取 user_id
        user_id = payload["sub"]
        # 生成新的 access token
        access_token, expires_at = JWTHandler.generate_access_token(user_id)
        print("refresh未过期，生成新的acess")
        return jsonify({
            "message": "success",
            "access_token": access_token,
            "expires_at": expires_at.isoformat()
        }), 200
    finally:
        db_session.close()
@bp.route('/auth/login-sync', methods=['POST'])
def auth_login_sync():
    db_session = SessionLocal()
    try:
        data = request.get_json()
        print("Session received:", data)
        oauth_user_info={
            "provider": "google",
            "provider_user_id": data.get("user_id"),
            "email": data.get("user_email"),
            "username": data.get("user_name"),
        }
        user=LoginService.oauth_login_service(db_session, oauth_user_info)
        db_session.commit()
        return user, 200
    except Exception as e:
        print(e)
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()




