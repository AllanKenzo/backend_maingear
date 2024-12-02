from db import get_db_connection
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import mysql.connector

class Extintor:
    def __init__(self, patrimonio, tipo, capacidade, codigo_fabricante, data_fabricacao,
                 data_validade, ultima_recarga, proxima_inspecao, status,
                 id_localizacao, qr_code, observacoes=None):
        self.patrimonio = patrimonio
        self.tipo = tipo
        self.capacidade = capacidade
        self.codigo_fabricante = codigo_fabricante
        self.data_fabricacao = data_fabricacao
        self.data_validade = data_validade
        self.ultima_recarga = ultima_recarga
        self.proxima_inspecao = proxima_inspecao
        self.status = status
        self.id_localizacao = id_localizacao
        self.qr_code = qr_code
        self.observacoes = observacoes

    @staticmethod
    def cadastrar(dados):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO Extintores (Patrimonio, Tipo, Capacidade, Codigo_Fabricante, Data_Fabricacao,
                                    Data_Validade, Ultima_Recarga, Proxima_Inspecao, Status,
                                    ID_Localizacao, QR_Code, Observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['patrimonio'], dados['tipo'], dados['capacidade'], dados['codigo_fabricante'],
            dados['data_fabricacao'], dados['data_validade'], dados['ultima_recarga'],
            dados['proxima_inspecao'], dados['status'], dados['id_localizacao'],
            dados.get('qr_code', None), dados.get('observacoes', None)
        )
        
        try:
            cursor.execute(sql, valores)
            conn.commit()
            return True, "Extintor cadastrado com sucesso."
        except mysql.connector.Error as err:
            return False, f"Erro ao cadastrar o extintor: {str(err)}"
        finally:
            cursor.close()
            conn.close()
        
            
    @staticmethod
    def atualizar(dados):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE Extintores
            SET Tipo = %s, Capacidade = %s, Codigo_Fabricante = %s, Data_Fabricacao = %s,
                Data_Validade = %s, Ultima_Recarga = %s, Proxima_Inspecao = %s, Status = %s,
                ID_Localizacao = %s, QR_Code = %s, Observacoes = %s
            WHERE Patrimonio = %s
        """
        valores = (
            dados['tipo'], dados['capacidade'], dados['codigo_fabricante'],
            dados['data_fabricacao'], dados['data_validade'], dados['ultima_recarga'],
            dados['proxima_inspecao'], dados['status'], dados['id_localizacao'],
            dados['qr_code'], dados.get('observacoes', ''), dados['patrimonio']
        )
        
        try:
            cursor.execute(sql, valores)
            conn.commit()
            return True, "Extintor atualizado com sucesso."
        except mysql.connector.Error as err:
            return False, f"Erro ao atualizar o extintor: {str(err)}"
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def deletar(patrimonio):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM Extintores WHERE Patrimonio = %s"
        
        try:
            cursor.execute(sql, (patrimonio,))
            conn.commit()
            return True, "Extintor deletado com sucesso."
        except mysql.connector.Error as err:
            return False, f"Erro ao deletar o extintor: {str(err)}"
        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def buscar_por_id(patrimonio):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM Extintores WHERE Patrimonio = %s"
        
        cursor.execute(sql, (patrimonio,))
        extintor = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return extintor
    
    @staticmethod
    def buscar_por_localizacao(id_localizacao):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM Extintores WHERE ID_Localizacao = %s"
        
        cursor.execute(sql, (id_localizacao,))
        extintores = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return extintores
    
    @staticmethod
    def buscar_por_validade(data_validade):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM Extintores WHERE Data_Validade = %s"
        
        cursor.execute(sql, (data_validade,))
        extintores = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return extintores
    
    @staticmethod
    def buscar_por_status(status):#lembrar de mandar uma string do status corretamente
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM Extintores WHERE Status = %s"
        
        cursor.execute(sql, (status,))
        extintores = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return extintores
    
    @staticmethod
    def buscar_todos_perto_validade():#para relatorios
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        data_atual = datetime.now().date()
        
        sql = """
            SELECT * 
            FROM Extintores 
            WHERE Data_Validade BETWEEN %s AND DATE_ADD(%s, INTERVAL 7 DAY)
        """
        
        cursor.execute(sql, (data_atual, data_atual))
        extintores = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return extintores
    
    @staticmethod
    def buscar_todos(): #Buscar todos os extintores
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM Extintores"
        
        try:
            cursor.execute(sql)
            extintores = cursor.fetchall()
            return extintores
        except mysql.connector.Error as err:
            print(f"Erro ao buscar extintores: {str(err)}")
            return []
        finally:
            cursor.close()
            conn.close()

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