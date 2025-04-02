import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# db = MySQL()
class SQLAlchemyBase(DeclarativeBase):
    __abstract__ = True
    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
    def to_list(self):
        return [{field.name:getattr(self, field.name)} for field in self.__table__.c]
    pass

db = SQLAlchemy(model_class=SQLAlchemyBase)
# Cargar variables de entorno
def get_database_uri():
    load_dotenv()
    # Obtener valores de las credenciales de la base de datos MySQL
    # Se proveen valores por defecto para asegurar que la aplicación funcione normalmente
    username = os.getenv('DB_USERNAME', None)
    password = os.getenv('DB_PASSWORD', None)
    host = os.getenv('DB_HOST', None)
    database = os.getenv('DB_DATABASE', None)

    # Conectarse a una base de datos MySQL si se proveen las credenciales
    # O conectarse a una base de datos SQLite por defecto
    if username and password and host and database:
        database_uri = f'mysql://{username}:{password}@{host}/{database}'
    else:
        database_uri = 'sqlite:///cautec.db'

    return database_uri