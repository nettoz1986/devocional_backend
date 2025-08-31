import sqlite3

DB_FILE = "base.db"

def get_conn():
    return sqlite3.connect(DB_FILE)

def get_daily():
    """Seleciona um salmo ou provérbio aleatório"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM versiculos 
        WHERE livro IN ('Salmos', 'Provérbios')
        ORDER BY RANDOM() LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    return row

def get_fatores():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT fator FROM versiculos")
    fatores = [r[0] for r in cur.fetchall() if r[0]]
    conn.close()
    return fatores

def get_refinadores(fator):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT refinador FROM versiculos WHERE fator=?", (fator,))
    refinadores = [r[0] for r in cur.fetchall() if r[0]]
    conn.close()
    return refinadores

def search(fator, refinadores):
    conn = get_conn()
    cur = conn.cursor()
    query = """
        SELECT * FROM versiculos
        WHERE fator = ?
    """
    params = [fator]

    if refinadores:
        cond = " OR ".join(["refinador LIKE ?"] * len(refinadores))
        query += f" AND ({cond})"
        params += [f"%{r}%" for r in refinadores]

    query += " ORDER BY score DESC LIMIT 5"
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()
    return results

def save_feedback(versiculo_id, fator, refinadores, nota, comentario):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO feedback (versiculo_id, fator, refinadores, nota, comentario)
        VALUES (?, ?, ?, ?, ?)
    """, (versiculo_id, fator, ",".join(refinadores), nota, comentario))
    conn.commit()
    conn.close()
