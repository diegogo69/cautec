from flask import Blueprint, flash, render_template, request, redirect, url_for, abort, send_file, Response, make_response
from flask_login import current_user, login_required
from src.models.reporte import Reporte
from src.models.comentario import Comentario
from src.models.departamento import Departamento
from src.utils.departamentos import departamentos_json, AREAS_TIPOS, AREAS_TORRES, AREAS_PISOS
from src.utils.reportes import TIPOS_DISPOSITIVOS, FALLAS_DISPOSITIVOS, ESTADOS_REPORTE
from src.utils.pdfs import crear_pdf
from src import db
from sqlalchemy.sql import func
from datetime import datetime
from io import BytesIO

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
    texto_comentario = request.form["comentario"].strip()

    if not texto_comentario:
        return

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

path = {'path': None}

@reportes.route("/reporte/<int:id>/generar-nota-de-servicio", methods=["GET", "POST"])
@login_required
def nota_servicio(id):
    reporte = Reporte.query.get_or_404(id)
    departamento = Departamento.query.get_or_404(reporte.departamento_id)
    
    print(reportes.root_path) # /home/diego/repos/cautec/src/routes

    if request.method == "POST":
        # if reporte.usuario_id != current_user.id:
        #     abort(403)
        data = {}
        ruta_template = None
        ruta_css = None
        ruta_pdf = None

        reporte.accion = request.form['accion'].strip()
        reporte.diagnostico = request.form['diagnostico'].strip()

        data['fecha_emision'] = reporte.fecha_emision.strftime('%Y-%m-%d')
        data['nombre_solicitante'] = reporte.nombre_solicitante
        data['nombre_departamento'] = departamento.nombre
        data['ext_telefonica'] = departamento.linea_telefonica
        data['nombre_coordinador'] = request.form['coordinador']
        data['marca_disp'] = request.form['marca']
        data['serial_disp'] = request.form['serial']
        data['cod_bienes_disp'] = reporte.cod_bienes_dispositvo # Fix typo
        data['diagnostico'] = reporte.diagnostico
        # data['fecha_atencion'] = reporte.fecha_atencion.strftime('%Y-%m-%d')
        data['fecha_atencion'] = None
        # data['fecha_cierre'] = reporte.fecha_cierre.strftime('%Y-%m-%d')
        data['fecha_cierre'] = None
        data['accion'] = reporte.accion

        # print(reportes.root_path) # /home/diego/repos/cautec/src/routes
        # root_path = reportes.root_path.replace('src/routes', '') 
        root_path = reportes.root_path.removesuffix('src/routes') 
        ruta_template = f'{root_path}src/templates/pdfs/solicitud_de_servicio.html'
        ruta_css = f'{root_path}src/static/css/pdfs/solicitud_de_servicio.css'
        # ruta_css = url_for('static', filename='css/pdfs/solicitud_de_servicio.css')
        ruta_pdf = f'{root_path}prueba_pdf.pdf'
        ruta_pdf = None
        
        # instance_path = None
        # static_url_path = None

        pdf = crear_pdf(data, ruta_template, ruta_css, ruta_pdf)

        if pdf != True:
            # Usando send_file es necesario utilizar BytesIO sobre pdf
            # Mientras que al usar Response o make_response no es necesario
            # send_file me parece más directo y semántico, sin embargo necesita ese paso extra

            # Passing a file-like object requires that the file is
            # opened in binary mode, and is mostly useful when
            # building a file in memory with io.BytesIO

            # as_attachment (bool) – Indicate to a browser that it should offer to save the file instead of displaying it.
            pdf_buffer = BytesIO(pdf)

            print(type(pdf)) # <class 'bytes'>
            print(type(pdf_buffer)) # <class '_io.BytesIO'>
            
            # nombre_pdf = 'pdf_descarga_send_file.pdf'
            # return send_file(
            #     pdf,
            #     # pdf_buffer,
            #     download_name = nombre_pdf,
            #     as_attachment = True,
            # )

            # According to flask documentation: 
            # Do not set to a plain string or bytes, that will cause
            # sending the response to be very inefficient
            # as it will iterate one byte at a time.
            
            # Response: Quite often you don’t have to create this object yourself because make_response() will take care of that for you.
            # make_response: A response object is created with the bytes as the body
            # you will get a response object which you can use to attach headers
            # useful when need to attach additional headers

            # nombre_pdf = 'descarga_pdf_response.pdf'
            # headers = {
            #     'Content-Type': 'application/pdf',
            #     'Content-Disposition': f"attachment;filename={nombre_pdf}"
            # }

            # response = Response(pdf, headers=headers)
            # return response

            nombre_pdf = 'descarga_pdf_make_response.pdf'
            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = f"attachment;filename={nombre_pdf}"
            return response

        flash(f"El reporte ID #{id} se elimino exitosamente!", "success")
        return redirect(url_for("reportes.ver_reporte", id=id))
    
    elif request.method == "GET":
        reporte.falla = FALLAS_DISPOSITIVOS[int(reporte.falla_id)]
        reporte.tipo_dispositivo = TIPOS_DISPOSITIVOS[int(reporte.tipo_dispositivo_id)]

        return render_template(
            'reportes/crear-nota-servicio.html',
            reporte=reporte,
            departamento=departamento,
        )
