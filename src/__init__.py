from flask import Flask
# from flask_mysqldb import MySQL # Usar SQL-Alchemy
from src.config import Config
from src.utils.db import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from src.routes.main import main
    from src.routes.reportes import reportes
    app.register_blueprint(main)
    app.register_blueprint(reportes)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

