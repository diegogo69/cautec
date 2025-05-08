from src.utils.db import db

class Departamento(db.Model):
    __tablename__ = "departamentos"

    id = db.Column(db.Integer, primary_key=True)
    torre = db.Column(db.String(2), nullable=False)
    piso = db.Column(db.String(2), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    nombre_coordinador = db.Column(db.String(100), nullable=False)
    linea_telefonica = db.Column(db.String(20))


    def __repr__(self):
        return f"Departamento('{self.nombre}')"