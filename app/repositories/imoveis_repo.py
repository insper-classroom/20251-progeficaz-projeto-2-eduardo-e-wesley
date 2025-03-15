from database.connection import connect_db

def fetch_all_imoveis():
    conn = connect_db()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
        FROM imoveis
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_imovel(payload):
    conn = connect_db()
    if not conn:
        return None
    cursor = conn.cursor()
    sql = """
        INSERT INTO imoveis
        (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        payload['logradouro'],
        payload['tipo_logradouro'],
        payload['bairro'],
        payload['cidade'],
        payload['cep'],
        payload['tipo'],
        payload['valor'],
        payload['data_aquisicao']
    )
    cursor.execute(sql, valores)
    conn.commit()
    if cursor.rowcount == 1:
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return novo_id
    cursor.close()
    conn.close()
    return None


def fetch_imovel_by_id(imovel_id):
    conn = connect_db()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
        FROM imoveis
        WHERE id = %s
    """, (imovel_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def update_imovel(payload, imovel_id):
    conn = connect_db()
    if not conn:
        return 0
    cursor = conn.cursor()
    sql = """
        UPDATE imoveis
        SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, cep=%s,
            tipo=%s, valor=%s, data_aquisicao=%s
        WHERE id=%s
    """
    valores = (
        payload['logradouro'],
        payload['tipo_logradouro'],
        payload['bairro'],
        payload['cidade'],
        payload['cep'],
        payload['tipo'],
        payload['valor'],
        payload['data_aquisicao'],
        imovel_id
    )
    cursor.execute(sql, valores)
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected


def delete_imovel(imovel_id):
    conn = connect_db()
    if not conn:
        return 0
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id=%s", (imovel_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected


def fetch_imoveis_by_param(param, value):
    allowed_cols = ['tipo', 'cidade']
    if param not in allowed_cols:
        raise ValueError(f"Coluna '{param}' não é permitida.")

    conn = connect_db()
    if not conn:
        return []
    cursor = conn.cursor()
    sql = f"""
        SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
        FROM imoveis
        WHERE {param} = %s
    """
    cursor.execute(sql, (value,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
