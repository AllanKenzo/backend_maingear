from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['SECRET_KEY'] = Config.SECRET_KEY
jwt = JWTManager(app)

# Registrar Blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)