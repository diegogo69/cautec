from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from src.models.departamento import Departamento
from src.models.reporte import Reporte
from src.forms.departamentos import CrearDepartamento
from src.utils.departamentos import AREAS_TIPOS
from src import db
from sqlalchemy.sql import func

departamentos = Blueprint(
    "departamentos", __name__, url_prefix="/departamentos", template_folder="templates"
)


@departamentos.route("/", methods=["GET"])
@login_required
def ver_departamentos():
    # departamentos = Departamento.query.all()
    
    page_default = 1
    por_pagina = 10
    pagina = request.args.get('pagina', page_default, type=int)
    departamentos = (
        Departamento.query #.order_by(Departamento.nombre.desc())
            .paginate(page=pagina, per_page=por_pagina)
    )

    return render_template(
        "departamentos/ver-departamentos.html", departamentos=departamentos
    )


# from sqlalchemy.orm import asdict
@departamentos.route("/departamento/<int:id>")
@login_required
def ver_departamento(id):
    departamento = Departamento.query.get_or_404(id)

    form = CrearDepartamento(
        nombre=departamento.nombre,
        ubicacion=departamento.ubicacion,
        nombre_coordinador=departamento.nombre_coordinador,
        linea_telefonica=departamento.linea_telefonica,
    )
    return render_template(
        "departamentos/ver-departamento.html", departamento=departamento, form=form
    )


@departamentos.route("/crear-departamento", methods=["GET", "POST"])
@login_required
def crear_departamento():
    if current_user.tipo != "admin":
        flash("Sólo un usuario administrador tiene permitido esa acción.", "success")
        return redirect(url_for("main.index"))
    # tipo-area
    # nombre-area
    # nombre-coor
    # torre
    # piso
    # ext-telefonica

    if request.method == "POST":
        # nombre = form.nombre.data #request.form['nombre']
        # ubicacion = form.ubicacion.data #request.form['ubicacion']
        # nombre_coordinador = form.nombre_coordinador.data #request.form['nombre_coordinador']
        # linea_telefonica = form.linea_telefonica.data #request.form['linea_telefonica']

        tipo_area = request.form["tipo-area"].strip().lower()
        nombre_area = request.form["nombre-area"].strip()
        nombre_coor = request.form["nombre-coor"].strip()
        linea_telefonica = request.form["ext-telefonica"].strip()
        torre = request.form["torre"].strip().lower()
        piso = request.form["piso"].strip()
        piso_texto = piso if piso != '0' else 'planta baja' 
        ubicacion = f"Torre {torre}, piso {piso_texto}, {tipo_area} {nombre_area}"

        departamento = Departamento(
            tipo=tipo_area,
            torre=torre,
            piso=piso,
            nombre=nombre_area,
            ubicacion=ubicacion,
            nombre_coordinador=nombre_coor,
            linea_telefonica=linea_telefonica,
        )
        db.session.add(departamento)
        db.session.commit()

        flash("El departamento ha sido registrado exitosamente!", "success")
        return redirect(url_for("departamentos.ver_departamentos"))

    elif request.method == "GET":
        return render_template("departamentos/crear-departamento.html")


@departamentos.route("/departamento/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_departamento(id):
    if current_user.tipo != "admin":
        flash("Sólo un usuario administrador tiene permitido esa acción.", "success")
        return redirect(url_for("main.index"))
    
    departamento = Departamento.query.get_or_404(id)
    form = CrearDepartamento()

    if request.method == "POST":
        departamento.nombre = (form.nombre.data,)
        departamento.ubicacion = (form.ubicacion.data,)
        departamento.nombre_coordinador = (form.nombre_coordinador.data,)
        departamento.linea_telefonica = (form.linea_telefonica.data,)

        db.session.commit()

        flash(f"El departamento ID #{id} fue editado exitosamente!", "success")
        return redirect(url_for("departamentos.ver_departamentos"))

    elif request.method == "GET":
        form = CrearDepartamento(
            nombre=departamento.nombre,
            ubicacion=departamento.ubicacion,
            nombre_coordinador=departamento.nombre_coordinador,
            linea_telefonica=departamento.linea_telefonica,
        )
        return render_template(
            "departamentos/editar-departamento.html",
            departamento=departamento,
            form=form,
        )


@departamentos.route("/departamento/<int:id>/eliminar", methods=["GET", "POST"])
@login_required
def eliminar_departamento(id):
    if current_user.tipo != "admin":
        flash("Sólo un usuario administrador tiene permitido esa acción.", "success")
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        departamento = Departamento.query.get_or_404(id)

        # Eliminar el departamento s definir como nulo la propiedad de departamento_id de los reportes asociados
        # No funciona porque el departamento es un primary key en la tabla reportes
        # reportes_asociados = Reporte.query.filter_by(departamento_id=id).all()
        # for reporte in reportes_asociados:
        #     reporte.departamento_id = None

        db.session.delete(departamento)
        db.session.commit()

        flash(f"El departamento ID #{id} se elimino exitosamente!", "success")
        return redirect(url_for("departamentos.ver_departamentos"))

    elif request.method == "GET":
        abort(403)

@departamentos.route("/query", methods=["GET"])
# @departamentos.route("/query/<string:torre>/<string:piso>/<string:tipo>", methods=["GET"])
# def query(torre='none', piso='none', tipo='none'):
def query():
    # Request args method
    torre = request.args.get('torre')
    piso = request.args.get('piso')
    tipo = request.args.get('tipo')

    # Crear un objeto de consula, aplicar filtros condicionalmente, y ejecutar la consulta
    dep_query = Departamento.query # También válido
    # dep_query = db.session.query(Departamento)
    if torre != 'none':
        dep_query = dep_query.filter(Departamento.torre == torre)
    if piso != 'none':
        dep_query = dep_query.filter(Departamento.piso == piso)
    if tipo != 'none':
        dep_query = dep_query.filter(Departamento.tipo == tipo)
    
    # deps = dep_query.order_by(Departamento.tipo).all()
    deps = dep_query.all()
    
    return [dep.to_dict() for dep in deps]