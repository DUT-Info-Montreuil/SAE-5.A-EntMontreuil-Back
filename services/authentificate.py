import psycopg2
import connect_pg
from flask import  jsonify
import bcrypt
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
            return jsonify({"error" : f"{username} not exist"}) , 400
        
        password_in_db = AuthentificateFonction.get_password_with_username(username)
        
        
        
        
        
        
        
class AuthentificateFonction:
    def get_password_with_username(username) :
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT password FROM ent.users WHERE username = %s"
        cursor.execute(query, (username,))
        password = cursor.fetchone()[0]
        conn.close()
        return password
