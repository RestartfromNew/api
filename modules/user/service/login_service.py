from os import access

from modules.user.dao.userDAO import UserDAO
import hashlib
import bcrypt
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.auth.jwt_handler import JWTHandler
def login_service(db,data):
    try:

        email = data.get('email')
        password = data.get('password')
        user_info=UserDAO.get_by_email(db, email)
        if not user_info:
            raise ValueError('No such user')
        if not bcrypt.checkpw(
                    password.encode("utf-8"),
                    user_info.password_hash.encode("utf-8")):
            raise ValueError("Incorrect password")
        user_id=user_info.id
        access_token,expires_at_access=JWTHandler.generate_access_token(user_id)
        refresh_token, expires_at = JWTHandler.generate_refresh_token(user_id)
        refresh_token_hash = hashlib.sha256(
            refresh_token.encode()
        ).hexdigest()
        refresh_token_record = {
            "user_id": user_id,
            "token_hash": refresh_token_hash,
            "expires_at": expires_at,
            "revoked": False
        }
        print("refresh_token_hash=",  refresh_token_record)
        insert_refresh_token_hash(db, refresh_token_record)
        return access_token,refresh_token
    except ValueError as e:
        print(e)
        raise e

def insert_refresh_token_hash(db,refresh_token):
    try:
        new_record=RefreshTokensDAO.create_refresh_token_record(db,refresh_token)
        db.commit()
        return new_record
    except Exception as e:
        db.rollback()
        print(e)
        raise e

