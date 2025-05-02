from flask import Blueprint, request, jsonify
from app.models import db, Persona, Credencial
from datetime import datetime
from app.models import Usuario
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

# ─────────────── PERSONAS ───────────────

@main.route('/personas', methods=['POST'])
def crear_persona():
    data = request.get_json()
    persona = Persona(
        rut=data['rut'],
        nombre=data['nombre'],
        apellido=data['apellido'],
        rango=data.get('rango'),
        unidad=data.get('unidad'),
        tipo_persona=data.get('tipo_persona', 'Militar')
    )
    db.session.add(persona)
    db.session.commit()
    return jsonify({'mensaje': 'Persona creada', 'id': persona.id}), 201


@main.route('/personas', methods=['GET'])
def listar_personas():
    personas = Persona.query.all()
    resultado = []
    for p in personas:
        resultado.append({
            'id': p.id,
            'rut': p.rut,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'tipo_persona': p.tipo_persona
        })
    return jsonify(resultado)


@main.route('/personas/<int:id>', methods=['DELETE'])
def eliminar_persona(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return jsonify({'mensaje': 'Persona eliminada'})


# ─────────────── CREDENCIALES ───────────────

@main.route('/credenciales', methods=['POST'])
def crear_credencial():
    data = request.get_json()
    credencial = Credencial(
        estado=data['estado'],
        fecha_emision=datetime.utcnow(),
        fecha_expiracion=datetime.strptime(data['fecha_expiracion'], '%Y-%m-%d'),
        persona_id=data['persona_id']
    )
    db.session.add(credencial)
    db.session.commit()
    return jsonify({'mensaje': 'Credencial creada', 'id': credencial.id}), 201


@main.route('/credenciales', methods=['GET'])
def listar_credenciales():
    credenciales = Credencial.query.all()
    resultado = []
    for c in credenciales:
        resultado.append({
            'id': c.id,
            'estado': c.estado,
            'persona_id': c.persona_id,
            'fecha_emision': c.fecha_emision.strftime('%Y-%m-%d'),
            'fecha_expiracion': c.fecha_expiracion.strftime('%Y-%m-%d')
        })
    return jsonify(resultado)

# ─────────────── REGISTRO ───────────────

@main.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    if Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first():
        return jsonify({'error': 'Usuario ya existe'}), 400

    nuevo_usuario = Usuario(
        nombre_usuario=data['nombre_usuario'],
        rol=data['rol']
    )
    nuevo_usuario.set_password(data['contraseña'])
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

# ─────────────── LOGIN ───────────────

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(nombre_usuario=data['nombre_usuario']).first()

    if usuario and usuario.check_password(data['contraseña']):
        token = create_access_token(identity={'id': usuario.id, 'rol': usuario.rol})
        return jsonify({'access_token': token}), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401