from src.utils.db import db

# Fallas de los dispositivos
# Tipo de falla: general, específica de dispositivo (teclado, monitor, etc)
# Predeterminada: indica si es una falla predeterminada de la aplicación o añadida por un usuario 
# Descripcion: descripción de la falla
class Falla_Dispositivo(db.Model):
    __tablename__ = "fallas_dispositivos" 

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    predeterminada = db.Column(db.Boolean(False), default=False, nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)

    # usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id'), nullable=False)


    def __repr__(self):
        return f"Falla('{self.tipo}', '{self.predeterminada}', '{self.descripcion}')"
