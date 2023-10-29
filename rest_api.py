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
@app.route('/users', methods=['GET','POST'])
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
@app.route('/teachers', methods=['GET','POST'])
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

############  USERS ADD ################
def add_users(data):
    try:
        password = data["password"] 
        username = data["username"] 
        email = data["email"] 
        first_name = data["first_name"] 
        last_name = data["last_name"] 
        # Verifie si tous les attributs sont présents sauf type
        if not username:
            return jsonify({"error": "Missing 'username' field in JSON"}), 400
        if not first_name:
            return jsonify({"error": "Missing 'first_name' field in JSON"}), 400
        if not last_name:
            return jsonify({"error": "Missing 'last_name' field in JSON"}), 400
        if not email:
            return jsonify({"error": "Missing 'email' field in JSON"}), 400
        if not password:
            return jsonify({"error": "Missing 'password' field in JSON"}), 400
        # Verification username plus de 4 caracteres
        if len(username) < 4:
            return jsonify({"error": "Username need to have minimum 4 characters"}), 400
        # Verifiez si le nom d'utilisateur est deja utilise
        if username_exists(username):
            return jsonify({"error": f"Username '{username}' already exists"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        # Verifiez le mot de passe
        if len(password) < 12 : # plus de 12 caracteres
            return jsonify({"error": "password need to contains minimum 12 characters"}), 400
        if not re.search(r'[A-Z]', password) : # au moins 1 majuscule
            return jsonify({"error": "Password need to contains minimum 1 capital"}), 400
        if not re.search(r'[a-z]', password) : # au moins une minuscule
            return jsonify({"error": "Password need to contains minimum 1 minuscule"}), 400
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) :  # Au moins un caractere special
            return jsonify({"error": "Password need to contains minimum 1 special characters"}) , 400
        if not re.search(r'[1-9]', password) : # au moins 1 chiffre
            return jsonify({"error": "Password need to contains minimum 1 number"}) , 400
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
        return jsonify({"message": "User added", "id": row[0]}) , 200 
    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}) , 400

############ TEACHERS/ADD ############
@app.route('/teachers/add', methods=['POST'])
def add_teachers():
    try:
        jsonObject = request.json
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400
        data = jsonObject["datas"]
        if "user" not in data:
            return jsonify({"error": "Missing 'user' field in JSON"}) , 400
        user_data = data["user"]
        if initial_exists(data.get("initial")) :
            return jsonify({"error": f"Initial '{data.get('initial')}' already exists"}), 400
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status 
        else :
            user_id = user_response.json.get("id")
            teacher_data = {
                "desktop": data.get("desktop"),
                "initial": data.get("initial"),
                "timetable_manager": data.get("timetable_manager"),
                "id_User" : user_id
            }
            columns = list(teacher_data.keys())
            values = list(teacher_data.values())
            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            # Créez la requête SQL parametree
            query = f"INSERT INTO ent.teachers ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
            # Executez la requête SQL avec les valeurs
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
            return jsonify({"message": "Teachers added", "id": row[0]}) , 200  
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400

############  USERS REMOVE ################
def remove_user(id_user):
    try:
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.users WHERE id = %s"
        cursor.execute(query, (id_user,))
        conn.commit()
        conn.close()
        return jsonify({"message": "User deleted", "id": id_user}) , 200 
    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}) , 400

############ TEACHERS/REMOVE/<int:id_teacher> ############
@app.route('/teachers/remove/<int:id_teacher>', methods=['DELETE'])
def delete_teacher(id_teacher):
    try:
        if teacher_id_exists(id_teacher) :
            return jsonify({"error": f"id_teacher : '{id_teacher}' not exists"}) , 400
        id_user = get_user_id(id_teacher)
        if user_id_exists(id_user) :
            return jsonify({"error": f"id_user : '{id_user}' not exists"}) , 400

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.teachers WHERE id = %s"
        cursor.execute(query, (id_teacher,))
        conn.commit()
        conn.close()
        user_response, http_status = remove_user(id_user)
        return jsonify({"message": "Teacher deleted", "id": id_teacher}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

############ TEACHERS/GET/<int:id_teacher> ############
@app.route('/teachers/<int:id_teacher>', methods=['GET', 'POST'])
def get_teacher(id_teacher):
    try:
        if teacher_id_exists(id_teacher) :
            return jsonify({"error": f"id_teacher : '{id_teacher}' not exists"}) , 400
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM ent.teachers WHERE id = %s"
        cursor.execute(query, (id_teacher,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return get_teacher_statement(row)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400


############  VERIFICATION USERNAME EXIST ################
def username_exists(username):
    # Fonction pour verifier si le nom d'utilisateur existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION INITIAL EXIST ################
def initial_exists(initial):
    # Fonction pour verifier si le les initiales d'un enseignant existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.teachers WHERE initial = %s", (initial,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION TEACHER ID EXIST PAS ################
def teacher_id_exists(id):
    # Fonction pour verifier si l'id d'un enseignant n'existe pas dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.teachers WHERE id = %s", (id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

############  RECUPERATION USER ID  ################
def get_user_id(id):
    # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon un id d'un role
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id_User FROM ent.teachers WHERE id = %s", (id,))
    id_user = cursor.fetchone()[0]
    conn.close()
    return id_user

############  VERIFICATION USER ID EXIST PAS ################
def user_id_exists(id):
    # Fonction pour verifier si l'id d'un utilisateur n'existe pas dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE id = %s", (id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

############  VERIFICATION EMAIL SYNTAXE ################
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