
from modules.user.dao.userDAO import UserDAO
import hashlib
import bcrypt
from modules.user.dao.refresh_tokenDAO import RefreshTokensDAO
from modules.user.dao.oauthDAO import OauthDAO
from modules.user.service.create_new_user_service import CreateNewUserService
from modules.user.auth.jwt_handler import JWTHandler


def insert_refresh_token_hash(db, refresh_token):
    try:
        new_record = RefreshTokensDAO.create_refresh_token_record(db, refresh_token)
        db.commit()
        return new_record
    except Exception as e:
        db.rollback()
        print(e)
        raise e
class LoginService:

    def login_service(db,data):
        try:
            #通过username 或者 email查找用户
            password = data["password"]
            login_info=data["user_info"]
            #现在将user登陆取消，email登陆允许
            user_info=UserDAO.get_by_email(db,login_info)
            if not user_info:
                raise ValueError('No such user')
            if not bcrypt.checkpw(
                        password.encode("utf-8"),
                        user_info.password_hash.encode("utf-8")):
                raise ValueError("Incorrect password")
            user_id=user_info.id
            user_email=user_info.email
            user_name=user_info.username
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
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "user_id": user_id,
                    "username": user_name,
                    "email": user_email
                }
            }
        except ValueError as e:
            print(e)
            raise e

    def oauth_login_service(db,data):
        try:
            provider = data["provider"]
            provider_user_id=data["provider_user_id"]
            email=data["email"]
            user_name=data["username"]
            message=  ""
            #查找这个授权用户是否存在
            oauth_user=OauthDAO.get_oauth_user_by_provider_id(db, provider=provider,provider_user_id=provider_user_id)
            if not oauth_user:
                #不存在，在user表中创建这个用户
                oauth_user_info={
                    "provider": provider,
                    "provider_user_id": provider_user_id,
                    "email": email,
                    "username": user_name,
                }
                #如果
                new_user_record=CreateNewUserService.create_oauth_user(db,oauth_user_info)

                #获取user_id,
                user_id= new_user_record.id
                #创建oauth表记录
                oauth_user_table_info={
                    "provider": provider,
                    "provider_user_id": provider_user_id,
                    "user_id": user_id,
                }
                new_oauth_user=OauthDAO.create_oauth_user(db,oauth_user_table_info)
                message="New User Created"
            else:
                user_id = oauth_user.user_id
                message="email already exists, binding Oauth User successfully"
            access_token, expires_at_access = JWTHandler.generate_access_token(user_id)
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
            print("refresh_token_hash=", refresh_token_record)
            insert_refresh_token_hash(db, refresh_token_record)
            return {

                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "user_id": user_id,
                    },
                "message": message

            }

        except Exception as e:
            print(e)
            raise e





