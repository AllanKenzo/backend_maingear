from pymongo import MongoClient
from config import Config

def get_mongo_connection():
    """Conexão com o banco de dados MongoDB."""
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]
    return db