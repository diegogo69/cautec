from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from src.utils.usuarios import notificar_cambio_contrasena
from src.forms.usuarios import CambiarContraseñaForm

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
# @main.route('/inicio')
# @login_required
def index():
    # Si el usuario está autenticado, redirigir a su panel de control sino redigir a la pagina de login
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        # Redirigir a la página de login
        return redirect(url_for('usuarios.login'))

# Ejecutar función después de cada solicitud @main.before_request
