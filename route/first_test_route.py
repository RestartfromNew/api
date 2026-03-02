from flask import Blueprint, jsonify, request
bp = Blueprint('first_test_route', __name__)
@bp.route('/first_test', methods=['POST'])
def first_test():
    try:
        data = request.get_json()
        print(data)
        return jsonify({"message": "success"}),201
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500