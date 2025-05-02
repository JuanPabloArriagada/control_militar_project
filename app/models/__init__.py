from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(9), unique=True, nullable=False)
    nombre = db.Column(db.String(15), nullable=False)
    apellido = db.Column(db.String(15), nullable=False)
    rango = db.Column(db.String(10))
    unidad = db.Column(db.String(10))
    tipo_persona = db.Column(db.String(20))  # Militar o Civil

    credencial = db.relationship("Credencial", backref="persona", uselist=False)
    accesos = db.relationship("Acceso", backref="persona", lazy=True)


class Credencial(db.Model):
    __tablename__ = 'credenciales'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(15))  # Activa / Inactiva
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_expiracion = db.Column(db.DateTime)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)


class Instalacion(db.Model):
    __tablename__ = 'instalaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15), nullable=False)
    zonas = db.relationship("Zona", backref="instalacion", lazy=True)


class Zona(db.Model):
    __tablename__ = 'zonas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15), nullable=False)
    nivel_seguridad = db.Column(db.String(15))  # SECRETO, RESTRINGIDO, PUBLICO
    instalacion_id = db.Column(db.Integer, db.ForeignKey('instalaciones.id'), nullable=False)
    accesos = db.relationship("Acceso", backref="zona", lazy=True)


class Acceso(db.Model):
    __tablename__ = 'accesos'
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    credencial_id = db.Column(db.Integer, db.ForeignKey('credenciales.id'), nullable=True)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=False)
    resultado = db.Column(db.String(10))  # Permitido o Denegado
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)


class UsuarioSistema(db.Model):
    __tablename__ = 'usuarios_sistema'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)  # Hasheada
    rol = db.Column(db.String(10))  # Admin, Seguridad

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    rol = db.Column(db.String(10), nullable=False)
    contraseña_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)