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
            return jsonify({"username" : username, "id_user" : user[0] , "first_name" : user[4] , "last_name" : user[3] , "role" : user[9] }) , 200
        #utilisateur test : 
        #username : oudssi
        #mdp : aldp~o8xUwa8

        
class AuthentificateFonction:
    
    def get_user_by_username(username):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select * from ent.users inner join ent.roles on users.id_role = roles.id WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
