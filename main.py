import os
import logging
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from route.first_test_route import bp as first_test_bp
app = Flask(__name__)
def creat_app():
    app = Flask(__name__)
    # db = SQLAlchemy()
    # db.init_app(app)
    app.register_blueprint(first_test_bp)
    return app

Api=creat_app()
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0", port=8000)