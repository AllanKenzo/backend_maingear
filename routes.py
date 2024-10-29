from flask import Blueprint, request, jsonify
from models import Extintor

equipamento_bp = Blueprint('equipamento', __name__)

@equipamento_bp.route('/cadastrar_extintor', methods=['POST'])
def cadastrar_extintor():
    dados = request.json

    # Validação de campos obrigatórios
    campos_obrigatorios = [
        'patrimonio', 'tipo', 'capacidade', 'codigo_fabricante', 'data_fabricacao',
        'data_validade', 'ultima_recarga', 'proxima_inspecao', 'status',
        'id_localizacao', 'qr_code'
    ]
    
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            return jsonify({"erro": f"O campo {campo} é obrigatório."}), 400

    sucesso, mensagem = Extintor.cadastrar(dados)
    if sucesso:
        return jsonify({"mensagem": mensagem}), 201
    else:
        return jsonify({"erro": mensagem}), 500