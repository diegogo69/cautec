import os
from src.utils.db import get_database_uri

database_uri = get_database_uri()

# Configuración de la aplicación agrupada en una clase
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') # Usa una clave segura
    # Conección Flask-SQLAlchemy: MySQL / MariaDB o SQLite
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
