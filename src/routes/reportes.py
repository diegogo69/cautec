from flask import (
    Blueprint, flash, render_template,
    request, redirect, url_for
)
from src.models.reporte import Reporte
from src import db

reportes = Blueprint('reportes', __name__, url_prefix='/reportes',
                    template_folder='templates')


@reportes.route('/ver-reporte/<string:id>')
def ver_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    
    return render_template('reportes/ver-reporte.html', data={'reporte': reporte})
    


@reportes.route('/crear-reporte', methods=['GET', 'POST'])
def crear_reporte():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        categoria = request.form['categoria']
        
        reporte = Reporte(titulo=titulo, descripcion=descripcion, tipo=tipo, categoria=categoria)
        db.session.add(reporte)
        db.session.commit()
        
        flash('Tu reporte ha sido registrado exitosamente!', 'message')
        
        return redirect(url_for('reportes.crear_reporte'))
    
    
    elif request.method == 'GET':
        return render_template('reportes/crear-reporte.html')



@reportes.route('/editar-reporte/<string:id>', methods=['GET', 'POST'])
def editar_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        reporte.titulo = titulo
        reporte.descripcion = descripcion

        # db.session.add(reporte)
        db.session.commit()
        
        flash(f'El reporte ID #{id} fue editado exitosamente!', 'message')
        
        return redirect(url_for('reportes.ver_reportes'))
    
    
    elif request.method == 'GET':
        return render_template('reportes/editar-reporte.html', data={'reporte': reporte})
    
    
    
@reportes.route('/eliminar-reporte/<string:id>', methods=['GET', 'POST'])
def eliminar_reporte(id):
    if request.method == 'POST':
        reporte = Reporte.query.get_or_404(id)
        db.session.delete(reporte)
        db.session.commit()
        
        flash(f'El reporte ID #{id} se elimino exitosamente!', 'message')
        
        return redirect(url_for('reportes.ver_reportes'))
    
    
    elif request.method == 'GET':
        flash('Los elementos se eliminan a través del método POST solamente', 'error')

        return redirect(url_for('reportes.ver_reportes'))
        
        
    
@reportes.route('/ver-reportes', methods=['GET'])
def ver_reportes():
    reportes = Reporte.query.all()
    
    return render_template('reportes/ver-reportes.html', data={'reportes': reportes})
