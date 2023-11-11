from flask import jsonify, Blueprint
import connect_pg
import hashlib
import re
import random
import string
from modules.statements import *


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

############  USERS/GET/<int:id_user> ################
@users_bp.route('/users/<int:id_user>', methods=['GET','POST'])
def get_users_with_id(id_user):
    """ Return one user in JSON format """
    try :
        if not id_exists(id_user) :
            return jsonify({"error": f"id_user : '{id_user}' not exists"}) , 400
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select * from ent.users where id = %s"
        cursor.execute(query, (id_user,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return get_user_statement(row)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

#--------------------------------------------------FONCTION--------------------------------------------------#

############  USER UPDATE ################
def update_users(user_data, id_user):
    try:
        # Si le password est present
        if "password" in user_data :
            password = user_data["password"]
            # Verification du password
            user_response, http_status = is_valid_password(password)  
            if http_status != 200 :
                return user_response, http_status 
            else :
                # Hashage du password
                user_data["password"] = hashlib.md5(password.encode()).hexdigest() 
        # Si id est présent 
        if "id" in user_data :
            return jsonify({"error": "Unable to modify user id, remove id field"}) , 400
        # Si username est présent
        if "username" in user_data :
            username = user_data["username"]
            # Verification username existe deja
            if username_exists(username):
                return jsonify({"error": f"Username '{username}' already exists"}), 400
            # Verification username plus de 4 caracteres
            if len(username) < 4:
                return jsonify({"error": "Username need to have minimum 4 characters"}), 400
        # Si email est present
        if "email" in user_data :
            email = user_data["email"]
            # Verification email
            if not is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400
        # Si type est present
        if "type" in user_data :
            # Si type est bien = etudiant ou enseignant ou responsable_edt ou admin
            if user_data["type"] != "etudiant" and user_data["type"] != "enseignant" and user_data["type"] != "responsable_edt" and user_data["type"] != "admin" and user_data["type"] != "test" :
                return jsonify({"error": "Invalid type, the 4 types available are {etudiant - enseignant - responsable_edt - admin}"}), 400
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
        # Verification si id_user existe bien
        if not id_exists(id_user) :
            return jsonify({"error": f"User {id_user} not exist"}) , 400
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
        # Si le password est mentionner 
        if "password" in data and data["password"] :
            password = data["password"]
            # Verifiez le mot de passe
            user_response, http_status = is_valid_password(password) 
            if http_status != 200 :
                return user_response, http_status 
        # Si le password n'est pas mentionner il est generer aleatoirement
        else :   
            data["password"] = generate_password()
        password = data["password"]
         
        
        # Verifie si tous les attributs sont presents 
        if "username" not in data:
            return jsonify({"error": "Missing 'username' field in JSON"}), 400
        if "first_name" not in data:
            return jsonify({"error": "Missing 'first_name' field in JSON"}), 400
        if "last_name" not in data:
            return jsonify({"error": "Missing 'last_name' field in JSON"}), 400
        if "email" not in data:
            return jsonify({"error": "Missing 'email' field in JSON"}), 400
        if "type" not in data :
            return jsonify({"error": "Missing 'type' field in JSON"}), 400
        
        # Attribution des valeurs
        username = data["username"]
        email = data["email"] 
        first_name = data["first_name"] 
        last_name = data["last_name"]
        # Verification si id est deja utiliser
        if "id" in data :
            if id_exists(data["id"]) :
                return jsonify({"error": f"Id for user '{data.get('id')}' already exist"}), 400
        # Verifiez username taille > 4
        if len(username) < 4:
            return jsonify({"error": "Username need to have minimum 4 characters"}), 400
        # Verifiez si le nom d'utilisateur est deja utilise
        if username_exists(username):
            return jsonify({"error": f"Username '{username}' already exists"}), 400
        # Verification de la syntaxe de l'email
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        # Verification si le type est bien un type existant (etudiant, enseignant, responsable_edt, admin)
        if data["type"] != "etudiant" and data["type"] != "enseignant" and data["type"] != "responsable_edt" and data["type"] != "admin" and data["type"] != "test" :
            return jsonify({"error": "Invalid type, the 4 types available are {etudiant - enseignant - responsable_edt - admin}"}), 400
        # Hashage du password avec md5
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
        return jsonify({"message": "User added", "id": row[0] , "username" : username , "password" : password}) , 200 
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

############  VERIFICATION ID_USER EXIST ################
def id_exists(id_user):
    # Fonction pour verifier si l'id user existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE id = %s", (id_user,))
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

############  GENERATE PASSWORD ################
def generate_password():
    # Generate a password with at least one uppercase letter, one special character, two digits, and the rest lowercase letters
    length = 12
    uppercase_letter = random.choice(string.ascii_uppercase)
    special_character = random.choice(string.punctuation)
    digits = ''.join(random.choices(string.digits, k=2))
    lowercase_letters = ''.join(random.choices(string.ascii_lowercase, k=length-4))

    # Shuffle the characters to create the final password
    password_list = list(uppercase_letter + special_character + digits + lowercase_letters)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password