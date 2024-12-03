import os
from datetime import datetime
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import jsonify
from bson import ObjectId
from models import Extintor
from services.pdf_service import decode_base64_to_pdf, encode_pdf_to_base64
from routes.equipamento import equipamento_bp
from dotenv import load_dotenv
from services.db_service import get_mongo_connection

load_dotenv()

client, collection = get_mongo_connection()


def create_temp_folder():
    """Create a temporary folder if it doesn't exist."""
    temp_folder = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

def delete_temp_files():
    """Delete all files in the temp folder."""
    temp_folder = os.path.join(os.getcwd(), 'temp')
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Erro ao deletar arquivo {file_path}: {e}")

def montar_pdf(pdf_path, extintores):
    """Montar o conteúdo do PDF."""
    with open(pdf_path, 'wb') as pdf_file:
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, "Relatório de Extintores por Localização")
        y = 700
        for extintor in extintores:
            print(extintor)
            c.drawString(100, y, f"Patrimônio: {extintor['Patrimonio']}")
            y -= 20
            c.drawString(100, y, f"Tipo: {extintor['Tipo']}")
            y -= 20
            c.drawString(100, y, f"Capacidade: {extintor['Capacidade']}")
            y -= 20
            c.drawString(100, y, f"Código Fabricante: {extintor['Codigo_Fabricante']}")
            y -= 20
            c.drawString(100, y, f"Data Fabricação: {extintor['Data_Fabricacao']}")
            y -= 20
            c.drawString(100, y, f"Data Validade: {extintor['Data_Validade']}")
            y -= 20
            c.drawString(100, y, f"Última Recarga: {extintor['Ultima_Recarga']}")
            y -= 20
            c.drawString(100, y, f"Próxima Inspeção: {extintor['Proxima_Inspecao']}")
            y -= 20
            c.drawString(100, y, f"Status: {extintor['Status']}")
            y -= 20
            c.drawString(100, y, f"ID Localização: {extintor['ID_Localizacao']}")
            y -= 20
            if 'qr_code' in extintor:
                c.drawString(100, y, f"QR Code: {extintor['QR_Code']}")
                y -= 20
            y -= 20  # Add extra space between extintores
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
    pdf_path = f"./temp/relatorio_{id_localizacao}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    montar_pdf(pdf_path, extintores)

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

    # Salvar o relatório no banco de dados
    insert_report_to_db(metadata)
    delete_temp_files()

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

    montar_pdf(pdf_path, extintores)

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
    delete_temp_files
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

    montar_pdf(pdf_path, extintores)

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
    delete_temp_files
    return insert_report_to_db(metadata)

def baixar_pdf(id):
    print(f"Received ID: {id}")  # Log the received ID
    client = None
    try:
        documento = collection.find_one({'_id': ObjectId(id)})
        if not documento:
            return jsonify({'error': 'Relatório não encontrado'}), 404

        # Decode the PDF file
        pdf_data = decode_base64_to_pdf(documento['arquivo']['conteudo'])

        # Save the PDF file in the Downloads folder
        downloads_folder = get_downloads_folder()
        pdf_path = os.path.join(downloads_folder, f'relatorio_{id}.pdf')
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)

        return jsonify({'message': f'PDF salvo em {pdf_path}'}), 200
    except Exception as e:
        print(f"Erro ao buscar relatório no MongoDB: {e}")
        return jsonify({'error': 'Erro ao buscar relatório'}), 500
    finally:
        if client:
            client.close()
            
def get_downloads_folder():
    """Get the path to the Downloads folder based on the operating system."""
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
