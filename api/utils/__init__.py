import mysql.connector as mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import random
import os

# os.getenv('HOSTNAME')

db = mysql.connect(user='root', password='', host='localhost', database='carte_digitale')

def generate_otp():
    random_digits = []
    for _ in range(4):
        digit = random.randint(0, 9)
        random_digits.append(str(digit))
    return ''.join(random_digits)

def conversion_result_search(results):
    data = []
    for row in results:
        row_dict = {
            'nom': row[0],
            'prenom': row[1],
            'lieu_naiss': row[2],
            'date_naiss': row[3],
            'phone': row[4],
            'profession': row[5],
            'cni': row[6],
            'sexe': row[7],
        }
        data.append(row_dict)
    return data

def conversion_result_login(result):
    # create a new token with the user id inside current_user = get_jwt_identity()
    access_token = create_access_token(identity=result[0])
    return {
        'id': result[7],
        'login': result[0],
        'nom': result[2],
        'prenom': result[3],
        'department': result[4],
        'email': result[5],
        'phone': result[6],
        'token': access_token
    }

# Fonction pour générer un mot de passe hashé
def generate_hashed_password(password):
    return generate_password_hash(password)

# Fonction pour vérifier un mot de passe
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
