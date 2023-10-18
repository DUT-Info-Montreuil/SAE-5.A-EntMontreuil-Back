# IMPORT
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import psycopg2
from contextlib import closing
from config import config
import connect_pg
import hashlib
import re

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

############  USERS/GET ################
@app.route('/users/get', methods=['GET','POST'])
def get_users():
    """ Return all users in JSON format """
    query = "select * from ent.users order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_user_statement(row))
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

############  TEACHERS/GET ################
@app.route('/teachers/get', methods=['GET','POST'])
def get_teachers():
    """ Return all teachers in JSON format """
    query = "select * from ent.teachers order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_teacher_statement(row))
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

############  USERS/ADD ################
@app.route('/users/add', methods=['POST'])
def add_users():
    try:
        jsonObject = request.json
        # Assurez-vous que "datas" est présent dans l'objet JSON
        if "datas" not in jsonObject:
            return jsonify({"message": "Missing 'datas' field in JSON"})
        data = jsonObject["datas"]
        password = data.get("password") 
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        # Verifie si tous les attributs sont présents sauf type
        if not username:
            return jsonify({"message": "Missing 'username' field in JSON"})
        if not first_name:
            return jsonify({"message": "Missing 'first_name' field in JSON"})
        if not last_name:
            return jsonify({"message": "Missing 'last_name' field in JSON"})
        if not email:
            return jsonify({"message": "Missing 'email' field in JSON"})
        if not password:
            return jsonify({"message": "Missing 'password' field in JSON"})
        # Verification username plus de 4 caracteres
        if len(username) < 4:
            return jsonify({"message": "Username need to have minimum 4 characters"})
        # Verifiez si le nom d'utilisateur est deja utilise
        if username_exists(username):
            return jsonify({"message": "Username already in use"})
        if not is_valid_email(email):
            return jsonify({"message": "Invalid email format"})
        # Verifiez le mot de passe
        if len(password) < 12 : # plus de 12 caracteres
            return jsonify({"message": "password need to contains minimum 12 characters"})
        if not re.search(r'[A-Z]', password) : # au moins 1 majuscule
            return jsonify({"message": "Password need to contains minimum 1 capital"})
        if not re.search(r'[a-z]', password) : # au moins une minuscule
            return jsonify({"message": "Password need to contains minimum 1 minuscule"})
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) :  # Au moins un caractere special
            return jsonify({"message": "Password need to contains minimum 1 special characters"})
        if not re.search(r'[1-9]', password) : # au moins 1 chiffre
            return jsonify({"message": "Password need to contains minimum 1 number"})
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        # Creez la liste de colonnes et de valeurs
        columns = list(data.keys())
        values = list(data.values())
        values[columns.index("password")] = hashed_password
        # Etablissez la connexion a la base de donnees
        conn = connect_pg.connect()
        cursor = conn.cursor()
        # Créez la requête SQL parametree
        query = f"INSERT INTO ent.users ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
        # Executez la requête SQL avec les valeurs
        cursor.execute(query, values)
        # Recuperez l'identifiant de l'utilisateur insere
        row = cursor.fetchone()
        # Validez la transaction et fermez la connexion
        conn.commit()
        conn.close()
        return jsonify({"message": "User added", "id": row[0]})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)})

def username_exists(username):
    # Fonction pour verifier si le nom d'utilisateur existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def is_valid_email(email):
    # Utilisez une expression reguliere pour verifier la syntaxe de l'e-mail
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)


############  USER STATEMENT ################
def get_user_statement(row) :
    """ User array statement """
    return {
        'id':row[0],
        'username':row[1],
        'password':row[2],
        'type':row[3],
        'last_name':row[4],
        'first_name':row[5],
        'email':row[6]
    }

############  TEACHER STATEMENT ################
def get_teacher_statement(row):
    """ Teacher array statement """
    teacher_statement = {
        'id': row[0],
        'initial': row[1],
        'desktop': row[2],
        'timetable_manager': row[3],
    }
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ent.users WHERE id = %s", (row[4],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user :
        user_statement = get_user_statement(user)  
        teacher_statement['user'] = user_statement
    else :
        teacher_statement['user'] = None  # L'utilisateur n'existe pas
    return teacher_statement


if __name__ == "__main__":
    # read server parameters
    params = config('config.ini', 'server')
    # Launch Flask server
    app.run(debug=params['debug'], host=params['host'], port=params['port'])