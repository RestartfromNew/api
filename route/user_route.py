from flask import Flask, request, jsonify,Blueprint
from database.database import SessionLocal
from modules.user.service.create_new_user_service import create_new_user_service
bp = Blueprint('first_test_route', __name__)

@bp.route('/register', methods=['POST'])
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