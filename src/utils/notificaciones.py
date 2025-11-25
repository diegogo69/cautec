from src import db
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario
from src.utils.auth import mail
from flask_mail import Message
# helpers for creating notifications

def crear_notificacion(usuario_id: int, tipo: str, mensaje: str, reporte_id: int = None):
    n = Notificacion(usuario_id=usuario_id, tipo=tipo, mensaje=mensaje, reporte_id=reporte_id)
    db.session.add(n)
    db.session.commit()

    # Enviar correo de notificación
    usuario = Usuario.query.get(usuario_id)
    
    try:
        enviar_correo_notificacion(usuario)
    except Exception as e:
        print(f"No se pudo enviar el correo de notificación. Error {e}")

    return n


def obtener_no_leidas(usuario_id: int, limit: int = 10):
    return (
        Notificacion.query.filter_by(usuario_id=usuario_id, leido=False)
        .order_by(Notificacion.fecha.desc())
        .limit(limit)
        .all()
    )


def marcar_todas_leidas(usuario_id: int):
    nots = Notificacion.query.filter_by(usuario_id=usuario_id, leido=False).all()
    for n in nots:
        n.leido = True
    db.session.commit()
    return len(nots)

# Enviar mensaje de correo electrónico para notificaciones importantes
def enviar_correo_notificacion(usuario):
    msg = Message('Nueva notificacion CAUTEC',
                    sender='soportenurr@gmail.com',
                    recipients=[usuario.email])
    msg.body = f'''Hola!
Tienes una nueva notificación en el sistema CAUTEC. Por favor, inicia sesión para revisarla.
'''
    mail.send(msg)
