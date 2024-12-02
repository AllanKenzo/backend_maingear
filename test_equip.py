from routes.relatorio import upload_relatorio
from flask import Flask

app = Flask(__name__)

metadata = {
    "tipo_relatorio": "mensal",
    "descricao": "Relatório mensal de extintores",
    "data_geracao": "2024-12-01",
    "arquivo": {
        "nome": "relatorio.pdf",
        "conteudo": "dGVzdCBjb250ZW50"  # This is an example base64 encoded string for "test content"
    },
    "metadados": {
        "total_extintores": 10
    }
}

with app.app_context():
    response = upload_relatorio(metadata)
    print(response)