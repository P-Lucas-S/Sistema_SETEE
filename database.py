import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            dbname="sistema_solicitacoes_db",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

def fechar_conexao(conn):
    if conn:
        conn.close()