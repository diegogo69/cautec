The db.create_all() function does not recreate or update a table if it already exists. For example, if you modify your model by adding a new column, and run the db.create_all() function, the change you make to the model will not be applied to the table if the table already exists in the database. The solution is to delete all existing database tables with the db.drop_all() function and then recreate them with the db.create_all() function like so

>>> from src import create_app
Conexión a la base de datos fallida. Se utilizará una base de datos SQLite
>>> app = create_app()
----- USUARIOS -----
Usuario('admin')
Ya hay usuarios registrados
>>> app.app_context().push()

>>> d = Departamento.query
>>> d = d.filter(Departamento.torre == 'e')
>>> d = d.filter(Departamento.piso == '1')
>>> print(d.all())