from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from src import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from src.utils.auth import login_manager
from src.models.usuario import Usuario
from src.forms.usuarios import (
    RegistroForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
    CambiarContraseñaForm,
)
from src.utils.usuarios import enviar_correo_recuperacion, notificar_cambio_contrasena

# from src.utils import save_picture, remove_picture, send_reset_email

usuarios = Blueprint("usuarios", __name__)


# Init login manager extension
# Cargar usuario en base al id de usuario de la sesión actual
# Devuelve el usuario correspondiente para ese id
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@usuarios.route("/ver-usuarios", methods=["GET"])
@login_required
def ver_usuarios():
    if current_user.tipo != "admin":
        return redirect(url_for("main.index"))

    query = Usuario.query
    
    page_default = 1
    por_pagina = 20
    pagina = request.args.get('pagina', page_default, type=int)

    usuarios = query.paginate(page=pagina, per_page=por_pagina)
    print(usuarios.first)
    # usuarios = Usuario.query.all()

    return render_template(
        "usuarios/ver-usuarios.html", usuarios=usuarios
    )

@usuarios.route("/registrar-usuario", methods=["GET", "POST"])
@login_required
def registrar_usuario():
    if current_user.tipo != "admin":
        return redirect(url_for("main.index"))

    form = RegistroForm()

    if request.method == 'POST' and form.validate():
        nombre_usuario = form.usuario.data.strip().lower()
        email = form.email.data.strip().lower()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        tipo = request.form.get('tipo').strip()

        nuevo_usuario = Usuario(
            usuario=nombre_usuario,
            email=email,
            password=hashed_password,
            tipo=tipo,
        )
        
        db.session.add(nuevo_usuario)  # add query
        db.session.commit()  # commit changes

        flash("Tu cuenta ha sido creada exitosamente! Ahora puedes ingresar", "success")
        return redirect(url_for("usuarios.ver_usuarios"))
    return render_template("usuarios/registrar-usuario.html", title="Register", form=form)

# Ruta para eliminar reporte. Válida sólo para el método POST
@usuarios.route("/usuario/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if current_user.tipo != 'admin' and current_user.id != usuario.id:
        abort(403)
        return

    if usuario.id == 1:
        # Acción prohibida: esta acción causaría daños permanentes al sistema y no se puede realizar.
        abort(403)
        return

    db.session.delete(usuario)
    db.session.commit()

    flash(f"El usuario ID #{id} se elimino exitosamente!", "success")
    return redirect(url_for("usuarios.ver_usuarios"))

@usuarios.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistroForm()
    print(form.email.label(text="Correo Electrónico"))
    if form.validate_on_submit():
        nombre_usuario = form.usuario.data.strip().lower()
        email = form.email.data.strip().lower()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        nuevo_usuario = Usuario(
            usuario=nombre_usuario,
            email=email,
            password=hashed_password,
            tipo="solicitante"
        )
        
        db.session.add(nuevo_usuario)  # add query
        db.session.commit()  # commit changes

        flash("Tu cuenta ha sido creada exitosamente! Ahora puedes ingresar", "success")
        return redirect(url_for("usuarios.login"))
    return render_template("usuarios/registrarse.html", title="Register", form=form)


@usuarios.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        nombre_usuario = form.usuario.data.strip().lower()
        usuario = Usuario.query.filter_by(usuario=nombre_usuario).first()

        if not usuario:
            flash(
                "El nombre de usuario no está registrado. Verificalo o registrate",
                "danger"
            )

        elif usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember=form.remember.data)

            # Verificar si el usuario debe cambiar su contraseña
            if notificar_cambio_contrasena(current_user):
                return redirect(url_for('usuarios.cambiar_contrasena_primera_vez'))

            # If next arg from previous attempt to acces a route without logged in. Redirect to that attempted route
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.index"))

        else:
            flash(
                "No se ha podido ingresar. Por favor verifica el correo y la contraseña",
                "danger",
            )
    return render_template("usuarios/login.html", title="Login", form=form)


@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("usuarios.login"))


@usuarios.route("/cuenta", methods=["GET", "POST"])
@login_required
def cuenta():
    form = UpdateAccountForm()
    # ON POST METHOD AS SUMBIT FORM
    if form.validate_on_submit():
        current_user.usuario = form.usuario.data.strip().lower()
        current_user.email = form.email.data.strip().lower()
        db.session.commit()

        flash("Tu cuenta ha sido actualizada exitosamente!", "success")
        return redirect(url_for("usuarios.cuenta"))
    # Populate form with current user email and username
    elif request.method == "GET":
        form.usuario.data = current_user.usuario
        form.email.data = current_user.email

    return render_template(
        "usuarios/cuenta.html", title="Account", form=form, usuario=current_user
    )  # , profile_img=profile_img


@usuarios.route("/cambiar-contrasena", methods=["GET", "POST"])
@login_required
def cambiar_contrasena():
    form = CambiarContraseñaForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password_actual.data):
            hashed_password = bcrypt.generate_password_hash(form.nueva_password.data).decode("utf-8")
            current_user.password = hashed_password
            db.session.commit()
            flash("Tu contraseña ha sido actualizada exitosamente!", "success")
            return redirect(url_for("usuarios.cuenta"))
        else:
            flash("La contraseña actual es incorrecta. Inténtalo de nuevo.", "danger")
    return render_template("usuarios/cambiar-contraseña.html", title="Cambiar contraseña", form=form)

# Ruta para cambiar la contraseña la primera vez que un usuario por defecto inicia sesión
@usuarios.route("/cambiar-contrasena-primera-vez", methods=["GET", "POST"])
@login_required
def cambiar_contrasena_primera_vez():
    form = CambiarContraseñaForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password_actual.data):
            hashed_password = bcrypt.generate_password_hash(form.nueva_password.data).decode("utf-8")
            current_user.password = hashed_password
            db.session.commit()
            flash("Tu contraseña ha sido actualizada exitosamente!", "success")
            return redirect(url_for("usuarios.cuenta"))
        else:
            flash("La contraseña actual es incorrecta. Inténtalo de nuevo.", "danger")
    return render_template("usuarios/cambiar-contraseña-primera-vez.html", form=form)

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


@usuarios.route("/restablecer-contraseña", methods=['GET', 'POST'])
def restablecer_contrasena():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data.strip().lower()).first()
        try:
            enviar_correo_recuperacion(user)
        except Exception as e:
            print(f"No se pudo enviar el correo de restablecimiento. Error: {e}")
            flash('Algo salió mal, el correo de restablecimiento no pudo ser enviado. Intenta más tarde', 'danger')
            return redirect(url_for('usuarios.login'))
        flash('Se te ha enviado un mensaje a tu correo para restablecer la contraseña.', 'info')
        return redirect(url_for('usuarios.login'))
    return render_template('usuarios/restablecer-contrasena.html', form=form)


@usuarios.route("/restablecer-contraseña/<token>", methods=['GET', 'POST'])
def token_restablecer_contrasena(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = Usuario.verify_reset_token(token)
    if not user:
        flash('El token es inválido o ha expirado.', 'warning')
        return redirect(url_for('usuarios.restablecer_contrasena'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('¡Tu contraseña se ha restablecido correctamente! Ahora puedes acceder a tu cuenta.', 'success')
        return redirect(url_for('usuarios.login'))
    return render_template('usuarios/token-restablecer-contrasena.html', form=form)
