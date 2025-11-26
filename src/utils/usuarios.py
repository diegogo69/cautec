import os
import secrets
# from PIL import Image
from flask import current_app, url_for, flash, redirect
from src.utils.auth import mail
from flask_mail import Message
from src import bcrypt
# from src.routes.usuarios import cambiar_contrasena


# Funcion para verificar si el usuario actual es un usuario por defecto y si no ha cambiado su contraseña
def verificar_usuario_por_defecto(user):
    print(user.id)
    if user.id in (1, 2, 3):
        match user.tipo:
            case 'admin':
                contrasena = 'admin'      # Usuario admin
            case 'soporte':
                contrasena = 'soporte'    # Usuario tecnico
            case _:
                contrasena = 'solicitante' # Usuario solicitante
        if bcrypt.check_password_hash(user.password, contrasena):
            print('si es')
            return True
        print('no es')
        print(contrasena)
    return False

def notificar_cambio_contrasena(current_user_):
    if current_user_.is_authenticated:
        print('Verificando si el usuario debe cambiar su contraseña...')
        if current_user_.is_authenticated and verificar_usuario_por_defecto(current_user_):
            # flash('Por razones de seguridad, debes cambiar tu contraseña antes de continuar.', 'warning')
            return True
    return False

# RESET AUTHENTICATION
def enviar_correo_recuperacion(user):
    token = user.get_reset_token()
    # msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg = Message('Restablecer contraseña Cautec',
                  sender='diegomaterano03@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Para restablecer tu contraseña haz click en el siguiente enlace:
{url_for('usuarios.token_restablecer_contrasena', token=token, _external=True)}

Si no realizaste esta solicitud, simplemente ignora este correo.
'''
    # Catch any possible exection here. Connection, invalid auth, etc. Something went wrong
    mail.send(msg)

# Save input image file
# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext # picture filename
#     picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # flask app root path

#     # Resize image
#     output_size = (125, 125)
#     img = Image.open(form_picture)
#     img.thumbnail(output_size)
#     # form_picture.save(picture_path) Og size img
#     img.save(picture_path) # Save resized img instead of og size

#     return picture_fn # return picture filename


# def remove_picture(picture_name):
#     if picture_name != 'default.jpg':
#         os.remove(os.path.join(current_app.root_path, 'static/profile_pics', picture_name))
        
      

