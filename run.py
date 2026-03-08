from flask import Flask, request, jsonify
from database.database import SessionLocal
from modules.user.service.create_new_user_service import create_new_user_service
from flask_cors import CORS
from modules.user.test.test_dao import test_selection

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})# 👈 关键就是这一行



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

@app.route('/register', methods=['POST'])
def register():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.get_json()
        print("Session received:", data)
        new_user=create_new_user_service(db_session,data)
        print(new_user)
        return jsonify({"message": "success","user_info":new_user.to_dict()}),201

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        print(e)

        return jsonify({
            "error": "internal server error"
        }), 500
    finally:
        db_session.close()

@app.route('/search_by_id_username_email', methods=['GET'])
def search_by_id_username_email():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.args.get("username")
        print("Session received:", data)
        identifier={'username': data}
        selected_user = test_selection(db_session,identifier)
        print(selected_user)
        return jsonify(selected_user.to_dict()),200
        # return jsonify([user.to_dict() for user in selected_user]), 200
    except Exception as e:
        db_session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)