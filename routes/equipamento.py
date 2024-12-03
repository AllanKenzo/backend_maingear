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
        'id_localizacao'
    ]
    
    campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados or not dados[campo]]
    if campos_faltantes:
        return jsonify({"erro": f"Os campos {', '.join(campos_faltantes)} são obrigatórios."}), 400

    sucesso, mensagem = Extintor.cadastrar(dados)
    if sucesso:
        return jsonify({"mensagem": mensagem}), 201
    else:
        return jsonify({"erro": mensagem}), 500

@equipamento_bp.route('/atualizar_extintor/<patrimonio>', methods=['PUT'])
def atualizar_extintor(patrimonio):
    dados = request.json

    campos_obrigatorios = [
        'tipo', 'capacidade', 'codigo_fabricante', 'data_fabricacao',
        'data_validade', 'ultima_recarga', 'proxima_inspecao', 'status',
        'id_localizacao', 'qr_code'
    ]
    
    for campo in campos_obrigatorios:
        if not dados.get(campo):
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
    
@equipamento_bp.route('/buscar_extintor_por_id', methods=['GET'])
def buscar_por_id(patrimonio):
    extintor = Extintor.buscar_por_id(patrimonio)
    if extintor:
        return jsonify(extintor), 200
    else:
        return jsonify({"erro": "Extintor não encontrado"}), 404

@equipamento_bp.route('/buscar_extintor_por_localizacao', methods=['GET'])
def buscar_por_localizacao():
    id_localizacao = request.args.get('id_localizacao')
    extintores = Extintor.buscar_por_localizacao(id_localizacao)
    return jsonify(extintores), 200

@equipamento_bp.route('/buscar_extintor_por_data_validade', methods=['GET'])
def buscar_por_data_validade():
    data_validade = request.args.get('data_validade')
    extintores = Extintor.buscar_por_validade(data_validade)
    return jsonify(extintores), 200

@equipamento_bp.route('/buscar_extintor_por_status', methods=['GET'])
def buscar_por_status():
    status = request.args.get('status')#lembrar de receber uma string com algum status válido
    extintores = Extintor.buscar_por_status(status)
    return jsonify(extintores), 200

@equipamento_bp.route('/buscar_extintores_perto_validade', methods=['GET'])
def buscar_perto_validade():
    extintores = Extintor.buscar_todos_perto_validade()
    return jsonify(extintores), 200

@equipamento_bp.route('/buscar_todos_extintores', methods=['GET'])
def buscar_todos():
    extintores = Extintor.buscar_todos()
    return jsonify(extintores), 200
