#从请求头中获取token,
#调用请jwt_handler验证，把结果传给路由
#所有和用户数据的服务都应该验证token
from functools import wraps
from flask import request, jsonify, g
#g是Flask 的当前请求上下文临时存储区。
from modules.user.auth.jwt_handler import JWTHandler


def auth_required(func):
    #wrapp保留原函数的名字、注释等信息，不然 Flask 有时会把路由函数信息弄乱。
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("auth middleware triggered")
        auth_header = request.headers.get("Authorization")
        #从发回来的请求头里获取Authorization
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Invalid Authorization format"}), 401

        token = parts[1]
        #token是part[1],如"eyJhbGc..."

        payload = JWTHandler.verify_access_token(token)

        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.current_user_id = payload["sub"]

        return func(*args, **kwargs)

    return wrapper