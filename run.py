import hashlib
import json

# import torch
from flask import Flask, request, jsonify
from sqlalchemy.exc import NoResultFound

from database.database import SessionLocal
from modules.characters.service.chat_management_service import ChatManagementService
from modules.characters.service.get_characters_service import GetCharactersService
from modules.characters.service.upload_character_assets_service import UploadCharacterAssetsService
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.service.create_new_user_service import CreateNewUserService
from flask_cors import CORS
import io

# import soundfile as sf
# from google.oauth2 import id_token
# from google.auth.transport import requests
# from datetime import datetime, timezone
GOOGLE_CLIENT_ID  = "557921543964-5fviq7q9spg7uhhmrpkei3fkgfhkfnnr.apps.googleusercontent.com"

# from flask import Response, jsonify, request, g
# from resemblyzer import VoiceEncoder, preprocess_wav
from modules.user.service.login_service import LoginService
from modules.user.auth.jwt_handler import JWTHandler
from modules.user.dao.userDAO import UserDAO
import datetime
from modules.user.auth.jwt_handler import JWTHandler
from modules.user.auth.auth_middleware import auth_required
from flask import g
from datetime import datetime, timezone
# # from tts_engine import init_tts
# from resemblyzer import VoiceEncoder, preprocess_wav
# from flask import Response
# from TTS.api import TTS
import subprocess
import modules.characters.dao.charactersDAO as charactersDAO

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})# 👈 关键就是这一行
#
# tts_engine=init_tts()


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
        result= LoginService.login_service(db_session, data)
        print("登陆成功")
        return jsonify({"message": "success","data":result }), 200
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
        new_user=CreateNewUserService.create_new_user_service(db_session,data)
        print(new_user)
        db_session.commit()
        return jsonify({"message": "success","user_info":new_user.to_dict()}),201

    except ValueError as e:
        db_session.commit()
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:
        db_session.commit()
        print(e)

        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()

# @app.route('/search_by_id_username_email', methods=['GET'])
# def search_by_id_username_email():
#     db_session = SessionLocal()
#     print(db_session)
#     try:
#         data = request.args.get("username")
#         print("Session received:", data)
#         identifier={'username': data}
#         selected_user = test_selection(db_session,identifier)
#         print(selected_user)
#         return jsonify(selected_user.to_dict()),200
#         # return jsonify([user.to_dict() for user in selected_user]), 200
#     except Exception as e:
#         db_session.rollback()
#         print(e)
#         return jsonify({"error": str(e)}), 500
#     finally:
#         db_session.close()
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


# from TTS.api import TTS
# def compress_audio(input_path, output_path):
#     cmd = [
#         "ffmpeg",
#         "-y",
#         "-i", input_path,
#         "-ac", "1",      # mono
#         "-ar", "16000",  # 16kHz
#         "-t", "6",       # 最多6秒
#         "-c:a", "flac",
#         output_path
#     ]
#
#     subprocess.run(cmd, check=True)
#
# # import time
# # import torch
# from flask import Response, jsonify, request, g

# @app.route('/upload_reference_audio', methods=['POST'])
# @auth_required
# def upload_reference_audio():
#
#     user_id = g.current_user_id
#
#     audio_file = request.files.get("audio")
#     voice_name = request.form.get("voice_name")
#
#     if not audio_file:
#         return jsonify({"error": "audio missing"}), 400
#
#     # 1 保存上传音频
#     input_path = "temp_input.wav"
#     audio_file.save(input_path)
#
#     # 2 压缩音频
#     reference_audio = "reference.flac"
#     compress_audio(input_path, reference_audio)
#
#     print("audio compressed")
#
#     # 3 生成 speaker embedding
#     wav = preprocess_wav(reference_audio)
#
#     encoder = VoiceEncoder()
#     embedding = encoder.embed_utterance(wav)
#
#     print("embedding length:", len(embedding))
#
#     # 4 生成语音（直接返回 waveform）
#     with torch.inference_mode():
#
#         wav = tts_engine.tts(
#             text="Hello, this is a streaming voice cloning test. "
#                  "The server will generate speech and send audio back to the browser.",
#             speaker_wav=reference_audio,
#             language="en"
#         )
#
#     # 5 写入内存 buffer
#     buffer = io.BytesIO()
#
#     sf.write(buffer, wav, 24000, format="WAV")
#
#     buffer.seek(0)
#
#     # 6 streaming 返回
#     def generate():
#
#         while True:
#
#             chunk = buffer.read(4096)
#
#             if not chunk:
#                 break
#
#             yield chunk
#
#     return Response(
#         generate(),
#         mimetype="audio/wav",
#         headers={
#             "Content-Disposition": "inline; filename=voice.wav",
#             "Cache-Control": "no-cache"
#         }
#     )
#
# @app.route('/test_stream_voice', methods=['GET'])
# def test_stream_voice():
#
#     output_file = "output_upload.wav"
#
#     with torch.inference_mode():
#         tts_engine.tts_to_file(
#             language="en",
#             text="Hello, this is a voice cloning test for my AI speech system. I am uploading a reference audio sample to generate a speaker embedding, then using that embedding to synthesize new speech with a neural text-to-speech model",
#             speaker_wav="reference.flac",
#             file_path=output_file
#         )
#
#     def generate():
#
#         with open(output_file, "rb") as f:
#             while True:
#                 chunk = f.read(4096)
#                 if not chunk:
#                     break
#                 yield chunk
#
#     return Response(generate(), mimetype="audio/wav")
@app.route('/characters/upload_info', methods=['POST'])
def upload_info():
    db_session=SessionLocal()
    data = request.get_json()
    characters=charactersDAO.reate_character(db_session,data)
    print(data)

    return jsonify({"received": "success"}),200

# @app.route('/google', methods=['POST'])
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
@app.route('/characters/upload_character_assets', methods=['POST'])
@auth_required
def upload_character_assets():
    user_id = g.current_user_id
    db_session = SessionLocal()
    file = request.files.get("file")
    if not file:
        return {"error": "no file"}, 400
    data_str = request.form.get("data")
    if not data_str:
        return {"error": "no data"}, 400
    data = json.loads(data_str)
    data["user_id"] = user_id
    asset_id=UploadCharacterAssetsService.save_assets_record(db_session, file,data)
    return {
        "asset_id": asset_id
    }
@app.route('/characters/create_character', methods=['POST'])
@auth_required
def create_character():
    try:
        user_id = g.current_user_id
        db_session = SessionLocal()
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
        return {"message": "success"},200
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500
@app.route('/characters/get_character_list', methods=['POST'])
@auth_required
def get_character_list():
    try:
        user_id = g.current_user_id
        db_session = SessionLocal()
        character_list=GetCharactersService.get_characters_list(db_session,user_id)
        return {"message": "success","data":{"characters": character_list}},200
    except NoResultFound:
        return {"message": "no characters found"}, 404
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500

@app.route('/characters/get_or_create_chat_session', methods=['POST'])
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
            db_session.commit()
            return {"message": "Success,Session Linked","data":chat_session},200
    except Exception as e:
        db_session.rollback()
        print(e)
        return {"message": str(e)}, 500
    finally:
        db_session.close()

@app.route('/characters/history', methods=['POST'])
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
@app.route('/characters/save_new_message', methods=['POST'])
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
@app.route('/auth/login-sync', methods=['POST'])
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
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)