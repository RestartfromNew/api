# import hashlib
# from datetime import datetime
#
# from flask import Flask, request, jsonify,Blueprint
# from database.database import SessionLocal
# from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
# from modules.user.service.create_new_user_service import CreateNewUserService
# from modules.user.service.login_service import LoginService
# from modules.user.auth.auth_middleware import auth_required
# from modules.user.auth.jwt_handler import JWTHandler
# from datetime import datetime, timezone
# import  logging
# from resemblyzer import VoiceEncoder, preprocess_wav
# from tts_engine import tts_engine
# import subprocess
# bp = Blueprint('voice_route', __name__)
# from flask import g
# from modules.user.dao.userDAO import UserDAO
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
# # @bp.route('/upload_reference_audio', methods=[ 'POST'])
# # @auth_required
# # def upload_reference_audio():
# #     user_id = g.current_user_id
# #
# #     audio_file = request.files.get("audio")
# #     voice_name = request.form.get("voice_name")
# #
# #     if not audio_file:
# #         return jsonify({"error": "audio missing"}), 400
# #
# #     # 临时保存原始音频
# #     input_path = "temp_input.wav"
# #
# #     audio_file.save(input_path)
# #
# #     # 压缩后音频
# #     reference_audio = "reference.flac"
# #
# #     compress_audio(input_path, reference_audio)
# #
# #     # 生成 embedding
# #     wav = preprocess_wav(reference_audio)
# #
# #     encoder = VoiceEncoder()
# #     embedding = encoder.embed_utterance(wav)
# #
# #     print("embedding length:", len(embedding))
# #
# #     # 测试 TTS
# #     tts_engine.tts_to_file(
# #         language="en",
# #         text="Hello, this is a test voice clone.",
# #         speaker_wav=reference_audio,
# #         file_path="/Users/cin/工程文件/Python/api/test_media/output_upload.wav"
# #     )
# #
# #     print("Voice generated -> output_upload.wav")
# #
# #     return jsonify({
# #         "message": "upload test success",
# #         "embedding_len": len(embedding)
# #     })
# #
# #
# #
