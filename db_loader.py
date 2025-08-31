import pandas as pd
import sqlite3

EXCEL_FILE = r"C:\PROJETOS\# Devocional\devocional_backend\Base de dados.xlsx"
DB_FILE = "base.db"

def load_excel_to_sqlite():
    # lê o excel
    df = pd.read_excel(EXCEL_FILE)

    # Normaliza colunas (ajuste conforme seu Excel)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # conecta no sqlite
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("versiculos", conn, if_exists="replace", index=False)

    # cria tabela de feedback se não existir
    conn.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        versiculo_id INTEGER,
        fator TEXT,
        refinadores TEXT,
        nota INTEGER,
        comentario TEXT
    )
    """)
    conn.commit()
    conn.close()
    print(f"[ok] Banco criado em {DB_FILE} com {len(df)} versículos.")

if __name__ == "__main__":
    load_excel_to_sqlite()
