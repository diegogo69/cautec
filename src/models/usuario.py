from src.utils.db import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))

    departamento = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)


    def __repr__(self):
        return f"Usuario('{self.usuario}')"