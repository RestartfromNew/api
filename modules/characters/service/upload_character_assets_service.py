import os
import subprocess
import uuid
from itertools import compress

from pyasn1_modules.rfc2985 import gender
from werkzeug.datastructures import FileStorage
from PIL import Image
import os
import uuid

from database.database import SessionLocal
from sqlalchemy.orm import Session, relationship
from modules.characters.dao.charactersDAO import charactersDAO
from modules.characters.dao.charactersAssetsDAO import CharactersAssetsDAO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
class UploadCharacterAssetsService:
    def compress_image(file: FileStorage, save_dir: str) -> str:
        os.makedirs(save_dir, exist_ok=True)
        input_filename = str(uuid.uuid4()) + "_" + file.filename
        input_path = os.path.join(save_dir, input_filename)
        file.save(input_path)
        img = Image.open(input_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        max_size = (512, 512)
        img.thumbnail(max_size)
        output_filename = str(uuid.uuid4()) + ".jpg"
        output_path = os.path.join(save_dir, output_filename)
        img.save(
            output_path,
            format="JPEG",
            quality=70,
            optimize=True
        )
        os.remove(input_path)

        return output_path

    def compress_audio(file:FileStorage, save_dir):
        #压缩文件，并返回保存路径
        #输入FileStorage对象，文件名加文件内容
        input_filename = str(uuid.uuid4()) + "_" + file.filename
        output_filename = str(uuid.uuid4()) + ".wav"
        input_path = os.path.join(save_dir, input_filename)
        output_path = os.path.join(save_dir, output_filename)
        file.save(input_path)#保存原始文件
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ac", "1",
            "-ar", "16000",
            "-t", "6",
            "-c:a", "flac",
            output_path
        ]
        subprocess.run(cmd, check=True)
        os.remove(input_path)
        #输出返回路径
        return output_path
    def save_assets_record(db: Session,file:FileStorage,data):
        try:
            #暂时保存上传assets并写入数据库，返回对应db记录的assets_id
            asset_type=data.get("asset_type")
            save_path=os.path.join(BASE_DIR, "assets", asset_type)
            file_url=""
            if(asset_type == "image"):
                file_url=UploadCharacterAssetsService.compress_image(file, save_path)
            elif(asset_type == "voice"):
                file_url = UploadCharacterAssetsService.compress_audio(file, save_path)
            elif(asset_type == "avater"):
                file_url=save_path+"/avater/"+file.filename
            file_url = os.path.relpath(file_url, BASE_DIR)
            asset_info={
                "file_url": file_url,
                "asset_type": asset_type,
                "user_id": data["user_id"],
                "is_temp": True,
                 "character_id": None
            }
            asset=CharactersAssetsDAO.create_character_assets(db,asset_info)
            db.commit()
            return asset.id
        except Exception as e:
            print(e)
            db.rollback()
            raise
    def create_character(db: Session, character_info,assets_id):
        try:
            character_info={
                "name": character_info["name"],
                "user_id": character_info["user_id"],
                "gender": character_info["gender"],
                "relationship": character_info["relationship"],
                "background_story": character_info["background_story"],
                "personality": character_info["personality"],
                "speak_style": character_info["speak_style"],
                "do_rules": character_info["do_rules"],
                "dont_rules": character_info["dont_rules"],
            }
            character=charactersDAO.create_character(db,character_info)
            character_id=character.id
            for record in assets_id:
                CharactersAssetsDAO.bind_character_assets_id(db,record, character_id)
            db.commit()
            return character.id
        except Exception as e:
            print(e)
            db.rollback()
            raise


# with open("/Users/cin/工程文件/Python/api/face.png", "rb") as f:
#     file = FileStorage(
#         stream=f,
#         filename="face.png",
#     )
#     db=SessionLocal()
#     test_data = {
#         "user_id": "bbc38909-28a2-4a97-95c0-ce9ad56fb7bb",
#         "asset_type": "image"  # avatar / voice / image
#     }
#
#     asset_id=[(UploadCharacterAssetsService.save_assets_record(db=db,file=file,data=test_data))]
#     print(asset_id)
#
#     character_data= {
#         "name": "Test AI2",
#         "user_id": "bbc38909-28a2-4a97-95c0-ce9ad56fb7bb",
#         "gender": "female",
#         "relationship": "friend",
#         "personality": "kind and smart",
#         "background_story": "She is an AI assistant.",
#         "speak_style": "friendly",
#         "do_rules": ["be kind", "help user"],
#         "dont_rules": ["do not lie"]
#     }
#     character=UploadCharacterAssetsService.create_character(db=db,character_info=character_data,assets_id=asset_id)
#     print(character)
