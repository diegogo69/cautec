from flask import (
    Blueprint, flash, render_template,
    request, redirect, url_for
)

from src import db

reportes = Blueprint('reportes', __name__, url_prefix='/reportes',
                    template_folder='templates')


@reportes.route('/ver-reporte/<string:id>')
def ver_reporte(id):
    reporte = get_reporte(id)
    
    return render_template('reportes/ver-reporte.html', data={'reporte': reporte})
    


@reportes.route('/crear-reporte', methods=['GET', 'POST'])
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
        
        return redirect(url_for('reportes.crear_reporte'))
    
    
    elif request.method == 'GET':
        return render_template('reportes/crear-reporte.html')



@reportes.route('/editar-reporte/<string:id>', methods=['GET', 'POST'])
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
        
        return redirect(url_for('reportes.ver_reportes'))
    
    
    elif request.method == 'GET':
        reporte = get_reporte(id)
       
        return render_template('reportes/editar-reporte.html', data={'reporte': reporte})
    
    
    
@reportes.route('/eliminar-reporte/<string:id>', methods=['GET', 'POST'])
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
        
        return redirect(url_for('reportes.ver_reportes'))
    
    
    elif request.method == 'GET':
        flash('Los elementos se eliminan a través del método POST solamente', 'error')

        return redirect(url_for('reportes.ver_reportes'))
        
        
    
@reportes.route('/ver-reportes', methods=['GET', 'POST'])
def ver_reportes():
    if request.method == 'POST':
        ...
    
    elif request.method == 'GET':
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM reportes')
        reportes = cursor.fetchall()        
       
        return render_template('reportes/ver-reportes.html', data={'reportes': reportes})



def get_reporte(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM reportes WHERE id = %s', (id,))
    reporte = cursor.fetchone()
    return reporte