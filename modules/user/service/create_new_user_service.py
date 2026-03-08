from datetime import datetime, timedelta
import datetime
import pendulum
from modules.user.dao.create_user_dao import create_user_dao
import bcrypt
from modules.user.dao.userDAO import UserDAO
import re
from password_validator import PasswordValidator

# 定义规则
schema = PasswordValidator()
schema.min(8)           # 最少8位
schema.max(100)         # 最多100位
schema.has().uppercase() # 至少1个大写
schema.has().lowercase() # 至少1个小写
schema.has().digits()    # 至少1个数字
schema.has().symbols()   # 至少1个符号
schema.has().no().spaces() # 不能有空格
# 验证密码
def is_validate_password(password: str) -> bool:
    return schema.validate(password)

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def is_valid_email(email: str) -> bool:
    #email是否符合格式
    return re.match(EMAIL_REGEX, email)

def create_new_user_service(db, data):
    try:
        #验证密码和邮箱是否符合格式
        if not is_valid_email(data['email']):
            raise ValueError("Invalid email format")
        if not is_validate_password(data['password']):
            raise ValueError("Invalid password format")
        username=data['username']
        email=data['email']
        userbyId=UserDAO.get_by_username(db, username)
        userbyEmail=UserDAO.get_by_email(db, email)
        #验证邮箱和用户名是否存在
        if  userbyEmail:
            raise ValueError("Email already registered")
        if userbyId:
            raise ValueError("Username already registered")

        password = data.get('password')
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        data['password_hash'] = password_hash
        data['is_active'] = True
        new_user= UserDAO.create_user(db,data)
        db.commit()
        print("提交成功")
        return new_user
    except Exception as e:
        db.rollback()
        print(e)
        raise e

