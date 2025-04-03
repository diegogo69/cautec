from flask import (
    Blueprint, flash, render_template,
    request, redirect, url_for, abort
)
from flask_login import current_user, login_required
from src.models.departamento import Departamento
from src.forms.departamentos import CrearDepartamento
from src import db
from sqlalchemy.sql import func

departamentos = Blueprint('departamentos', __name__, url_prefix='/departamentos',
                    template_folder='templates')

@departamentos.route('/ver-departamentos', methods=['GET'])
@login_required
def ver_departamentos():
    departamentos = Departamento.query.all()
    
    return render_template('departamentos/ver-departamentos.html',
                           departamentos=departamentos)

# from sqlalchemy.orm import asdict
@departamentos.route('/departamento/<string:id>')
@login_required
def ver_departamento(id):
    # crear_comentario.reporte_id = id
    departamento = Departamento.query.get_or_404(id)
    # reporte.fecha_atencion = func.now()
    
    forms = {}
    return render_template('departamentos/ver-departamento.html',
                           departamento=departamento, 
                           forms=forms)
    

@departamentos.route('/crear-departamento', methods=['GET', 'POST'])
@login_required
def crear_departamento():
    form = CrearDepartamento()

    if request.method == 'POST':
        nombre = form.nombre.data #request.form['nombre']
        ubicacion = form.ubicacion.data #request.form['ubicacion']
        nombre_coordinador = form.nombre_coordinador.data #request.form['nombre_coordinador']
        linea_telefonica = form.linea_telefonica.data #request.form['linea_telefonica']
        
        departamento = Departamento(nombre=nombre, ubicacion=ubicacion,
                                    nombre_coordinador=nombre_coordinador,
                                    linea_telefonica=linea_telefonica,
                                    )
        db.session.add(departamento)
        db.session.commit()
        
        flash('El departamento ha sido registrado exitosamente!', 'message')
        
        return redirect(url_for('departamentos.crear_departamento'))
    
    
    elif request.method == 'GET':
        return render_template('departamentos/crear-departamento.html', form=form)



@departamentos.route('/editar-departamento/<string:id>', methods=['GET', 'POST'])
@login_required
def editar_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    if departamento.usuario_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        departamento.titulo = titulo
        departamento.descripcion = descripcion

        # db.session.add(reporte)
        db.session.commit()
        
        flash(f'El departamento ID #{id} fue editado exitosamente!', 'message')
        
        return redirect(url_for('departamentos.ver_departamentos'))
    
    
    elif request.method == 'GET':
        return render_template('departamentos/editar-departamento.html', data={'departamento': departamento})
    
    
    
@departamentos.route('/eliminar-departamento/<string:id>', methods=['GET', 'POST'])
@login_required
def eliminar_departamento(id):
    if request.method == 'POST':
        departamento = Departamento.query.get_or_404(id)
        if departamento.usuario_id != current_user.id:
            abort(403)

        db.session.delete(departamento)
        db.session.commit()
        
        flash(f'El departamento ID #{id} se elimino exitosamente!', 'message')
        
        return redirect(url_for('departamentos.ver_departamentos'))
    
    
    elif request.method == 'GET':
        flash('Los elementos se eliminan a través del método POST solamente', 'error')

        return redirect(url_for('departamentos.ver_departamentos'))
        