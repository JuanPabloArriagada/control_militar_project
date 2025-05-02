from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from redis import Redis
from dotenv import load_dotenv
import os

# ───── Extensiones ─────
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    db=0  # puedes usar otra base si quieres separar entornos
)

def create_app():
    # Cargar variables de entorno
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')  # Asegúrate de tener config.py

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registrar Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
