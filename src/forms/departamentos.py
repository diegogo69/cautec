from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired

class CrearDepartamento(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired()])
    ubicacion = StringField('Ubicacion:', validators=[DataRequired()])
    nombre_coordinador = StringField('Coordinador:')
    linea_telefonica = StringField('Linea telefonica:')
    
    # estado = SelectField('Estado', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

    submit = SubmitField('Registrar')