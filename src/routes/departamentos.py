from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from src.models.departamento import Departamento
from src.forms.departamentos import CrearDepartamento
from src import db
from sqlalchemy.sql import func

departamentos = Blueprint(
    "departamentos", __name__, url_prefix="/departamentos", template_folder="templates"
)


@departamentos.route("/", methods=["GET"])
@login_required
def ver_departamentos():
    departamentos = Departamento.query.all()

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

        tipo_area = request.form["tipo-area"].strip()
        nombre_area = request.form["nombre-area"].strip()
        nombre_coor = request.form["nombre-coor"].strip()
        linea_telefonica = request.form["ext-telefonica"].strip()
        torre = request.form["torre"].strip()
        piso = request.form["piso"].strip()
        ubicacion = f"Torre {torre}, piso {piso}, {tipo_area} {nombre_area}"

        departamento = Departamento(
            tipo=tipo_area,
            nombre=nombre_area,
            ubicacion=ubicacion,
            nombre_coordinador=nombre_coor,
            linea_telefonica=linea_telefonica,
        )
        db.session.add(departamento)
        db.session.commit()

        departamentosToCsv()
        flash("El departamento ha sido registrado exitosamente!", "success")
        return redirect(url_for("departamentos.ver_departamentos"))

    elif request.method == "GET":
        return render_template("departamentos/crear-departamento.html")


@departamentos.route("/departamento/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_departamento(id):
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
    if request.method == "POST":
        departamento = Departamento.query.get_or_404(id)

        db.session.delete(departamento)
        db.session.commit()

        flash(f"El departamento ID #{id} se elimino exitosamente!", "success")
        return redirect(url_for("departamentos.ver_departamentos"))

    elif request.method == "GET":
        abort(403)


# from json import JSONEncoder, JSONDecoder
import csv


def departamentosToCsv():
    departamentos_lista = []
    departamentos_db = Departamento.query.all()
    print()
    print(departamentos_db)

    for dep in departamentos_db:
        id = dep.id
        tipo = dep.tipo
        nombre = dep.nombre
        ubicacion = dep.ubicacion
        nombre_coordinador = dep.nombre_coordinador
        linea_telefonica = dep.linea_telefonica

        dep_diccionario = {
            "id": id,
            "tipo": tipo,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "nombre_coordinador": nombre_coordinador,
            "linea_telefonica": linea_telefonica,
        }

        departamentos_lista.append(dep_diccionario)

    with open("local/csv/departamentos.csv", "w") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "tipo",
                "nombre",
                "ubicacion",
                "nombre_coordinador",
                "linea_telefonica",
            ],
        )

        writer.writeheader()
        for dep in departamentos_lista:
            writer.writerow(dep)

    file.close()