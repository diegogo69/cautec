from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from src.models.usuario import Usuario

class RegistroForm(FlaskForm):
  usuario = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=20)])

  email = StringField('Correo', validators=[DataRequired(), Email()])

  password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=3, max=20)])
  confirm_password = PasswordField(
    'Confirmar contraseña', validators=[DataRequired(), EqualTo('password'), Length(min=3, max=20)]
  )
  
  submit = SubmitField('Registrarse')
  
  def validate_username(self, username):
    #                                    username enter in the form
    user = Usuario.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('El nombre de usuario ya está registrado. Elige uno diferente.')

  def validate_email(self, email):
    #                                    email enter in the form
    user = Usuario.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('El correo ya está registrado. Elige uno diferente.')
  
  
class LoginForm(FlaskForm):
#   email = StringField('Email', validators=[DataRequired(), Email()])
  usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=20)])

  password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=3, max=20)])
  remember = BooleanField('Recordarme')
  submit = SubmitField('Ingresar')


class UpdateAccountForm(FlaskForm):
  usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=20)])

  email = StringField('Correo', validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

  submit = SubmitField('Actualizar')
  

  def validate_username(self, username):
    if username.data != current_user.username:
      #                                    username enter in the form
      user = Usuario.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('El nombre de usuario ya está registrado. Elige uno diferente.')

  def validate_email(self, email):
    if email.data != current_user.email:
      #                                    email enter in the form
      user = Usuario.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('El correo ya está registrado. Elige uno diferente.')
  


class RequestResetForm(FlaskForm):
    email = StringField('Correo',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Restablecer contraseña')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('El nombre de usuario no está registrado. Regístrate y crea una cuenta.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Restablecer contraseña')
    
