from datetime import datetime
from flask import jsonify, send_file
from config import Config
from models import Extintor
from services.pdf_service import encode_pdf_to_base64, decode_base64_to_pdf
from services.db_service import get_mongo_connection
from routes.equipamento import equipamento_bp
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os


load_dotenv()

client, collection = get_mongo_connection()


def montar_pdf(pdf_file, extintores):
    for extintor in extintores:
        pdf_file.write(f"Patrimônio: {extintor['Patrimonio']}\n")
        pdf_file.write(f"Tipo: {extintor['Tipo']}\n")
        pdf_file.write(f"Capacidade: {extintor['Capacidade']}\n")
        pdf_file.write(f"Status: {extintor['Status']}\n")
        pdf_file.write(f"Localização: {extintor['ID_Localizacao']}\n")
        pdf_file.write(f"Data de Fabricação: {extintor['Data_Fabricacao']}\n")
        pdf_file.write(f"Data de Validade: {extintor['Data_Validade']}\n")
        pdf_file.write(f"Última Recarga: {extintor['Ultima_Recarga']}\n")
        pdf_file.write(f"Próxima Inspeção: {extintor['Proxima_Inspecao']}\n")
        pdf_file.write(f"Código do Fabricante: {extintor['Codigo_Fabricante']}\n\n")

def insert_report_to_db(metadata):
    client = None
    try:
        document = {
            "tipo_relatorio": metadata.get("tipo_relatorio"),
            "descricao": metadata.get("descricao"),
            "data_geracao": metadata.get("data_geracao"),
            "arquivo": {
                "nome": metadata.get("arquivo", {}).get("nome"),
                "conteudo": metadata.get("arquivo", {}).get("conteudo")
            },
            "metadados": metadata.get("metadados")
        }
        
        # Insere o documento no banco de dados
        result = collection.insert_one(document)
        
        # Retorna o ID do documento inserido
        return str(result.inserted_id)
    except Exception as e:
        print(f"Erro ao inserir relatório no MongoDB: {e}")
        return None
    finally:
        # Garante que a conexão será fechada
        if client:
            client.close()

def serialize_document(doc):
    """Converte documentos do MongoDB para um formato serializável"""
    return {
        key: (str(value) if isinstance(value, ObjectId) else value)
        for key, value in doc.items()
    }

def devolver_todos_relatorios():
    client = None
    try:
        relatorios = collection.find()
        # Serializa os documentos
        return [serialize_document(relatorio) for relatorio in relatorios]
    except Exception as e:
        print(f"Erro ao buscar relatórios no MongoDB: {e}")
        return None
    finally:
        if client:
            client.close()

def inserir_relatorio_por_localizacao(id_localizacao):
    """Gera um relatório de extintores por localização."""
    # Buscar extintores por localização
    extintores = Extintor.buscar_por_localizacao(id_localizacao)
    if not extintores:
        return False, "Nenhum extintor encontrado para essa localização"

    # Gerar conteúdo do relatório
    create_temp_folder()
    pdf_path = f"./temp/relatorio_{id_localizacao}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf"
    with open(pdf_path, "w") as pdf_file:
        pdf_file.write("Relatório de Extintores por Localização\n\n")
        montar_pdf(pdf_file, extintores)
            

    # Metadados do relatório
    # Codificar o PDF em base64
    base64_pdf = encode_pdf_to_base64(pdf_path)

    metadata = {
        "id_relatorio": f"relatorio_{id_localizacao}",
        "tipo_relatorio": "localização",
        "descricao": "Relatório de extintores por localização",
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": {
            "nome": f"relatorio_{id_localizacao}.pdf",
            "conteudo": base64_pdf
            },
        "metadados": {
            "total_extintores": len(extintores)
        }
    }

    insert_report_to_db(metadata)
    # Salvar o relatório no banco de dados

def inserir_relatorio_por_validade():
    """Gera um relatório de extintores por data de validade."""
    # Buscar extintores por data de validade
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    extintores = Extintor.buscar_todos_perto_validade()
    if not extintores:
        return False, "Nenhum extintor encontrado para essa data de validade"

    # Gerar conteúdo do relatório
    create_temp_folder()
    pdf_path = f"./temp/relatorio_{data}.pdf"
    with open(pdf_path, "w") as pdf_file:
        pdf_file.write("Relatório de Extintores por Data de Validade\n\n")
        montar_pdf(pdf_file, extintores)

    # Metadados do relatório
    # Codificar o PDF em base64
    base64_pdf = encode_pdf_to_base64(pdf_path)

    metadata = {
        "id_relatorio": f"relatorio_{data}",
        "tipo_relatorio": "validade",
        "descricao": "Relatório de extintores por data de validade",
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": {
            "nome": f"relatorio_{data}.pdf",
            "conteudo": base64_pdf
            },
        "metadados": {
            "total_extintores": len(extintores)
        }
    }

    # Salvar o relatório no banco de dados
    return insert_report_to_db(metadata)

def inserir_relatorio_por_status(status):
    """Gera um relatório de extintores por status."""
    # Buscar extintores por status
    extintores = Extintor.buscar_por_status(status)
    if not extintores:
        return False, "Nenhum extintor encontrado para esse status"

    # Gerar conteúdo do relatório
    create_temp_folder()
    pdf_path = f"./temp/relatorio_{status}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf"
    with open(pdf_path, "w") as pdf_file:
        pdf_file.write("Relatório de Extintores por Status\n\n")
        montar_pdf(pdf_file, extintores)

    # Metadados do relatório
    # Codificar o PDF em base64
    base64_pdf = encode_pdf_to_base64(pdf_path)

    metadata = {
        "id_relatorio": f"relatorio_{status}",
        "tipo_relatorio": "status",
        "descricao": "Relatório de extintores por status",
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": {
            "nome": f"relatorio_{status}.pdf",
            "conteudo": base64_pdf
            },
        "metadados": {
            "total_extintores": len(extintores)
        }
    }

    # Salvar o relatório no banco de dados
    return insert_report_to_db(metadata)

def baixar_pdf(id):
    print(f"Received ID: {id}")  # Log the received ID
    try:
        documento = collection.find_one({'_id': ObjectId(id)})
        if not documento:
            return id, 404

        # Decode the PDF file
        pdf_data = decode_base64_to_pdf(documento['arquivo']['conteudo'])
        return pdf_data
    except Exception as e:
        print(f"Erro ao buscar relatório no MongoDB: {e}")
        return None
    finally:
        if client:
            client.close()
            
def create_temp_folder():
    temp_folder_path = os.path.join(os.path.dirname(__file__), '..', 'temp')
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
    return temp_folder_path
