import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT')  # Definindo a porta padrão como 3306
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    
    # Configurações do JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Configurações do MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = os.getenv("MONGO_PORT")