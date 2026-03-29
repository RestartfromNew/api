from flask import Blueprint, jsonify, request
from database.database import SessionLocal
bp = Blueprint('first_test_route', __name__)
@bp.route('/first_test', methods=['POST','GET'])
def first_test():
    try:
        data = request.get_json()
        print(data)
        return jsonify({"message": "success"}),201
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500

@bp.route('/test', methods=['GET','POST'])
def test():
    return jsonify({"message": "received"})

@bp.route('/create_session', methods=['POST'])
def create_session():
    db_session = SessionLocal()
    print(db_session)
    try:
        data = request.get_json()
        db_session.commit()
        return jsonify({"message": "success"}),201
    except Exception as e:
        db_session.rollback()
        print(e)
    finally:
        db_session.close()

