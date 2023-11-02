from flask import request, jsonify, Blueprint
import json
import connect_pg
import csv
import os
from users import *

students_bp = Blueprint('students', __name__)


#--------------------------------------------------ROUTE--------------------------------------------------#

############ STUDENTS/GET ############
@students_bp.route('/students', methods=['GET','POST'])
def get_students():
    """ Return all students in JSON format """
    query = "select * from ent.students order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_student_statement(row))
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

############ STUDENTS/GET/<int:id_students> ############
@students_bp.route('/students/<int:id_students>', methods=['GET', 'POST'])
def get_teacher(id_students):
    try:
        if student_id_exists(id_students) :
            return jsonify({"error": f"id_students : '{id_students}' not exists"}) , 400
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM ent.students WHERE id = %s"
        cursor.execute(query, (id_students,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return get_student_statement(row)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

############ STUDENTS/ADD ############
@students_bp.route('/students/add', methods=['POST'])
def add_students():
    try:
        jsonObject = request.json
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400
        data = jsonObject["datas"]
        if "user" not in data:
            return jsonify({"error": "Missing 'user' field in JSON"}) , 400
        user_data = data["user"]
        user_data["type"] = "etudiant"
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status
        else :
            #on recupere le password de l'utilisateur ajouter pour  savoir quel est sont mdp si il est generer aleatoirement
            password = user_response.json.get("password")
            if "apprentice" in data :
                apprentice = data["apprentice"]
            else :
                apprentice = False
            user_id = user_response.json.get("id")
            student_data = {
                "apprentice": apprentice,
                "id_User" : user_id
            }
            columns = list(student_data.keys())
            values = list(student_data.values())
            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            # Créez la requête SQL parametree
            query = f"INSERT INTO ent.students ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
            # Executez la requête SQL avec les valeurs
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
            return jsonify({"message": "Student added, save the password for this user it will not be recoverable", "id": row[0], "username" : user_data["username"] , "password" : password }) , 200  
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400

############ STUDENTS/REMOVE/<int:id_student> ############
@students_bp.route('/students/remove/<int:id_student>', methods=['DELETE'])
def delete_students(id_student):
    try:
        if student_id_exists(id_student) :
            return jsonify({"error": f"id_student : '{id_student}' not exists"}) , 400
        id_user = get_user_id_with_id_student(id_student)
        if user_id_exists(id_user) :
            return jsonify({"error": f"id_user : '{id_user}' not exists"}) , 400

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.students WHERE id = %s"
        cursor.execute(query, (id_student,))
        conn.commit()
        conn.close()
        user_response, http_status = remove_users(id_user)
        return jsonify({"message": "Student deleted", "id": id_student}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

############ STUDENTS/UPDATE/<int:id_student> ############
@students_bp.route('/students/update/<int:id_student>', methods=['PATCH'])
def update_students(id_student):
    try:
        jsonObject = request.json
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400 
        student_data = jsonObject["datas"]
        if "user" in student_data:
            user_data = student_data["user"]
            del student_data["user"]
            if not user_data:
                return jsonify({"error": "Empty 'user' field in JSON"}), 400
            id_user = get_user_id_with_id_student(id_student)
            user_response, http_status = update_users(user_data, id_user)
            if http_status != 200 :
                return user_response, http_status
        if student_data :
            conn = connect_pg.connect()
            cursor = conn.cursor()
            update_clause = ", ".join([f"{key} = %s" for key in student_data.keys()])
            values = list(student_data.values())
            values.append(id_student)  # Ajoutez l'ID de l'enseignant à la fin pour identifier l'enregistrement a mettre a jour
            query = f"UPDATE ent.students SET {update_clause} WHERE id = %s"
            cursor.execute(query, values)
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
        return jsonify({"message": "Student update", "id": id_student}) , 200 
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400

############ STUDENTS/ADD/<path:csv_path> ############
@students_bp.route('/students/add/<path:csv_path>', methods=['GET','POST'])
def csv_add_students(csv_path):
    try:   
        
        #test avec : C:/Users/xxp90/Documents/BUT INFO/SAE EDT/csv_students.csv
        if not is_csv_file(csv_path) :
            return jsonify({"error": "Your file is not csv file "}) , 400

        response, http_status = verification_csv_file(csv_path) 
        if http_status != 200 :
            return response, http_status

        passwords = []
        data = {
            "user" : None
        }
        parts = csv_path.split("/") 
        filename = parts[-1]


        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data["user"] = row
                add_student_response, http_status = add_students(data)
                if http_status != 200 :
                    return add_student_response, http_status
                json_with_password = add_student_response.json.get("json")
                passwords.append(json_with_password)
        return jsonify({"csv file": f"All students add from {filename}" ,"message" : "Saved all passwords for all user they will not be recoverable", "password" : passwords} ) , 200 
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400


#--------------------------------------------------FONCTION--------------------------------------------------#

############  VERIFICATION STUDENT ID EXIST PAS ################
def student_id_exists(id):
    # Fonction pour verifier si l'id d'un etudiant n'existe pas dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.students WHERE id = %s", (id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

############  RECUPERATION USER ID SELON ID_STUDENT  ################
def get_user_id_with_id_student(id_student):
    # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_student
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id_User FROM ent.students WHERE id = %s", (id_student,))
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

############ STUDENTS/ADD ############
def add_students(student_data):
    try:
        if "user" not in student_data:
            return jsonify({"error": "Missing 'user' field in JSON"}) , 400
        user_data = student_data["user"]
        user_data["type"] = "etudiant"
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status 
        else :
            #on recupere le password de l'utilisateur ajouter pour  savoir quel est sont mdp si il est generer aleatoirement
            reponse_json = user_response.json
            password = reponse_json.get("password")
            if "apprentice" in student_data :
                apprentice = student_data["apprentice"]
                
            else :
                apprentice = False
            user_id = user_response.json.get("id")
            student_data = {
                "apprentice": apprentice,
                "id_User" : user_id
            }
            columns = list(student_data.keys())
            values = list(student_data.values())
            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            # Créez la requête SQL parametree
            query = f"INSERT INTO ent.students ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
            # Executez la requête SQL avec les valeurs
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
            json_response = {
                "password" : password,
                "username" : user_data["username"]
            }
            return jsonify({"message": "Student added","id" : row[0] ,  "json" : json_response}) , 200  
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400

############ VERIFICATION IS CSV FILE ############
def is_csv_file(filename):
    # Utilisez os.path.splitext pour obtenir l'extension du fichier
    file_extension = os.path.splitext(filename)[-1].lower()
    # Comparez l'extension avec ".csv" (en minuscules) pour vérifier s'il s'agit d'un fichier CSV
    return file_extension == ".csv"

############ VERIFICATION CSV VALIDE ############
def verification_csv_file(csv_path):
    response , http_status = find_duplicate_usernames(csv_path)
    if http_status != 200 :
        return response , http_status
        
    else : 
        return True

############ VERIFICATION USERNAME DANS LE CSV ############
def find_duplicate_usernames(csv_path):
    usernames = {}  # Utilisez un dictionnaire pour stocker les lignes où chaque nom d'utilisateur apparaît

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line_number = 1  # Initialisez le numéro de ligne à 1

        for row in reader:
            username = row.get('username')
            if username in usernames:
                # Si le nom d'utilisateur existe déjà dans le dictionnaire, ajoutez la ligne actuelle
                usernames[username].append(line_number)
            else:
                # Sinon, initialisez une nouvelle entrée dans le dictionnaire avec le numéro de ligne actuel
                usernames[username] = [line_number]
            
            line_number += 1  # Incrémentez le numéro de ligne pour la ligne suivante
    
    # Recherchez les noms d'utilisateur en double et les lignes correspondantes
    duplicates = {username: lines for username, lines in usernames.items() if len(lines) > 1}
    
    if duplicates:
        duplicate_usernames = []
        for username, lines in duplicates.items():
            duplicate_usernames.append(f"duplicates username : {username} at lines : {' , '.join(map(str, lines))}")
        return jsonify({"message": "Your csv file contains duplicate usernames", "duplicate usernames": duplicate_usernames }) , 400
    else:
        return jsonify({"message": "Your csv dont contains duplicate usernames"}) , 200