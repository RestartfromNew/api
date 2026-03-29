#生成，验证token
#生成access token
#生成热refresh token
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional,Dict,Any

from modules.user.dao.userDAO import UserDAO

SECRET_KEY="your-super-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 20
class JWTHandler():
    def generate_access_token(user_id:str)->str:
        # expire_time=datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload={
            "sub": str(user_id),
            "type": "access",
            "exp":int(expire_time.timestamp())
        }
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token, expire_time

    def verify_access_token(token:str)-> Optional[Dict[str, Any]]:
        try:
            #解码
            #header-payload-signature,如果当前时间大于exp，就会抛出jwt.ExpiredSignatureError
            #如果token格式不合法，抛出InvalidTokenError
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            if payload.get("type") != "access":
                return None
            return payload
        except jwt.ExpiredSignatureError:
            print("Access Token expired")
            return None

        except jwt.InvalidTokenError:
            print("Invalid Access token")
            return None

    def generate_refresh_token(user_id:str)->str:
        expire_time = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        # expire_time = datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": int(expire_time.timestamp())
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token,expire_time
    def verify_refresh_token(token:str)-> Optional[Dict[str, Any]]:
        try:
            #解码
            #header-payload-signature,如果当前时间大于exp，就会抛出jwt.ExpiredSignatureError
            #如果token格式不合法，抛出InvalidTokenError
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            return payload
        except jwt.ExpiredSignatureError:
            print("Refresh Token expired")
            return None

        except jwt.InvalidTokenError:
            print("Invalid Refresh token")
            return None