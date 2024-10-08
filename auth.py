from flask import Blueprint, request, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from models import register_user, get_user_by_email

auth_bp = Blueprint('auth', __name__)

# Rota para registro de novo usuário
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verificar se o e-mail já está registrado
    if get_user_by_email(data['email']):
        return jsonify({'message': 'Usuário já registrado'}), 400

    # Registrar o usuário
    register_user(data['email'], data['password'])

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

# Rota para login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Buscar o usuário no banco de dados
    user = get_user_by_email(email)

    # Validar se o usuário existe e se a senha está correta
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    # Criar o token JWT
    access_token = create_access_token(identity=user['id'])

    return jsonify({'token': access_token}), 200