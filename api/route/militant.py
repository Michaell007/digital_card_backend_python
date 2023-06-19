from http import HTTPStatus
from flask import Blueprint
from flask import request, jsonify
from ..utils import db, generate_otp
from datetime import datetime
import uuid

militant_api = Blueprint('militants', __name__)

@militant_api.route('', methods=['POST'])
def create():
    data = request.get_json()
    # Obtenir une connexion à la base de données
    db.reconnect()
    cursor = db.cursor()
    my_otp = generate_otp()
        
    # Check if device existe
    query = "SELECT code, militant_id FROM device WHERE code = %s"
    params = (data["qrcode"],)
    cursor.execute(query, params)
    results = cursor.fetchall() # Récupérer les résultats de la requête
    if cursor.rowcount > 0:
        return jsonify({
            "success": False,
            "message": "Ce device est déjà rattaché à un militant"
        })
        
    ''' Check if militant existe '''
    query = "SELECT nom FROM militant WHERE nom = %s AND prenom = %s AND cni = %s"
    params = (data["nom"], data["prenom"], data["cni"],)
    cursor.execute(query, params)
    res = cursor.fetchone()
    
    my_militant_id = 0
    if res is None:
        ''' New militant '''
        query = "INSERT INTO militant (uuid, phone, nom, prenom, date_naiss_long, lieu_naiss, profession, sexe, is_actived, otp, cni, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (str(uuid.uuid4()), data["phone"], data["nom"], data["prenom"], data["date_naiss_long"], data["lieu_naiss"], data["profession"], data["sexe"], False, my_otp, data["cni"], data["user_id"], datetime.now(), datetime.now(),)
        cursor.execute(query, params)
        my_militant_id = cursor.lastrowid
        db.commit()
    else:
        my_militant_id = res[0]
    
    ''' New Device '''
    query = "INSERT INTO device (code, militant_id, created_at, updated_at) VALUES (%s, %s, %s, %s)"
    params = (data["qrcode"], my_militant_id, datetime.now(), datetime.now(),)
    cursor.execute(query, params)
    db.commit()
    
    ''' Fermer le curseur et la connexion '''
    cursor.close()
    db.close()
    return jsonify({
        "success": True,
        "results": "Opération effectuée avec succès"
    })
    
    
@militant_api.route('/activation', methods=['POST'])
def actived_with_otp():
    data = request.get_json()
    db.reconnect()
    cursor = db.cursor()

    ''' get infos device '''
    query = "SELECT code, militant_id FROM device WHERE code = %s"
    params = (data["qrcode"],)
    cursor.execute(query, params)
    result = cursor.fetchone()

    if result is None:
        return jsonify({
            "success": False,
            "message": "Périphérique introuvable."
        })

    ''' Check if militant existe '''
    query = "SELECT nom, otp FROM militant WHERE id = %s"
    params = (result[1],)
    cursor.execute(query, params)
    res = cursor.fetchone()

    ''' Correct OTP ? '''
    if res[1] == data["otp"]:
        ''' Actived militant '''
        query = "UPDATE militant SET is_actived = %s, otp = %s WHERE id = %s"
        values = (True, "", result[1])
        cursor.execute(query, values)
        db.commit()
        # Fermer le curseur et la connexion
        cursor.close()
        db.close()
        return jsonify({
            "success": True,
            "message": "Activation réussie."
        })

    ''' Incorrect mot de passe '''
    return jsonify({
        "success": False,
        "message": "Mot de passe incorrect."
    })
