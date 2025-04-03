from flask import Flask
from src.config import Config
from src.utils.db import db
from src.utils.auth import bcrypt, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    login_manager.init_app(app)
        
    from src.routes.main import main
    from src.routes.usuarios import usuarios
    from src.routes.reportes import reportes
    app.register_blueprint(main)
    app.register_blueprint(usuarios)
    app.register_blueprint(reportes)

    db.init_app(app)
    with app.app_context():
        db.create_all()


    return app

