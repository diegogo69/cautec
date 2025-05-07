import os, sys
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
        try:
            if not database_exists(database_uri):
                print(f'La base de datos {database} aun no ha sido creada')
                create_database(database_uri)
                print(f'La base de datos {database} fue creada con exito')
        except Exception as e:
            print('No se pudo establecer conexion con la base de datos. Verifica las credenciales')
            print('Error: ', e)
            sys.exit()
        
    else:
        database_uri = 'sqlite:///cautec.db'
        print('Conexión a la base de datos fallida. Se utilizará una base de datos SQLite')

    return database_uri


# Comprobar si hay usuarios registrados en la base de datos
def primera_vez():
    from src.models.usuario import Usuario
    hay_usuarios = Usuario.query.first()

    print('----- USUARIOS -----')
    print(hay_usuarios)

    if hay_usuarios:
        print('Ya hay usuarios registrados')
        return
        
    print('Aún no hay usuarios registrados')
    tipos_usuario = ['admin', 'soporte', 'solicitante']
    for usuario in tipos_usuario:
        nuevo_usuario = Usuario(
            usuario=usuario,
            password=bcrypt.generate_password_hash(usuario).decode('utf-8'),
            tipo=usuario,
        )

        db.session.add(nuevo_usuario)

    db.session.commit()
    print('Los usuarios por defecto has sido creados exitosamente')
    return
