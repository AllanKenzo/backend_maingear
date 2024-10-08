from db import get_db_connection
from flask_bcrypt import generate_password_hash, check_password_hash

# Função para registrar um novo usuário
def register_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Criptografar a senha
    hashed_password = generate_password_hash(password).decode('utf-8')

    query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    cursor.execute(query, (email, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()

# Função para buscar um usuário por e-mail
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user