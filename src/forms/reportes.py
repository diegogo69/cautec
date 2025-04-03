from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired

class CrearReporte(FlaskForm):
    titulo = StringField('titulo', validators=[DataRequired()])
    descripcion = TextAreaField('descripcion', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=['solicitud', 'incidencia'], validators=[DataRequired()])
    categoria = SelectField('Categoria', choices=['software', 'hardware', 'Selecciona una categoria'])
    
    # estado = SelectField('Estado', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

    submit = SubmitField('Crear')
