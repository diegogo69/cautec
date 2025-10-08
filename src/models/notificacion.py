from src.utils.db import db
from sqlalchemy.sql import func


class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False)  # e.g. 'nuevo_reporte', 'cambio_estado', 'nuevo_comentario'
    mensaje = db.Column(db.String(320), nullable=False)
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())
    leido = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    reporte_id = db.Column(db.Integer, db.ForeignKey("reportes.id"), nullable=True)

    usuario = db.relationship("Usuario", backref=db.backref("notificaciones", lazy="dynamic"))
    reporte = db.relationship("Reporte", backref=db.backref("notificaciones", lazy="dynamic"))

    def marcar_leido(self):
        self.leido = True

    def __repr__(self):
        return f"Notificacion('{self.tipo}', usuario_id={self.usuario_id}, reporte_id={self.reporte_id})"