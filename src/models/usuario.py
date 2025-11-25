import os
from src.utils.db import db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

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

    # 

    def get_reset_token(self):
        s = Serializer(os.getenv('SECRET_KEY', 'clave_por_defecto'))
        return s.dumps({'user_id': self.id})#.decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY', 'clave_por_defecto'))
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)
    
    def __repr__(self):
        return f"Usuario('{self.usuario}')"