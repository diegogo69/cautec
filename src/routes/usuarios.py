from flask import render_template, url_for, flash, redirect, request, Blueprint
from src import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from src.utils.auth import login_manager
from src.models.usuario import Usuario
from src.forms.usuarios import (RegistroForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
# from src.utils import save_picture, remove_picture, send_reset_email

usuarios = Blueprint('usuarios', __name__)


# Init login manager extension
# Cargar usuario en base al id de usuario de la sesión actual
# Devuelve el usuario correspondiente para ese id
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@usuarios.route("/registrarse", methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistroForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = Usuario(usuario=form.usuario.data, email=form.email.data, password=hashed_password,
                          tipo='solicitante')
        db.session.add(usuario) # add query
        db.session.commit() # commit changes

        flash('Tu cuenta ha sido creada exitosamente! Ahora puedes ingresar', 'success')
        return redirect(url_for('usuarios.login'))
    return render_template('usuarios/registrarse.html', title='Register', form=form)


@usuarios.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(usuario=form.usuario.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            # If next arg from previous attempt to acces a route without logged in. Redirect to that attempted route
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))

        else:
            flash('No se ha podido ingresar. Por favor verifica el correo y la contraseña', 'danger')
    return render_template('usuarios/login.html', title='Login', form=form)


@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@usuarios.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    # ON POST METHOD AS SUMBIT FORM
    if form.validate_on_submit():
        # if form.picture.data:
        #     # Remove old pictore before updating. Might be optional to store all images
        #     remove_picture(current_user.image_file)
        #     picture_file = save_picture(form.picture.data)
        #     current_user.image_file = picture_file
        current_user.usuario = form.usuario.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Tu cuenta ha sido actualizada exitosamente!', 'success')
        return redirect(url_for('usuarios.account'))
    # Populate form with current user email and username
    elif request.method == 'GET':
        form.usuario.data = current_user.usuario
        form.email.data = current_user.email
    
    # profile_img = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('usuarios/account.html', title='Account', form=form) #, profile_img=profile_img


# PAGINATION PAGE FOR SPECIFIC USER POSTS
@usuarios.route("/user/<string:username>")
def user_posts(username):
    pass
    # page = request.args.get('page', 1, type=int)
    # user = Usuario.query.filter_by(username=username).first_or_404()
    # posts = Post.query.filter_by(author=user)\
    #     .order_by(Post.date_posted.desc())\
    #     .paginate(page=page, per_page=5)
    # return render_template('usuarios/user_posts.html', posts=posts, user=user)


@usuarios.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    pass
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = Usuario.query.filter_by(email=form.email.data).first()
#         try:
#             send_reset_email(user)
#         except Exception as e:
#             flash('Something went wrong, the email could not be sent. Try again later.', 'danger')
#             return redirect(url_for('usuarios.login'))            
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('usuarios.login'))
#     return render_template('usuarios/reset_request.html', title='Reset Password', form=form)


@usuarios.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    pass
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = Usuario.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('usuarios.reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('usuarios.login'))

#     flash('User validation succesful. You can now reset your password', 'info')
#     return render_template('usuarios/reset_token.html', title='Reset Password', form=form)
