from src import db
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario

# helpers for creating notifications

def crear_notificacion(usuario_id: int, tipo: str, mensaje: str, reporte_id: int = None):
    n = Notificacion(usuario_id=usuario_id, tipo=tipo, mensaje=mensaje, reporte_id=reporte_id)
    db.session.add(n)
    db.session.commit()
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
