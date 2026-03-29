from sqlalchemy.exc import NoResultFound

from modules.characters.models.characters_assets_model import CharacterAsset
class CharactersAssetsDAO:
    @staticmethod
    def create_character_assets(db, character_assets_info):
        character_assets_record=CharacterAsset(
            user_id=character_assets_info["user_id"],
            character_id=character_assets_info["character_id"],
            asset_type=character_assets_info["asset_type"],
            file_url=character_assets_info["file_url"],
            is_temp=character_assets_info["is_temp"],
        )
        db.add(character_assets_record)
        db.flush()
        #flush之后已经有character_id的值了
        return character_assets_record

    @staticmethod
    def get_assets_by_character_id(self, db, character_id):
        try:
            character_assets_record=db.query(CharacterAsset).filter(CharacterAsset.character_id == character_id).all()
            return character_assets_record
        except Exception as e:
            print("No such character")
            return e

    @staticmethod
    def get_assets_record_by_id(db, asset_record_id):
        try:
            character_assets_record=db.query(CharacterAsset).filter(CharacterAsset.id == id).first()
            return character_assets_record
        except Exception as e:
            print("No such character Assets record")
            return e
    @staticmethod
    def bind_character_assets_id(db,asset_id, character_id):
        asset = db.query(CharacterAsset).filter(
            CharacterAsset.id == asset_id
        ).first()

        if not asset:
            raise Exception("Asset not found")
        asset.character_id = character_id
        asset.is_temp = False
        return asset

    @staticmethod
    def get_image_url_by_character_id(db, character_id):
        image_url = db.query(CharacterAsset).filter(
            CharacterAsset.character_id == character_id,
            CharacterAsset.asset_type == "image"
        ).first()
        return image_url.file_url