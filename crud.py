def executar_sql(conn, sql, params=None, fetch=True):
    cursor = None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        if fetch and sql.strip().upper().startswith('SELECT'):
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        else:
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            return rows_affected
    except Exception as e:
        if cursor:
            cursor.close()
        conn.rollback()
        print(f"Erro SQL: {e}")
        return None

# Operações SELECT
def select_listar_pessoas(conn):
    sql = """
        SELECT id, nome_razao_social, email 
        FROM pessoa 
        ORDER BY nome_razao_social
    """
    return executar_sql(conn, sql)

def select_buscar_pessoa_nome(conn, nome):
    sql = """
        SELECT id, nome_razao_social, email 
        FROM pessoa 
        WHERE nome_razao_social ILIKE %s
        ORDER BY nome_razao_social
    """
    return executar_sql(conn, sql, (f'%{nome}%',))

def select_listar_usuarios(conn):
    sql = """
        SELECT u.id, u.nome, u.login, p.nome as perfil, u.ativo
        FROM usuario u, perfil_acesso p
        WHERE u.id_perfil = p.id
        ORDER BY u.nome
    """
    return executar_sql(conn, sql)

def select_listar_atendimentos(conn):
    sql = """
        SELECT a.id, a.data_atendimento, a.hora_atendimento, 
               p.nome_razao_social, u.nome, a.observacao
        FROM atendimento a, pessoa p, usuario u
        WHERE a.id_pessoa = p.id
          AND a.id_usuario = u.id
        ORDER BY a.data_atendimento DESC, a.hora_atendimento DESC
    """
    return executar_sql(conn, sql)

def select_buscar_atendimento_data(conn, data):
    sql = """
        SELECT a.id, a.data_atendimento, a.hora_atendimento, 
               p.nome_razao_social, u.nome, a.observacao
        FROM atendimento a, pessoa p, usuario u
        WHERE a.id_pessoa = p.id
          AND a.id_usuario = u.id
          AND a.data_atendimento = %s
        ORDER BY a.hora_atendimento
    """
    return executar_sql(conn, sql, (data,))

# Operações INSERT
def insert_pessoa(conn, nome, email):
    sql = """
        INSERT INTO pessoa (nome_razao_social, email) 
        VALUES (%s, %s)
    """
    return executar_sql(conn, sql, (nome, email), fetch=False)

def insert_usuario(conn, nome, login, senha, perfil_id):
    sql = """
        INSERT INTO usuario (nome, login, senha, id_perfil) 
        VALUES (%s, %s, %s, %s)
    """
    return executar_sql(conn, sql, (nome, login, senha, perfil_id), fetch=False)

def insert_atendimento(conn, data, hora, observacao, id_pessoa, id_usuario):
    sql = """
        INSERT INTO atendimento 
        (data_atendimento, hora_atendimento, observacao, id_pessoa, id_usuario) 
        VALUES (%s, %s, %s, %s, %s)
    """
    return executar_sql(conn, sql, (data, hora, observacao, id_pessoa, id_usuario), fetch=False)

# Operações UPDATE
def update_pessoa(conn, id_pessoa, novo_nome, novo_email):
    updates = []
    params = []
    if novo_nome:
        updates.append("nome_razao_social = %s")
        params.append(novo_nome)
    if novo_email:
        if novo_email.lower() == "none":
            updates.append("email = NULL")
        else:
            updates.append("email = %s")
            params.append(novo_email)
    
    if not updates:
        return 0
    
    params.append(id_pessoa)
    sql = f"UPDATE pessoa SET {', '.join(updates)} WHERE id = %s"
    return executar_sql(conn, sql, params, fetch=False)

def update_usuario(conn, id_usuario, novo_nome, novo_login, ativo):
    updates = []
    params = []
    if novo_nome:
        updates.append("nome = %s")
        params.append(novo_nome)
    if novo_login:
        updates.append("login = %s")
        params.append(novo_login)
    if ativo is not None:
        updates.append("ativo = %s")
        params.append(ativo)
    
    if not updates:
        return 0
    
    params.append(id_usuario)
    sql = f"UPDATE usuario SET {', '.join(updates)} WHERE id = %s"
    return executar_sql(conn, sql, params, fetch=False)

# Operações DELETE
def delete_pessoa(conn, id_pessoa):
    sql = "DELETE FROM pessoa WHERE id = %s"
    return executar_sql(conn, sql, (id_pessoa,), fetch=False)

def delete_usuario(conn, id_usuario):
    sql = "DELETE FROM usuario WHERE id = %s"
    return executar_sql(conn, sql, (id_usuario,), fetch=False)

# Funções auxiliares
def listar_perfis(conn):
    sql = "SELECT id, nome FROM perfil_acesso ORDER BY id"
    return executar_sql(conn, sql)

def listar_tipos_atendimento(conn):
    sql = "SELECT id, descricao FROM tipo_atendimento ORDER BY descricao"
    return executar_sql(conn, sql)

def listar_pessoas_simples(conn):
    sql = "SELECT id, nome_razao_social FROM pessoa ORDER BY nome_razao_social"
    return executar_sql(conn, sql)

def listar_usuarios_ativos(conn):
    sql = "SELECT id, nome FROM usuario WHERE ativo = true ORDER BY nome"
    return executar_sql(conn, sql)

def verificar_dependencias_pessoa(conn, id_pessoa):
    sql = """
        SELECT 'atendimento', COUNT(*) 
        FROM atendimento 
        WHERE id_pessoa = %s
        UNION ALL
        SELECT 'solicitacao', COUNT(*) 
        FROM solicitacao 
        WHERE id_pessoa = %s
    """
    return executar_sql(conn, sql, (id_pessoa, id_pessoa))

def verificar_dependencias_usuario(conn, id_usuario):
    sql = """
        SELECT 'atendimento', COUNT(*) 
        FROM atendimento 
        WHERE id_usuario = %s
        UNION ALL
        SELECT 'solicitacao', COUNT(*) 
        FROM solicitacao 
        WHERE id_usuario = %s
    """
    return executar_sql(conn, sql, (id_usuario, id_usuario))

def select_listar_solicitacoes(conn):
    sql = """
        SELECT s.id, s.data_solicitacao, p.nome_razao_social, 
               ts.descricao, st.descricao
        FROM solicitacao s, pessoa p, tipo_solicitacao ts, status st
        WHERE s.id_pessoa = p.id
          AND s.id_tipo_solicitacao = ts.id
          AND s.id_status = st.id
        ORDER BY s.data_solicitacao DESC
    """
    return executar_sql(conn, sql)

def select_detalhes_solicitacao(conn, id_solicitacao):
    sql = """
        SELECT s.id, s.data_solicitacao, p.nome_razao_social, p.email,
               ts.descricao, st.descricao, u.nome, s.descricao, s.observacao
        FROM solicitacao s, pessoa p, tipo_solicitacao ts, status st, usuario u
        WHERE s.id_pessoa = p.id
          AND s.id_tipo_solicitacao = ts.id
          AND s.id_status = st.id
          AND s.id_usuario = u.id
          AND s.id = %s
    """
    return executar_sql(conn, sql, (id_solicitacao,))

def listar_status_disponiveis(conn):
    sql = "SELECT id, descricao FROM status ORDER BY id"
    return executar_sql(conn, sql)

def update_status_solicitacao(conn, id_solicitacao, novo_status_id):
    sql = "UPDATE solicitacao SET id_status = %s WHERE id = %s"
    return executar_sql(conn, sql, (novo_status_id, id_solicitacao), fetch=False)