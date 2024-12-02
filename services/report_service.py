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
import base64
import os
from flask import Response
from reportlab.pdfgen import canvas

load_dotenv()

client, collection = get_mongo_connection()


def montar_pdf(pdf_path, extintores, titulo):
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 800, titulo)
    y_position = 750
    for extintor in extintores:
        c.drawString(100, y_position, f"Patrimônio: {extintor['Patrimonio']}")
        c.drawString(100, y_position - 20, f"Tipo: {extintor['Tipo']}")
        c.drawString(100, y_position - 40, f"Capacidade: {extintor['Capacidade']}")
        c.drawString(100, y_position - 60, f"Status: {extintor['Status']}")
        c.drawString(100, y_position - 80, f"Localização: {extintor['ID_Localizacao']}")
        y_position -= 120  # Ajusta a posição para evitar sobreposição
        if y_position < 100:  # Nova página se necessário
            c.showPage()
            y_position = 750
    c.save()



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
    extintores = Extintor.buscar_todos_perto_validade()
    if not extintores:
        return None

    pdf_path = os.path.join(create_temp_folder(), f"relatorio_validade_{datetime.now().strftime('%Y%m%d')}.pdf")
    montar_pdf(pdf_path, extintores, "Relatório de Extintores por Validade")

    base64_pdf = encode_pdf_to_base64(pdf_path)
    metadata = {
        "tipo_relatorio": "validade",
        "descricao": "Relatório de extintores com validade próxima",
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": {
            "nome": os.path.basename(pdf_path),
            "conteudo": base64_pdf
        },
        "metadados": {
            "total_extintores": len(extintores)
        }
    }

    return insert_report_to_db(metadata)


def inserir_relatorio_por_status(status):
    extintores = Extintor.buscar_por_status(status)
    if not extintores:
        return None

    pdf_path = os.path.join(create_temp_folder(), f"relatorio_status_{status}.pdf")
    montar_pdf(pdf_path, extintores, "Relatório de Extintores por Status")

    base64_pdf = encode_pdf_to_base64(pdf_path)
    metadata = {
        "tipo_relatorio": "status",
        "descricao": f"Relatório de extintores com status: {status}",
        "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "arquivo": {
            "nome": f"relatorio_status_{status}.pdf",
            "conteudo": base64_pdf
        },
        "metadados": {
            "total_extintores": len(extintores)
        }
    }

    return insert_report_to_db(metadata)


def baixar_pdf(id):
    try:
        documento = collection.find_one({'_id': ObjectId(id)})
        if not documento:
            return jsonify({'error': 'Relatório não encontrado'}), 404

        # Decode the PDF file
        pdf_data = base64.b64decode(documento['arquivo']['conteudo'])

        # Serve the PDF as a downloadable file
        return Response(
            pdf_data,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment;filename={documento["arquivo"]["nome"]}',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
    except Exception as e:
        print(f"Erro ao buscar relatório no MongoDB: {e}")
        return jsonify({'error': 'Erro ao buscar relatório'}), 500

            
def create_temp_folder():
    temp_folder_path = os.path.join(os.path.dirname(__file__), '..', 'temp')
    os.makedirs(temp_folder_path, exist_ok=True)
    return temp_folder_path

