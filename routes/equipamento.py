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

@equipamento_bp.route('/atualizar_extintor', methods=['PUT'])
def atualizar_extintor(patrimonio):
    dados = request.json

    # Validação de campos obrigatórios
    campos_obrigatorios = [
        'tipo', 'capacidade', 'codigo_fabricante', 'data_fabricacao',
        'data_validade', 'ultima_recarga', 'proxima_inspecao', 'status',
        'id_localizacao', 'qr_code'
    ]
    
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            return jsonify({"erro": f"O campo {campo} é obrigatório."}), 400

    dados['patrimonio'] = patrimonio

    sucesso, mensagem = Extintor.atualizar(dados)
    if sucesso:
        return jsonify({"mensagem": mensagem}), 200
    else:
        return jsonify({"erro": mensagem}), 500
    
@equipamento_bp.route('/deletar_extintor', methods=['DELETE'])
def deletar_extintor(patrimonio):
    sucesso, mensagem = Extintor.deletar(patrimonio)
    if sucesso:
        return jsonify({"mensagem": mensagem}), 200
    else:
        return jsonify({"erro": mensagem}), 500