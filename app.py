from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from auth import auth_bp

app = Flask(__name__)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
jwt = JWTManager(app)

# Registrar Blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)