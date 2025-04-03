import os
import secrets
# from PIL import Image
from flask import current_app, url_for
# from flask_mail import Message
# from src import mail


# RESET AUTHENTICATION
def send_reset_email(user):
    token = user.get_reset_token()
    # msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg = Message('Password Reset Request', sender='diegomaterano03@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    # Catch any possible exection here. Connection, invalid auth, etc. Something went wrong
    mail.send(msg)

# Save input image file
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext # picture filename
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # flask app root path

    # Resize image
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    # form_picture.save(picture_path) Og size img
    img.save(picture_path) # Save resized img instead of og size

    return picture_fn # return picture filename


def remove_picture(picture_name):
    if picture_name != 'default.jpg':
        os.remove(os.path.join(current_app.root_path, 'static/profile_pics', picture_name))
        
      

