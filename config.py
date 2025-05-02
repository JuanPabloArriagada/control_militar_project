import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-supersecreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usuario:clave@localhost:5432/nombre_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave-jwt-supersecreta')
