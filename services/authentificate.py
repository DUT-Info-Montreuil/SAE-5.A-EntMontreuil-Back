import psycopg2
import connect_pg
from flask import  jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from services.users import UsersFonction
from config import SECRETE_KEY
class AuthentificateService:
    
    def __init__(self):
        pass
    
    def authentification(self, data) :
        valid_data = ['username', 'password']
        for field in valid_data :
            if field not in data:
                return jsonify({"error" : f"data need to contains {field}"}) , 400
            if not field :
                return jsonify({"error" : f"{field} is empty"}) , 400
        password = data.get('password')
        username = data.get('username')
        if not UsersFonction.field_exists('username' , username) :
            return jsonify({"error" : "username or password incorrect"}) , 400
        
        user = AuthentificateFonction.get_user_by_username(username)
        password_in_db = user[2]
        
        password = password.encode('utf-8') 
        password_in_db = password_in_db.encode('utf-8')
        result = bcrypt.checkpw(password, password_in_db) 
        if not result :
            return jsonify({"error" : "username or password incorrect"}) , 400
        else :
            token = AuthentificateFonction.generate_token(username)
            return jsonify({"message" : f"{username} are connected", "token" : token }) , 200
        #username : oudssi
        #mdp : aldp~o8xUwa8

        
class AuthentificateFonction:
    
    

    def generate_token(username):
        # Créez un payload contenant des informations utiles (par exemple, l'ID de l'utilisateur)
        user = AuthentificateFonction.get_user_by_username(username)
        role = AuthentificateFonction.get_role_id_by_name(user[6])
        payload = {
            'id' : user[0],
            'username': username,
            'isAdmin' : user[7],
            'role' : role,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Définissez une expiration pour le token (1 heure dans cet exemple)
        }
        # Générez le token en utilisant la clé secrète
        token = jwt.encode(payload, SECRETE_KEY, algorithm='HS256')
        return token
    
    def get_user_by_username(username):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM ent.users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_role_id_by_name(role_id):
        conn = connect_pg.connect()# Établir une connexion à la base de données
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ent.roles WHERE id = %s", (role_id,))
        role_name = cursor.fetchone()
        conn.close()  # Fermer la connexion à la base de données
        return role_name[0]  # Renvoie l'ID du rôle s'il existe