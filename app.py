from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from auth import auth_bp
from routes.equipamento import equipamento_bp
from routes.relatorio import relatorio_bp  # Novo blueprint

app = Flask(__name__)
CORS(app)

# Configurações de JWT
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['SECRET_KEY'] = Config.SECRET_KEY
jwt = JWTManager(app)

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(equipamento_bp, url_prefix='/equipamento')
app.register_blueprint(relatorio_bp, url_prefix='/relatorio')  # Relatórios (MongoDB)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)