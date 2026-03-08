from flask import session

from modules.user.models.user_model import User
import bcrypt
def create_user_dao(db,new_user_info):
    try:
        password=new_user_info.get('password')
        password_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        new_user=User.create(
            username=new_user_info.get('username'),
            email=new_user_info.get('email'),
            password_hash=password_hash,
        )
        db.add(new_user)
        db.flush()
        return new_user
    except Exception as e:
        print(e)
        raise e

