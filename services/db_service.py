from pymongo import MongoClient
from config import Config

def get_mongo_connection():
    """Conexão com o banco de dados MongoDB."""
    try:
        uri = Config.MONGO_URI
        client = MongoClient(uri)
        db = client[Config.MONGO_DB_NAME]
        collection = db[Config.MONGO_COLLECTION_NAME]
        return client, collection
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}"); raise