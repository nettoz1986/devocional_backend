from flask import Blueprint, jsonify
import pandas as pd

bp = Blueprint("factors", __name__)

# Carrega a base de dados uma vez
df = pd.read_excel("Base de dados.xlsx")

@bp.route("/factor/<nome>")
def get_factor(nome):
    # Filtra pelo fator_label
    filtrado = df[df["fator_label"].str.contains(nome, case=False, na=False)]

    if filtrado.empty:
        return jsonify({"error": f"Fator '{nome}' não encontrado"}), 404

    resultados = []
    for _, row in filtrado.iterrows():
        resultados.append({
            "livro": row["livro"],
            "capitulo": int(row["capitulo"]),
            "versiculo": int(row["versiculo"]),
            "fator": row["fator_label"],
            "score": row["fator_score"],
            "refinadores": [row["Refinador 1"], row["Refinador 2"], row["Refinador 3"]],
            "texto": row.get("texto", "")
        })

    return jsonify(resultados)
