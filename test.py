from pymongo import MongoClient

# Substitua pela sua URL de conexão
client = MongoClient("mongodb://localhost:27017")
db = client["relatoriosdb"]  # Substitua pelo nome do seu banco
collection = db["relatorios"]  # Substitua pelo nome da sua coleção

# Busca todos os documentos e exibe as chaves e valores
for doc in collection.find():
    print("Documento:")
    for key, value in doc.items():
        print(f"  {key}: {value}")
    print("-" * 40)  # Separador entre documentos

client.close()
