El sistema carga las credenciales para la conexion a la base de datos desde variables de entorno. Si no hay variables de entorno registradas, el sistema crea un base de datos SQLite por defecto.

Para la conexion a la base de datos se esperan valores para:
dialect, es el sistema que SQLAlchemy utiliza para comunicarse con diversos tipos de implementaciones de DBAPI (databse api) y bases de datos

A basic SQLAlchemy database connection URL uses the following format:
Username, password, host, and port are optional depending on the database type and configuration.
dialect://username:password@host:port/database
Here are some example connection strings:
 SQLite, relative to Flask instance path
sqlite:///project.db
 PostgreSQL
postgresql://scott:tiger@localhost/project
 MySQL / MariaDB
mysql://scott:tiger@localhost/project
 Cargar variables de entorno

Error usuario incorrecto:
Error:  (MySQLdb.OperationalError) (1045, "Access denied for user 'caute'@'localhost' (using password: YES)")

Error contraseña incorrecta:
Error:  (MySQLdb.OperationalError) (1045, "Access denied for user 'cautec'@'localhost' (using password: YES)")
(Background on this error at: https://sqlalche.me/e/20/e3q8)