from pymongo import MongoClient

# Conectar ao MongoDB (substitua pela URL correta se necessário)
client = MongoClient("mongodb://localhost:27017/")

# Testar a conexão
try:
    # Verifica se o servidor MongoDB está disponível
    client.admin.command('ping')
    print("Conexão bem-sucedida com o MongoDB")
except Exception as e:
    print(f"Erro na conexão com o MongoDB: {e}")
    
# Conectar ao banco de dados
db = client["relatoriosdb"]

# Defina o documento que você quer inserir
documento = {
    "reportId": "REL1234567890",
    "dateTime": "2024-11-29 10:00:00",
    "email": "example@example.com",
    "detalhes": "Detalhes do relatório",
    "manutencao": "Sim",
    "especificacao": "Especificações do relatório"
}

# Inserir o documento na coleção
colecao = db["relatorios"]
result = colecao.insert_one(documento)

# Verificar se o documento foi inserido com sucesso
if result.acknowledged:
    print(f"Documento inserido com sucesso! ID: {result.inserted_id}")
else:
    print("Falha ao inserir o documento.")

# Verificar se a coleção existe
collections = db.list_collection_names()
if "nome_da_colecao" in collections:
    print("Coleção já existe")
else:
    print("Coleção não encontrada. Ela será criada ao adicionar um documento.")