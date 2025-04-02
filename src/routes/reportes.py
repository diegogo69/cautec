from flask import (
    Blueprint, flash, render_template,
    request, redirect, url_for
)
from src.models.reporte import Reporte
from src.models.comentario import Comentario
from src.forms.reportes import CrearReporte
from src import db

reportes = Blueprint('reportes', __name__, url_prefix='/reportes',
                    template_folder='templates')

# from sqlalchemy.orm import asdict
@reportes.route('/reporte/<string:id>')
def ver_reporte(id):
    # crear_comentario.reporte_id = id
    reporte = Reporte.query.get_or_404(id)
    comentarios = Comentario.query.filter_by(reporte_id=id)#.first()
    
    forms = {'crear_comentario': crear_comentario}
    return render_template('reportes/ver-reporte.html',
                           reporte=reporte, comentarios=comentarios,
                           forms=forms)
    


@reportes.route('/crear-reporte', methods=['GET', 'POST'])
def crear_reporte():
    form = CrearReporte()

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
        return render_template('reportes/crear-reporte.html', form=form)



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


# @reportes.route("/crear-comentario/<int:reporte_id>", methods=["POST"])
@reportes.route('/reporte/<int:reporte_id>/crear-comentario', methods=["POST"])
def crear_comentario(reporte_id):
    if request.method == 'POST':
        comentario_cont = request.form['comentario']
        # reporte_id = request.form['reporte_id']
        
        comentario = Comentario(comentario=comentario_cont, reporte_id=reporte_id)

        db.session.add(comentario)
        db.session.commit()
        flash("Tu comentario ha sido registrado exitosamente!", "message")

        return redirect(url_for("reportes.ver_reporte", id=reporte_id))
    return redirect(url_for("reportes.ver_reporte", id=reporte_id))

@reportes.route('/reporte/<int:reporte_id>/eliminar-comentario/<int:id>', methods=["POST"])
def eliminar_comentario(id, reporte_id):
    if request.method == 'POST':
        comentario = Comentario.query.get_or_404(id)
        db.session.delete(comentario)
        db.session.commit()
        
        flash(f'El comentario ID #{id} se elimino exitosamente!', 'message')
        
        return redirect(url_for('reportes.ver_reporte', id=reporte_id))
    
    elif request.method == 'GET':
        flash('Los elementos se eliminan a través del método POST solamente', 'error')
        return redirect(url_for('reportes.ver_reporte', id=reporte_id))
