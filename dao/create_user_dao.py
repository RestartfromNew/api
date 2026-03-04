from flask import session

from models.user_model import User
import bcrypt
def create_user_dao(db,new_user_info):
    try:
        password=new_user_info.get('password')
        password_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        new_user = User(
            email=new_user_info.get('email'),
            username=new_user_info.get('username'),
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
            created_at=new_user_info.get('created_at'),
            updated_at=new_user_info.get('updated_at'),
        )
        db.add(new_user)
        db.flush()
        return new_user
    except Exception as e:
        print(e)
        raise e

