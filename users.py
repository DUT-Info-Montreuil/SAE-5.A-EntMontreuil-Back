from flask import jsonify, Blueprint
import connect_pg
import hashlib
import re
from statement import *


users_bp = Blueprint('users', __name__)


#--------------------------------------------------ROUTE--------------------------------------------------#

############  USERS/GET ################
@users_bp.route('/users', methods=['GET','POST'])
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

#--------------------------------------------------FONCTION--------------------------------------------------#

############  USER UPDATE ################
def update_users(user_data, id_user):
    try:
        if "password" in user_data :
            password = user_data["password"]
            user_response, http_status = is_valid_password(password)  
            if http_status != 200 :
                return user_response, http_status 
            else :
                user_data["password"] = hashlib.md5(password.encode()).hexdigest()  
        if "id" in user_data :
            return jsonify({"error": "Unable to modify user id, remove id field"}) , 400
        if "username" in user_data :
            username = user_data["username"]
            if username_exists(username):
                return jsonify({"error": f"Username '{username}' already exists"}), 400
            if len(username) < 4:
                return jsonify({"error": "Username need to have minimum 4 characters"}), 400
        if "email" in user_data :
            email = user_data["email"]
            if not is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400
        if "type" in user_data :
            if data["type"] != "étudiant" and data["type"] != "enseignant" and data["type"] != "responsable_edt" and data["type"] != "admin" and data["type"] != "test" :
                return jsonify({"error": "Invalid type, the 4 types available are {étudiant - enseignant - responsable_edt - admin}"}), 400
        # Etablissez la connexion a la base de donnees
        conn = connect_pg.connect()
        cursor = conn.cursor()
        update_clause = ", ".join([f"{key} = %s" for key in user_data.keys()])
        values = list(user_data.values())
        values.append(id_user)  # Ajoutez l'ID de l'enseignant à la fin pour identifier l'enregistrement a mettre a jour
        query = f"UPDATE ent.users SET {update_clause} WHERE id = %s"
        cursor.execute(query, values)
        # Validez la transaction et fermez la connexion
        conn.commit()
        conn.close()
        return jsonify({"message": "User update", "id": id_user}) , 200 
    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}) , 400

############  USERS REMOVE ################
def remove_users(id_user):
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
        if data["type"] != "étudiant" and data["type"] != "enseignant" and data["type"] != "responsable_edt" and data["type"] != "admin" and data["type"] != "test" :
            return jsonify({"error": "Invalid type, the 4 types available are {étudiant - enseignant - responsable_edt - admin}"}), 400
        # Verifiez le mot de passe
        user_response, http_status = is_valid_password(password)  
        if http_status != 200 :
            return user_response, http_status 
        else :
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
        row = cursor.fetchone()
        # Validez la transaction et fermez la connexion
        conn.commit()
        conn.close()
        return jsonify({"message": "User added", "id": row[0]}) , 200 
    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}) , 400

############  VERIFICATION USERNAME EXIST ################
def username_exists(username):
    # Fonction pour verifier si le nom d'utilisateur existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION EMAIL SYNTAXE ################
def is_valid_email(email):
    # Utilisez une expression reguliere pour verifier la syntaxe de l'e-mail
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

############  VERIFICATION PASSWORD ################
def is_valid_password(password):
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
    return True , 200


