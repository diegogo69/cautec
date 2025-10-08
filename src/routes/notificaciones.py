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
    return render_template('_notificaciones.html', notificaciones=nots)

@notificaciones.route('/marcar-leidas', methods=['POST'])
@login_required
def marcar_leidas():
    cantidad = marcar_todas_leidas(current_user.id)
    flash(f'{cantidad} notificaciones marcadas como leidas', 'success')
    return redirect(url_for('main.index'))
