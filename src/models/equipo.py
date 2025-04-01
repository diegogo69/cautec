from src.utils.db import db

class Equipo(db.Model):
    __tablename__ = "equipos" 

    id = db.Column(db.Integer, primary_key=True)
    codigo_bienes = db.Column(db.String(50))
    tipo = db.Column(db.String(50), nullable=False)

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)


    def __repr__(self):
        return f"Equipo('{self.tipo}')"