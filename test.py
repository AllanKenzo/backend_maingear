from services.report_service import insert_report_to_db, inserir_relatorio_por_status, inserir_relatorio_por_localizacao, inserir_relatorio_por_validade
from flask import Blueprint, request, jsonify, send_file

relatorio_bp = Blueprint("relatorio", __name__)

inserir_relatorio_por_status("ativo")
