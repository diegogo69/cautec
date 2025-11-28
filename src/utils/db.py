import os, sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from src.utils.auth import bcrypt
from pathlib import Path

# Cargar archivo .env con las variables de entorno
# load_dotenv()
# Cargar archivo .env con las variables de entorno en servidor local XAMPP
load_dotenv('C:\\xampp\\htdocs\\cautec\\.env')

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
# Parece que el la aplicación mod_wsgi no carga las variables de entorno de python-dotenv
def get_variables_entorno():
    dialect = os.getenv('DB_DIALECT', None)
    username = os.getenv('DB_USERNAME', None)
    password = os.getenv('DB_PASSWORD', None)
    host = os.getenv('DB_HOST', None)
    port = os.getenv('DB_PORT', None)
    database = os.getenv('DB_DATABASE', None)
    use_sqlite = os.getenv('USE_SQLITE', None)

    print('----- Variables de entorno para la base de datos -----')
    print(dialect, username, password, host, port, database, use_sqlite)
    
    return dialect, username, password, host, port, database, use_sqlite


# Generar una dirección URI (identificador uniforme de recursos) para la conexion a la base de datos
# Se utilizan las credenciales provenientes de variables de entorno
# Si las hay y las credenciales son validas, 
# Se comprueba la existencia de una base de datos homonima al valor de la variable database
# En caso de que la base de datos no exista, se crea.
# Si no se proveen credenciales válidas para la URI, se crea una base de datos SQLite por defecto
# Asegurando que la aplicacion puede ejecutarse
def get_database_uri():
    default_uri = 'sqlite:///cautec.db'
    dialect, username, password, host, port, database, use_sqlite = get_variables_entorno()

    if use_sqlite:
        database_uri = default_uri
        print('----- Se utilizará una base de datos SQLite -----')

    elif (dialect and username and password and host and database):
        print(f'----- Se utilizará una base de datos {dialect} -----')
        database_uri = f'{dialect}://{username}:{password}@{host}:{port}/{database}'

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
        database_uri = default_uri
        print('----- Conexión a la base de datos fallida. Se utilizará una base de datos SQLite -----')

    return database_uri


def crear_usuarios():
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

def crear_dependencias_ula():
    from src.models.departamento import Departamento
    import csv

    hay_departamentos = Departamento.query.first()
    if hay_departamentos:
        return

    
    print(Path(__file__))
    ruta_actual = Path(__file__).parent 
    ruta_src = ruta_actual.parent
    ruta_csv =  ruta_src / 'static' / 'csv' / 'datos_universidad.csv'
    # ruta_csv = Path(__file__).parent.parent.parent / 'datos_universidad.csv'
    # Abre el archivo CSV en modo lectura ('r')
    with open(ruta_csv.absolute(), mode='r', newline='', encoding='utf-8') as archivo_csv:
        # Crea un objeto DictReader
        lector_csv = csv.DictReader(archivo_csv)

        # Itera sobre cada fila del archivo
        for fila in lector_csv:
            # Cada 'fila' es un diccionario
            # Puedes acceder a los valores por el nombre de la columna
            # print(f"Nombre: {fila['Nombre']}, Edad: {fila['Edad']}")

            tipo = fila['tipo'].lower()
            torre = fila['torre'].lower()
            piso = fila['piso']
            nombre = fila['nombre']
            linea_telefonica = fila['ext']

            # piso_texto = piso if piso != '0' else 'planta baja' 
            ubicacion = f"Torre {torre}, piso {piso}, {tipo} {nombre}"

            departamento = Departamento(
                tipo=tipo,
                torre=torre,
                piso=piso,
                nombre=nombre,
                ubicacion=ubicacion,
                linea_telefonica=linea_telefonica,
                # nombre_coordinador=nombre_coor,
            )

            db.session.add(departamento)
                
        db.session.commit()
        print('Departamentos creados exitosamente')


def crear_departamentos_por_defecto():
    from src.utils.departamentos import AREAS_TORRES, AREAS_PISOS, AREAS_TIPOS
    from src.models.departamento import Departamento
    
    hay_departamentos = Departamento.query.first()
    if hay_departamentos:
        return

    for torre in AREAS_TORRES:
        for piso in AREAS_PISOS:
            for tipo in AREAS_TIPOS:
                nombre = f'{tipo.capitalize()} {torre.upper()}{piso}'
                piso_texto = piso if piso != '0' else 'planta baja' 
                ubicacion = f"Torre {torre}, piso {piso_texto}, {tipo} {nombre}"

                departamento = Departamento(
                    tipo=tipo,
                    torre=torre,
                    piso=piso,
                    nombre=nombre,
                    ubicacion=ubicacion,
                    # nombre_coordinador=nombre_coor,
                    # linea_telefonica=linea_telefonica,
                )

                db.session.add(departamento)
                
    db.session.commit()
    print('Departamentos creados exitosamente')

def crear_fallas():
    from src.utils.reportes import FALLAS_DISPOSITIVOS
    from src.models.falla_dispositivo import Falla_Dispositivo

    hay_fallas = Falla_Dispositivo.query.first()
    print('----- Fallas -----')
    print(hay_fallas)

    if hay_fallas:
        print('Ya hay fallas registradas')
        return
        
    print('No hay fallas registradas. Añadiendo fallas predeterminadas')
    for falla in FALLAS_DISPOSITIVOS:
        tipo = falla['tipo']
        predeterminada = falla['predeterminada']
        descripcion = falla['descripcion']
        
        falla_dispositivo = Falla_Dispositivo(
            tipo=tipo,
            predeterminada=predeterminada,
            descripcion=descripcion,
        )

        db.session.add(falla_dispositivo)
                
    db.session.commit()
    print('Fallas registradas exitosamente')

# Comprobar si hay usuarios registrados en la base de datos
def primera_vez():
    crear_usuarios()
    # crear_departamentos_por_defecto()
    crear_dependencias_ula()
    crear_fallas()
    return
