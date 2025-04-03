#from datetime import datetime
from src.utils.db import db
from sqlalchemy.sql import func # access SQL functions, like default creation date and time

class Reporte(db.Model):
    __tablename__ = "reportes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    categoria = db.Column(db.String(20))
    descripcion = db.Column(db.Text, nullable=False)
    diagnostico = db.Column(db.Text)
    accion = db.Column(db.Text)
    fecha_emision = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # fecha_emision = db.Column(db.DateTime, nullable=False, default=datetime.now)
    fecha_atencion = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    resuelto = db.Column(db.Boolean(False), default=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # equipo_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)

    def __repr__(self):
        return f"Reporte('{self.titulo}', '{self.fecha_emision}')"
