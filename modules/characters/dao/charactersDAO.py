from sqlalchemy.exc import NoResultFound

from modules.characters.models.characters_model import Character
class charactersDAO:
    @staticmethod
    def create_character(db, character_info):
        character = Character.create(
            user_id=character_info["user_id"],
            name=character_info.get('name'),
            gender=character_info.get('gender'),
            relationship=character_info.get('relationship'),
            personality=character_info.get('personality'),
            background_story=character_info.get('background_story'),
            speak_style=character_info.get('speak_style'),
            do_rules=character_info.get('do_rules', []),
            dont_rules=character_info.get('dont_rules', [])
        )
        db.add(character)
        db.flush()
        return character

    @staticmethod
    def get_by_user_id(db, user_id):
        try:
            characters=db.query(Character).filter(Character.user_id == user_id).all()
            return characters
        except Exception as e:
            print("No such user or no characters")
            raise e
    def get_by_character_id(self, db, character_id):
        try:
            character=db.query(Character).filter(Character.id == character_id).first()
            return character
        except Exception as e:
            print("No such character")
            raise e

    @staticmethod
    def get_characters_by_user_id(db, user_id):
        try:
            #可能会返回空列表
            characters=db.query(Character).filter(Character.user_id == user_id).all()
            return characters
        except Exception as e:
            print(e)
            raise e