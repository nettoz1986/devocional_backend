from flask import Blueprint, request, jsonify
import models

bp = Blueprint("api", __name__)

@bp.route("/daily", methods=["GET"])
def daily():
    row = models.get_daily()
    if not row:
        return jsonify({"ok": False, "error": "sem dados"})
    return jsonify({"ok": True, "versiculo": row})

@bp.route("/fatores", methods=["GET"])
def fatores():
    return jsonify({"ok": True, "fatores": models.get_fatores()})

@bp.route("/refinadores", methods=["GET"])
def refinadores():
    fator = request.args.get("fator")
    return jsonify({"ok": True, "refinadores": models.get_refinadores(fator)})

@bp.route("/search", methods=["POST"])
def search():
    data = request.get_json(force=True)
    fator = data.get("fator")
    refinadores = data.get("refinadores", [])
    results = models.search(fator, refinadores)
    return jsonify({"ok": True, "results": results})

@bp.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json(force=True)
    models.save_feedback(
        data.get("versiculo_id"),
        data.get("fator"),
        data.get("refinadores", []),
        data.get("nota", 0),
        data.get("comentario", "")
    )
    return jsonify({"ok": True, "msg": "feedback salvo"})
