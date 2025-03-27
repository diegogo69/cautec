from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for
)

app = Flask(__name__)
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "cautec"
app.config["MYSQL_PASSWORD"] = "cautec"
app.config["MYSQL_DB"] = "cautec_db"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
#app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}  # https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes

# Session secret key. CHANGE DEFAULT LATER  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/ver-reporte/<string:id>')
def ver_reporte(id):
    reporte = get_reporte(id)
    
    return render_template('ver-reporte.html', data={'reporte': reporte})
    
    

@app.route('/crear_reporte', methods=['GET', 'POST'])
def crear_reporte():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        
        cursor = db.connection.cursor()
        cursor.execute(
            'INSERT INTO reportes (titulo, descripcion) VALUES (%s, %s)', (
                titulo, descripcion,
            )
        )
        db.connection.commit()
        
        flash('Tu reporte ha sido registrado exitosamente!', 'message')
        
        return redirect(url_for('crear_reporte'))
    
    
    elif request.method == 'GET':
        return render_template('crear-reporte.html')



@app.route('/editar-reporte/<string:id>', methods=['GET', 'POST'])
def editar_reporte(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        
        cursor = db.connection.cursor()
        cursor.execute("""
                UPDATE reportes
                SET titulo = %s,
                    descripcion = %s
                WHERE id = %s
            """, (titulo, descripcion, id,)
        )
        db.connection.commit()
        
        flash(f'El reporte ID #{id} fue editado exitosamente!', 'message')
        
        return redirect(url_for('ver_reportes'))
    
    
    elif request.method == 'GET':
        reporte = get_reporte(id)
       
        return render_template('editar-reporte.html', data={'reporte': reporte})
    
    
    
@app.route('/eliminar-reporte/<string:id>', methods=['GET', 'POST'])
def eliminar_reporte(id):
    if request.method == 'POST':
        cursor = db.connection.cursor()
        cursor.execute(
            'DELETE FROM reportes WHERE id = %s', (
                id,
            )
        )
        db.connection.commit()
        
        flash(f'El reporte ID #{id} se elimino exitosamente!', 'message')
        
        return redirect(url_for('ver_reportes'))
    
    
    elif request.method == 'GET':
        flash('Los elementos se eliminan a través del método POST solamente', 'error')

        return redirect(url_for('ver_reportes'))
        
        
    
@app.route('/ver-reportes', methods=['GET', 'POST'])
def ver_reportes():
    if request.method == 'POST':
        ...
    
    elif request.method == 'GET':
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM reportes')
        reportes = cursor.fetchall()        
       
        return render_template('ver-reportes.html', data={'reportes': reportes})



def get_reporte(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM reportes WHERE id = %s', (id,))
    reporte = cursor.fetchone()
    return reporte