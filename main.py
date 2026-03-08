from flask import Flask
from route.first_test_route import bp as first_test_bp
from route.user_route import bp as user_route_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(first_test_bp)
    app.register_blueprint(user_route_bp)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)