from flask import Flask, request, jsonify
from database.database import SessionLocal
from service.create_new_user_service import create_new_user_service
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})# 👈 关键就是这一行

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("Register received:", data)
    return jsonify({"message": "User registered", "data": data})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("Login received:", data)
    return jsonify({"access_token": "fake-token"})
@app.route("/profile", methods=["GET"])
def profile():
    data = request.get_json()
    print("Profile received:", data)
    return jsonify({"message": "Profile received"})

@app.route('/create_session', methods=['POST'])
def create_session():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.get_json()
        print("Session received:", data)
        db_session=create_new_user_service(db_session,data)
        db_session.commit()
        return jsonify({"message": "success"}),201
    except Exception as e:
        db_session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)