from flask import Blueprint, request, jsonify, send_file, Response
from services.report_service import insert_report_to_db, inserir_relatorio_por_status, inserir_relatorio_por_validade, inserir_relatorio_por_localizacao, devolver_todos_relatorios, baixar_pdf
from services.pdf_service import decode_base64_to_pdf,encode_pdf_to_base64


relatorio_bp = Blueprint("relatorio", __name__)

@relatorio_bp.route('/upload', methods=['POST'])
def upload_relatorio():
    """Endpoint para fazer upload de um relatório PDF"""
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Arquivo não especificado"}), 400

    # Metadados básicos do relatório
    metadata = {
        "id_relatorio": request.form.get("id_relatorio"),
        "tipo_relatorio": request.form.get("tipo_relatorio"),
        "descricao": request.form.get("descricao"),
        "data_geracao": request.form.get("data_geracao"),
        "periodo": {
            "inicio": request.form.get("periodo_inicio"),
            "fim": request.form.get("periodo_fim")
        },
        "arquivo_nome": file.filename,
        "metadados": {
            "total_extintores": int(request.form.get("total_extintores", 0))
        }
    }

    # Salvar o relatório no banco de dados
    try:
        file_path = f"./temp/{file.filename}"
        file.save(file_path)  # Salvar temporariamente o arquivo
        insert_report_to_db(file_path, metadata)
        return jsonify({"message": "Relatório salvo com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Precisa de um botão para fazer o relatório e um botão para baixar o relatório
@relatorio_bp.route('/relatorio_status', methods=['GET'])
def fazer_relatorio_por_status(status):
    """Endpoint para gerar um relatório de extintores por status"""
    try:
        relatorio = inserir_relatorio_por_status(status)
        if not relatorio:
            return jsonify({"error": "Nenhum extintor encontrado para esse status"}), 404
        return jsonify({"message": "Relatório gerado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Possivelmente para cada um dos tipos de relatórios
@relatorio_bp.route('/relatorio_validade', methods=['GET'])
def fazer_relatorio_por_validade(data_validade):
    """Endpoint para gerar um relatório de extintores por data de validade"""
    try:
        relatorio = inserir_relatorio_por_validade(data_validade)
        if not relatorio:
            return jsonify({"error": "Nenhum extintor encontrado para essa data de validade"}), 404
        return jsonify({"message": "Relatório gerado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@relatorio_bp.route('/relatorio_localizacao', methods=['GET'])
def fazer_relatorio_por_localizacao(id_localizacao):
    """Endpoint para gerar um relatório de extintores por localização"""
    try:
        relatorio = inserir_relatorio_por_localizacao(id_localizacao)
        if not relatorio:
            return jsonify({"error": "Nenhum extintor encontrado para essa localização"}), 404
        return jsonify({"message": "Relatório gerado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Para aparecer na tela de relatórios, ainda a determinar limite de relatorios
@relatorio_bp.route('/buscar_todos_relatorios', methods=['GET'])
def buscar_todos_relatorios():
    """Endpoint para buscar todos os relatórios salvos no banco de dados"""
    try:
        relatorios = devolver_todos_relatorios()
        return jsonify(relatorios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#
@relatorio_bp.route('/baixar_relatorio/<id>', methods=['POST'])#na url é passado o id do relatório, lembrar 
def baixar_relatorio(id):
    print(f"Received ID: {id}")
    """Retorna um link do PDF decodificado pelo ID"""
    try:
        # Busca o documento no banco de dados
        pdf_data = baixar_pdf(id)

        # Retorna como resposta binária
        return Response(pdf_data, mimetype='application/pdf', headers={
            "Content-Disposition": f"inline; filename=relatorio_{id}.pdf"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

