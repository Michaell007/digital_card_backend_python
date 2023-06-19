from http import HTTPStatus
import json
from flask import Blueprint, Response
from flask import request, jsonify
from ..utils import conversion_result_search, db

enrole_api = Blueprint('enroles', __name__)

@enrole_api.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    # Obtenir une connexion à la base de données
    db.reconnect()
    cursor = db.cursor()
    query = "SELECT NOMS_PERS, PRENOMS_PERS, LIEU_NAISS, DATE_NAISS, NUM_TEL, PROFESSION, NUM_IDENTITE, SEXE_P FROM persons WHERE NOMS_PERS = %s AND PRENOMS_PERS = %s AND NUM_IDENTITE = %s"
    params = (data["nom"], data["prenom"], data["cni"],)
    cursor.execute(query, params)

    # Récupérer les résultats de la requête
    results = cursor.fetchall()

    if cursor.rowcount == 0:
        return jsonify({
            "success": False,
            "message": "Cette personne ne figure pas dans la base de donnees."
        })

    
    data = conversion_result_search(results)
    # Fermer le curseur et la connexion
    cursor.close()
    db.close()
    return jsonify({
        "success": True,
        "results": data
    })
    
    