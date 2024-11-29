from flask import Blueprint, request, jsonify, send_file
from services.report_service import save_report_to_db, retrieve_report_from_db

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
        save_report_to_db(file_path, metadata)
        return jsonify({"message": "Relatório salvo com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@relatorio_bp.route('/download/<id_relatorio>', methods=['GET'])
def download_relatorio(id_relatorio):
    """Endpoint para baixar um relatório PDF"""
    try:
        output_path = f"./temp/{id_relatorio}.pdf"
        relatorio = retrieve_report_from_db(id_relatorio, output_path)
        if not relatorio:
            return jsonify({"error": "Relatório não encontrado"}), 404
        return send_file(output_path, as_attachment=True, download_name=relatorio["arquivo"]["nome"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500