from http import HTTPStatus
import json
from flask import Blueprint, Response
from flask import request, jsonify
from werkzeug.security import check_password_hash
from ..utils import conversion_result_login, db, generate_hashed_password

user_api = Blueprint('users', __name__)

@user_api.route('', methods=['POST'])
def create():
    data = request.get_json()
    hashed_password = generate_hashed_password( data["password"] )
    # Obtenir une connexion à la base de données
    db.reconnect()
    cursor = db.cursor()
    
    ''' Check login '''
    query = "SELECT nom FROM chef_zone WHERE login = %s"
    params = (data["login"],)
    cursor.execute(query, params)
    res = cursor.fetchone()
    
    if res is not None:
        return jsonify({
            "success": True,
            "message": "ce login est indisponible."
        })
        
    ''' New user '''
    query = "INSERT INTO chef_zone (LOGIN, NOM, PRENOMS, TYPEUTILISATEUR, DEPARTEMENT, TYPEDELEGUE, USER_ACTIF, IP_SIEGE, EMAIL_USER, TEL_USER, DOUBLE_AUTH, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (data["login"], data["nom"],data["prenom"], data["type_user"], data["department"], data["type_delegue"], data["user_actif"], data["ip_siege"], data["email_user"], data["tel_user"], 0, hashed_password)
    cursor.execute(query, params)
    db.commit()
    
    ''' Fermer le curseur et la connexion '''
    cursor.close()
    db.close()
    return jsonify({
        "success": True,
        "message": "Opération effectuée avec succès"
    })
    
    
@user_api.route('login', methods=['POST'])
def auth():  # sourcery skip: use-named-expression
    data = request.get_json()
    db.reconnect()
    cursor = db.cursor()

    ''' get infos user '''
    query = "SELECT LOGIN, password, NOM, PRENOMS, DEPARTEMENT, EMAIL_USER, TEL_USER, id  FROM  chef_zone WHERE login = %s"
    params = (data["login"],)
    cursor.execute(query, params)
    result = cursor.fetchone()
    
    if result is None:
        return jsonify({
            "success": False,
            "message": "Le login ou mot de passe est incorrect."
        })
    
    if not check_password_hash(result[1], data["password"]):
        return jsonify({
            "success": False,
            "message": "Le login ou mot de passe est incorrect."
        })

    data = conversion_result_login(result)
    return jsonify({
        "success": True,
        "results": data
    })
    
    
