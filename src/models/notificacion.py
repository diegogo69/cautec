from src.utils.db import db
from sqlalchemy.sql import func

class Comentario(db.Model):
    __tablename__ = "comentarios" 

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.String(240), nullable=False)
    leido = db.Column(db.Boolean(False), default=False)
    db.Column(db.DateTime(timezone=True), server_default=func.now())

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False)


    def __repr__(self):
        return f"Comentario('{self.tipo}', '{self.mensaje}')"