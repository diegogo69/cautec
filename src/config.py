import os
from src.utils.db import get_database_uri
from dotenv import load_dotenv
load_dotenv()

database_uri = get_database_uri()

# Configuración de la aplicación agrupada en una clase
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto') # Usa una clave segura
    # Conección Flask-SQLAlchemy: MySQL / MariaDB o SQLite
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración para Flask-Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # Variables de entorno para correo y contraseña
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    