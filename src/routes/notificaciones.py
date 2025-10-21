from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from src.models.notificacion import Notificacion
from src import db
from src.utils.notificaciones import marcar_todas_leidas

notificaciones = Blueprint('notificaciones', __name__, template_folder='templates', url_prefix='/notificaciones')

@notificaciones.route('/')
@login_required
def ver_notificaciones():
    # obtener ultimas 20 notificaciones del usuario
    nots = Notificacion.query.filter_by(usuario_id=current_user.id).order_by(Notificacion.fecha.desc()).limit(50).all()
    return render_template('notificaciones/ver-notificaciones.html', notificaciones=nots)

@notificaciones.route('/marcar-leidas', methods=['POST'])
@login_required
def marcar_leidas():
    cantidad = marcar_todas_leidas(current_user.id)
    # flash(f'{cantidad} notificaciones marcadas como leidas', 'success')
    return redirect(url_for('main.index'))


@notificaciones.route('/ver/<int:notificacion_id>')
@login_required
def ver_notificacion(notificacion_id):
    n = Notificacion.query.get_or_404(notificacion_id)
    # Solo permitir que el usuario dueño acceda
    if n.usuario_id != current_user.id:
        flash('No tienes permiso para ver esa notificación', 'warning')
        return redirect(url_for('main.index'))

    try:
        n.leido = True
        db.session.commit()
    except Exception:
        db.session.rollback()

    # Redirigir al reporte relacionado si existe
    if n.reporte_id:
        return redirect(url_for('reportes.ver_reporte', id=n.reporte_id))

    return redirect(url_for('main.index'))
