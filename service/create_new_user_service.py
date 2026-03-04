from datetime import datetime, timedelta
import datetime
import pendulum
from dao.create_user_dao import create_user_dao
import bcrypt
def create_new_user_service(db, data):
    password = data.get('password')
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    data['password_hash'] = password_hash
    data['is_active'] = True
    data['created_at'] = pendulum.now("UTC")
    data['updated_at'] =pendulum.now("UTC")
    create_user_dao(db, data)
    return db