import hashlib

from flask import Flask, request, jsonify
from database.database import SessionLocal
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.service.create_new_user_service import create_new_user_service
from flask_cors import CORS
from modules.user.test.test_dao import test_selection
from modules.user.service.login_service import login_service
from modules.user.auth.jwt_handler import JWTHandler
from modules.user.dao.userDAO import UserDAO
import datetime
from modules.user.auth.jwt_handler import JWTHandler
from modules.user.auth.auth_middleware import auth_required
from flask import g
from datetime import datetime, timezone

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})# 👈 关键就是这一行



@app.route("/login", methods=["POST"])
def login():
    db_session = SessionLocal()
    print("login触发")
    try:
        print(db_session)
        data = request.get_json()
        print("Session received:", data)
        user_email = data.get("email")
        user_password = data.get("password")
        access_token,refresh_token= login_service(db_session, data)
        print("登陆成功")
        return jsonify({"message": "success", "access_token": access_token,"refresh_token":refresh_token}), 200
    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400
    except Exception as e:

        print(e)

        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()

@app.route("/profile", methods=["GET"])
def profile():
    #test_token_get_id = auth_required(test_token_get_id)
    data = request.get_json()
    print("Profile received:", data)
    return jsonify({"message": "Profile received"})

@app.route('/register', methods=['POST'])
def register():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.get_json()
        print("Session received:", data)
        new_user=create_new_user_service(db_session,data)
        print(new_user)
        return jsonify({"message": "success","user_info":new_user.to_dict()}),201

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        print(e)

        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()

@app.route('/search_by_id_username_email', methods=['GET'])
def search_by_id_username_email():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.args.get("username")
        print("Session received:", data)
        identifier={'username': data}
        selected_user = test_selection(db_session,identifier)
        print(selected_user)
        return jsonify(selected_user.to_dict()),200
        # return jsonify([user.to_dict() for user in selected_user]), 200
    except Exception as e:
        db_session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()
@app.route('/test_token_get_id', methods=['GET'])
@auth_required
def test_token_get_id():
    print("中间件触发通过")
    #test_token_get_id = auth_required(test_token_get_id)
    #中间件先执行，包裹在路由代码外面
    # g每个请求独立
    # 线程安全
    # 请求结束自动销毁
    #在中间件中g.current_user_id = payload["sub"]，要在路由中访问sub就用user_id
    user_id = g.current_user_id
    db_session = SessionLocal()
    user = UserDAO.get_by_id(db_session, user_id)
    print(user)
    return {"user_id": str(user_id)}

@app.route('/refresh', methods=['POST'])
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)