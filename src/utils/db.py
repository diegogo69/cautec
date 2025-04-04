import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from src.utils.auth import bcrypt

# db = MySQL()
class SQLAlchemyBase(DeclarativeBase):
    __abstract__ = True
    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
    def to_list(self):
        return [{field.name:getattr(self, field.name)} for field in self.__table__.c]
    pass

db = SQLAlchemy(model_class=SQLAlchemyBase)


# Cargar valores de variables de entorno para las credenciales de la base de datos
# Se proveen un valor explicito por defecto de None
def get_variables_entorno():
    load_dotenv()
    dialect = os.getenv('DB_DIALECT', None)
    username = os.getenv('DB_USERNAME', None)
    password = os.getenv('DB_PASSWORD', None)
    host = os.getenv('DB_HOST', None)
    database = os.getenv('DB_DATABASE', None)

    return dialect, username, password, host, database


# Generar una dirección URI (identificador uniforme de recursos) para la conexion a la base de datos
# Se utilizan las credenciales provenientes de variables de entorno
# Si las hay y las credenciales son validas, 
# Se comprueba la existencia de una base de datos homonima al valor de la variable database
# En caso de que la base de datos no exista, se crea.
# Si no se proveen credenciales válidas para la URI, se crea una base de datos SQLite por defecto
# Asegurando que la aplicacion puede ejecutarse
def get_database_uri():
    dialect, username, password, host, database = get_variables_entorno()

    if (dialect and username and password and host and database):
        database_uri = f'{dialect}://{username}:{password}@{host}/{database}'

        from sqlalchemy_utils import database_exists, create_database
        if not database_exists(database_uri):
            print(f'La base de datos {database} aun no ha sido creada')
            create_database(database_uri)
            print(f'La base de datos {database} fue creada con exito')
    else:
        database_uri = 'sqlite:///cautec.db'
        print('Conexión a la base de datos fallida. Se utilizará una base de datos SQLite')

    return database_uri


