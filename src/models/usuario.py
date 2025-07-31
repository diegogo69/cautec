from src.utils.db import db
from flask_login import UserMixin

# UserMixin provides certain attributes and methods User model expects:
# isAuthenticated, isActive, isAnonymous, get_id()

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100)) #, unique=True)
    telefono = db.Column(db.String(50))
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id')) #, nullable=False)


    def __repr__(self):
        return f"Usuario('{self.usuario}')"