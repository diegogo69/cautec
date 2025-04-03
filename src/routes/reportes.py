from flask import (
    Blueprint, flash, render_template,
    request, redirect, url_for, abort
)
from flask_login import current_user, login_required
from src.models.reporte import Reporte
from src.models.comentario import Comentario
from src.forms.reportes import CrearReporte
from src import db
from sqlalchemy.sql import func


reportes = Blueprint('reportes', __name__, url_prefix='/reportes',
                    template_folder='templates')


@reportes.route('/', methods=['GET'])
@login_required
def ver_reportes():
    reportes = Reporte.query.all()
    return render_template('reportes/ver-reportes.html', data={'reportes': reportes})

# from sqlalchemy.orm import asdict
@reportes.route('/reporte/<int:id>', methods=['GET'])
@login_required
def ver_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    comentarios = Comentario.query.filter_by(reporte_id=id)#.first()
    
    return render_template('reportes/ver-reporte.html',
                           reporte=reporte, comentarios=comentarios,
                           )
    

@reportes.route('/crear-reporte', methods=['GET', 'POST'])
@login_required
def crear_reporte():
    form = CrearReporte()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        categoria = request.form['categoria']
        
        reporte = Reporte(titulo=titulo, descripcion=descripcion, tipo=tipo, categoria=categoria,
                          usuario_id=current_user.id)
        db.session.add(reporte)
        db.session.commit()
        
        flash('Tu reporte ha sido registrado exitosamente!', 'message')
        return redirect(url_for('reportes.crear_reporte'))
    
    elif request.method == 'GET':
        return render_template('reportes/crear-reporte.html', form=form)


@reportes.route('/reporte/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    if reporte.usuario_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        reporte.titulo = titulo
        reporte.descripcion = descripcion

        db.session.commit()
        
        flash(f'El reporte ID #{id} fue editado exitosamente!', 'message')
        return redirect(url_for('reportes.ver_reportes'))
    
    elif request.method == 'GET':
        return render_template('reportes/editar-reporte.html', reporte=reporte)


# Ruta para eliminar reporte. Válida sólo para el método POST
@reportes.route('/reporte/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_reporte(id):
    reporte = Reporte.query.get_or_404(id)

    if reporte.usuario_id != current_user.id:
        abort(403)

    db.session.delete(reporte)
    db.session.commit()
    
    flash(f'El reporte ID #{id} se elimino exitosamente!', 'message')
    return redirect(url_for('reportes.ver_reportes'))


@reportes.route('/reporte/<int:reporte_id>/crear-comentario', methods=["POST"])
@login_required
def crear_comentario(reporte_id):
    texto_comentario = request.form['comentario']
    comentario = Comentario(comentario=texto_comentario, reporte_id=reporte_id,
                            usuario_id=current_user.id)

    db.session.add(comentario)
    db.session.commit()

    flash("Tu comentario ha sido registrado exitosamente!", "message")
    return redirect(url_for("reportes.ver_reporte", id=reporte_id))


@reportes.route('/reporte/<int:reporte_id>/eliminar-comentario/<int:id>', methods=["POST"])
@login_required
def eliminar_comentario(id, reporte_id):
    comentario = Comentario.query.get_or_404(id)
    if comentario.usuario_id != current_user.id:
        abort(403)
        
    db.session.delete(comentario)
    db.session.commit()
    
    flash(f'El comentario ID #{id} se elimino exitosamente!', 'message')
    return redirect(url_for('reportes.ver_reporte', id=reporte_id))
