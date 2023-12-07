import psycopg2
import connect_pg
from flask import  jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from services.users import UsersFonction

class AuthentificateService:
    
    def __init__(self):
        pass
    
    def authentification(self, data) :
        password = data.get('password')
        username = data.get('username')
        if not UsersFonction.field_exists('username' , username) :
            return jsonify({"error" : "Identifiant ou mot de passe incorrect."}) , 400
        
        user = AuthentificateFonction.get_user_by_username(username)
        password_in_db = user[1]
        
        password = password.encode('utf-8') 
        password_in_db = password_in_db.encode('utf-8')
        result = bcrypt.checkpw(password, password_in_db) 
        if not result :
            return jsonify({"error" : "Identifiant ou mot de passe incorrect."}) , 400
        else :
            return jsonify({"username" : username, "id_user" : user[0] , "first_name" : user[2] , "last_name" : user[3] , "role" : user[4] , "isAdmin" : user[5] , "isTTManager" : user[6]} ) , 200
        #utilisateur test : 
        #username : oudssi
        #mdp : aldp~o8xUwa8

        
class AuthentificateFonction:
    
    def get_user_by_username(username):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select u.id, u.password, u.first_name, u.last_name, r.name, u.isAdmin, u.isTTManager from ent.users u inner join ent.roles r on u.id_role = r.id WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
