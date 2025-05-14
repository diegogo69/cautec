from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from src.models.reporte import Reporte
from src.models.comentario import Comentario
from src.models.departamento import Departamento
from src.utils.departamentos import departamentos_json, AREAS_TIPOS, AREAS_TORRES, AREAS_PISOS
from src.utils.reportes import TIPOS_DISPOSITIVOS, FALLAS_DISPOSITIVOS, ESTADOS_REPORTE
from src import db
from sqlalchemy.sql import func
from datetime import datetime


reportes = Blueprint(
    "reportes", __name__, url_prefix="/reportes", template_folder="templates"
)


@reportes.route("/", methods=["GET"])
@login_required
def ver_reportes():
    reportes = Reporte.query.all()
    return render_template("reportes/ver-reportes.html", data={"reportes": reportes})


# from sqlalchemy.orm import asdict
@reportes.route("/reporte/<int:id>", methods=["GET"])
@login_required
def ver_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    departamento = Departamento.query.get_or_404(reporte.departamento_id)
    comentarios = Comentario.query.filter_by(reporte_id=id).all()
    reporte.falla = FALLAS_DISPOSITIVOS[int(reporte.falla_id)]
    reporte.tipo_dispositivo = TIPOS_DISPOSITIVOS[int(reporte.tipo_dispositivo_id)]
    reporte.estados = ESTADOS_REPORTE

    return render_template(
        "reportes/ver-reporte.html",
        reporte=reporte,
        departamento=departamento,
        comentarios=comentarios,
    )


@reportes.route("/crear-reporte", methods=["GET", "POST"])
@login_required
def crear_reporte():
    if request.method == "POST":
        # titulo = request.form['titulo']
        # descripcion = request.form['descripcion']
        # tipo = request.form['tipo']
        # categoria = request.form['categoria']
        # departamento_id = 1
        # equipo_asociado = request.form['equipo_asociado']

        nombre_sol = request.form["nombre-sol"].strip()
        apellido_sol = request.form["apellido-sol"].strip()

        tipo_area = request.form["tipo-area"].strip()
        reporte_area = request.form["nombre-area"].strip()
        torre = request.form["torre"].strip()
        piso = request.form["piso"].strip()
        ext_telefonica = request.form["ext-telefonica"].strip()

        tipo_dispositivo = request.form["tipo-dispositivo"].strip()
        cod_bienes = request.form["cod-bienes"].strip()
        falla = request.form["falla"].strip()
        fecha_visita = request.form["fecha-visita"].strip()

        nombre_solicitante = f"{nombre_sol} {apellido_sol}"

        # departamento = Departamento.query.get(departamento_id)
        # if not departamento:
        #     departamento_id = None

        reporte = Reporte(
            nombre_solicitante=nombre_solicitante,
            tipo_dispositivo_id=tipo_dispositivo,
            cod_bienes_dispositvo=cod_bienes,
            falla_id=falla,
            fecha_visita=datetime.fromisoformat(fecha_visita),
            usuario_id=current_user.id,
            departamento_id=reporte_area,
        )

        db.session.add(reporte)
        db.session.commit()

        flash("Tu reporte ha sido registrado exitosamente!", "success")
        return redirect(url_for("reportes.ver_reportes"))

    elif request.method == "GET":
        areas = {}
        areas["areas"] = departamentos_json()
        areas["tipos"] = AREAS_TIPOS
        areas['torres'] = AREAS_TORRES
        areas['pisos'] = AREAS_PISOS

        dispositivos = {}
        dispositivos['tipos'] = TIPOS_DISPOSITIVOS
        dispositivos['fallas'] = FALLAS_DISPOSITIVOS

        return render_template("reportes/crear-reporte.html",
                               areas=areas,
                               dispositivos=dispositivos,
                               enumerate=enumerate
                            )

@reportes.route("/reporte/<int:id>/actualizar", methods=["POST"])
@login_required
def actualizar_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    if reporte.usuario_id != current_user.id:
        abort(403)

    estado = request.form["estado"]
    # fecha_emision = request.form["fecha_emision"]
    fecha_visita = request.form["fecha_visita"] # 2025-05-25T12:12
    # fecha_atencion = request.form["fecha_atencion"]
    # fecha_cierre = request.form["fecha_cierre"]
    # solicitante = request.form["solicitante"]
    # departamento = request.form["departamento"]
    # ubicacion = request.form["ubicacion"]
    # tipo = request.form["tipo"]
    # falla = request.form["falla"]
    # cod_bienes = request.form["cod_bienes"]

    reporte.estado = estado
    reporte.fecha_visita = datetime.fromisoformat(fecha_visita)
    
    db.session.commit()

    flash(f"El reporte ID #{id} fue actualizado exitosamente!", "success")
    return redirect(url_for("reportes.ver_reporte", id=reporte.id))


@reportes.route("/reporte/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_reporte(id):
    reporte = Reporte.query.get_or_404(id)
    if reporte.usuario_id != current_user.id:
        abort(403)

    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]

        reporte.titulo = titulo
        reporte.descripcion = descripcion

        db.session.commit()

        flash(f"El reporte ID #{id} fue editado exitosamente!", "success")
        return redirect(url_for("reportes.ver_reportes"))

    elif request.method == "GET":
        return render_template("reportes/editar-reporte.html", reporte=reporte)


# Ruta para eliminar reporte. Válida sólo para el método POST
@reportes.route("/reporte/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_reporte(id):
    reporte = Reporte.query.get_or_404(id)

    if reporte.usuario_id != current_user.id:
        abort(403)

    db.session.delete(reporte)
    db.session.commit()

    flash(f"El reporte ID #{id} se elimino exitosamente!", "success")
    return redirect(url_for("reportes.ver_reportes"))


@reportes.route("/reporte/<int:reporte_id>/crear-comentario", methods=["POST"])
@login_required
def crear_comentario(reporte_id):
    texto_comentario = request.form["comentario"]
    comentario = Comentario(
        comentario=texto_comentario, reporte_id=reporte_id, usuario_id=current_user.id
    )

    db.session.add(comentario)
    db.session.commit()

    flash("Tu comentario se añadió exitosamente!", "success")
    return redirect(url_for("reportes.ver_reporte", id=reporte_id))


@reportes.route(
    "/reporte/<int:reporte_id>/eliminar-comentario/<int:id>", methods=["POST"]
)
@login_required
def eliminar_comentario(id, reporte_id):
    comentario = Comentario.query.get_or_404(id)
    if comentario.usuario_id != current_user.id:
        abort(403)

    db.session.delete(comentario)
    db.session.commit()

    flash(f"El comentario ID #{id} se elimino exitosamente!", "success")
    return redirect(url_for("reportes.ver_reporte", id=reporte_id))
