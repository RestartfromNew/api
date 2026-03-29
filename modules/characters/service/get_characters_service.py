
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship

from modules.characters.dao.charactersDAO import charactersDAO
from modules.characters.dao.charactersAssetsDAO import CharacterAsset, CharactersAssetsDAO
from sqlalchemy.orm import Session, relationship


class GetCharactersService:
    def get_characters_list(db:Session,user_id):
        try:
            query_list=charactersDAO.get_by_user_id(db,user_id)
            character_list=[]
            for character in query_list:
                character_list.append({
                    'character_id': character.id,
                    "gender": character.gender,
                    "name": character.name,
                    "relationship": character.relationship,
                    "image_url": CharactersAssetsDAO.get_image_url_by_character_id(db,character.id),
                })
            print(character_list)
            return character_list
        except Exception as e:
            print(e)
            raise e
