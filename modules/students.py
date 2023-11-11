from flask import request, jsonify, Blueprint
import json
import connect_pg
import csv
import os
from modules.users import *

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
        # Verification id student existe
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
        # Si il manque datas renvoie une erreur
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400
        data = jsonObject["datas"]
        # Si il manque user renvoie une erreur
        if "user" not in data:
            return jsonify({"error": "Missing 'user' field in JSON"}) , 400
        user_data = data["user"]
        # Si il manque ine renvoie une erreur
        if "ine" not in data : 
            return jsonify({"error": "Missing 'ine' field in JSON"}) , 400
        # Si il manque student_number renvoie une erreur
        if "student_number" not in data : 
            return jsonify({"error": "Missing 'student_number' field in JSON"}) , 400
        # INE deja existant
        if ine_exists(data["ine"]) :
            return jsonify({"error": f"Ine '{data.get('ine')}' already exist"}) , 400
        # student_number deja existant
        if student_number_exists(data["student_number"]) :
            return jsonify({"error": f"Student_number {data.get('student_number')} already exist"}) , 400
        # email deja existant
        if email_exists(user_data["email"]) :
            return jsonify({"error": f"email {data.get('email')} already exist"}) , 400
        user_data["type"] = "etudiant"
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status
        else :
            #on recupere le password de l'utilisateur ajouter pour savoir quel est sont mdp si il est generer aleatoirement
            password = user_response.json.get("password")
            # Si apprentice est mentionner sinon valeur par defaut a false
            if "apprentice" in data :
                apprentice = data["apprentice"]
            else :
                apprentice = False
            # Recuperation du user id
            user_id = user_response.json.get("id")
            # Creation du student data json
            student_data = {
                "apprentice": apprentice,
                "id_User" : user_id,
                "ine" : data["ine"],
                "student_number" : data["student_number"]
            }
            # Si id est present
            if "id" in data :
                # Verification si id existe deja
                if id_exists(data["id"]) :
                    return jsonify({"error": f"Id for student '{data.get('id')}' already exist"}), 400
                else :
                    student_data["id"] = data["id"]
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
        # Si id student n'existe pas
        if student_id_exists(id_student) :
            return jsonify({"error": f"id_student : '{id_student}' not exists"}) , 400
        
        id_user = get_user_id_with_id_student(id_student)

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
        # Si il manque datas renvoie une erreur
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400 
        student_data = jsonObject["datas"]
        if "id" in student_data :
            return jsonify({"error": "Unable to modify user id, remove id field"}), 400
        # Si il manque user renvoie une erreur
        if "user" in student_data:
            user_data = student_data["user"]
            # Supression du champ user pour garder les datas de l'etudiant
            del student_data["user"]
            # Si user data est vide
            if not user_data:
                return jsonify({"error": "Empty 'user' field in JSON"}), 400
            # Recuperation du user id
            id_user = get_user_id_with_id_student(id_student)
            user_response, http_status = update_users(user_data, id_user)
            # Si user update echoue
            if http_status != 200 :
                return user_response, http_status
        # Si student data n'est pas vide
        if student_data :
            conn = connect_pg.connect()
            cursor = conn.cursor()
            update_clause = ", ".join([f"{key} = %s" for key in student_data.keys()])
            values = list(student_data.values())
            values.append(id_student)  # Ajoutez l'ID de l'etudiant à la fin pour identifier l'enregistrement a mettre a jour
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
        # Verification fichier valide
        response, http_status = verification_csv_file(csv_path) 
        if http_status != 200 :
            return response, http_status
        # Tableau de tout les mdp des user ajouter
        passwords = []
        # Creation du json
        data = {
            "user" : None
        }
        # Recuperation du nom du fichier
        parts = csv_path.split("/") 
        filename = parts[-1]
        
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Pour chaque ligne ajoute l'etudiant
            for row in reader:
                data["user"] = row
                add_student_response, http_status = add_students(data)
                if http_status != 200 :
                    return add_student_response, http_status
                # Recuperation des password des students ajouter
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
        
        # INE deja existant
        if ine_exists(student_data["ine"]) :
            return jsonify({"error": f"Ine {student_data.get('ine')} already exist"}) , 400
        # student_number deja existant
        if student_number_exists(student_data["student_number"]) :
            return jsonify({"error": f"Student_number {student_data.get('student_number')} already exist"}) , 400
        # email deja existant
        if email_exists(user_data["email"]) :
            return jsonify({"error": f"email {student_data.get('email')} already exist"}) , 400
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



############ VERIFICATION CSV VALIDE ############
def verification_csv_file(csv_path):
    # verification duplicate usernames 
    response_duplicate_username , http_status_u = find_duplicate_usernames(csv_path)
    if http_status_u != 200 :
        return response_duplicate_username , http_status_u
    # verification duplicate emails
    response_duplicate_emails , http_status_e = find_duplicate_emails(csv_path)
    if http_status_e != 200 :
        return response_duplicate_emails , http_status_e
    # verification username exist in csv
    response_username_exists_csv , http_status_ue = username_exists_csv(csv_path)
    if http_status_ue != 200 :
        return response_username_exists_csv , http_status_ue
    # verification emails syntaxe in csv
    response_emails_syntaxe_csv , http_status_es = emails_syntaxe_csv(csv_path)
    if http_status_es != 200 :
        return response_emails_syntaxe_csv , http_status_es
    else : 
        return jsonify({"message": "Your csv is valide"}) , 200

############ VERIFICATION DUPLICATE USERNAMES DANS LE CSV ############
def find_duplicate_usernames(csv_path):
    usernames = {}  # Utilisez un dictionnaire pour stocker les lignes ou chaque nom d'utilisateur apparaît
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line_number = 1  # Initialisez le numero de ligne a 1
        for row in reader:
            username = row.get('username')
            if username in usernames:
                # Si le nom d'utilisateur existe deja dans le dictionnaire, ajoutez la ligne actuelle
                usernames[username].append(line_number)
            else:
                # Sinon, initialisez une nouvelle entree dans le dictionnaire avec le numero de ligne actuel
                usernames[username] = [line_number]
            line_number += 1  # Incrementez le numero de ligne pour la ligne suivante
    # Recherchez les noms d'utilisateur en double et les lignes correspondantes
    duplicates = {username: lines for username, lines in usernames.items() if len(lines) > 1}
    if duplicates:
        duplicate_usernames = []
        for username, lines in duplicates.items():
            duplicate_usernames.append(f"duplicates username : '{username}' at lines : {' , '.join(map(str, lines))}")
        return jsonify({"message": "Your csv file contains duplicate usernames", "duplicate usernames": duplicate_usernames }) , 400
    else:
        return jsonify({"message": "Your csv dont contains duplicate usernames"}) , 200

############ VERIFICATION DUPLICATE EMAILS DANS LE CSV ############
def find_duplicate_emails(csv_path):
    emails = {}  # Utilisez un dictionnaire pour stocker les lignes où chaque email apparaît
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line_number = 1  # Initialisez le numéro de ligne à 1
        for row in reader:
            email = row.get('email')
            if email in emails:
                # Si l'email existe déjà dans le dictionnaire, ajoutez la ligne actuelle
                emails[email].append(line_number)
            else:
                # Sinon, initialisez une nouvelle entrée dans le dictionnaire avec le numéro de ligne actuel
                emails[email] = [line_number]
            line_number += 1  # Incrémentez le numéro de ligne pour la ligne suivante
    # Recherchez les emails en double et les lignes correspondantes
    duplicates = {email: lines for email, lines in emails.items() if len(lines) > 1}
    if duplicates:
        duplicate_emails = []
        for email, lines in duplicates.items():
            duplicate_emails.append(f"duplicates email : '{email}' at lines : {' , '.join(map(str, lines))}")
        return jsonify({"message": "Your csv file contains duplicate emails", "duplicate emails": duplicate_emails }) , 400
    else:
        return jsonify({"message": "Your csv dont contains duplicate emails"}) , 200

############ VERIFICATION USERNAME EXISTES DANS LE CSV ############
def username_exists_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        username_exist = []
        line_number = 1  # Initialisez le numero de ligne à 1
        for row in reader:
            username = row.get("username")
            if username_exists(username) :
                username_exist.append(f"Existing username   : '{username}' , line {line_number} in CSV")
            line_number += 1
    if username_exist :
        return jsonify({"error": username_exist}) , 400
    else :
        return jsonify({"message": "Valide CSV"}) , 200

############ VERIFICATION EMAILS SYNTAXE DANS LE CSV ############
def emails_syntaxe_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        invalid_email = []
        line_number = 1  # Initialisez le numero de ligne à 1
        for row in reader:
            email = row.get("email")
            if not is_valid_email(email) :
                invalid_email.append( f"Invalid email format for : {email} , line {line_number} in CSV") , 400
            line_number += 1
    if line_number :
        return jsonify({"error": invalid_email}) , 400
    else :
        return jsonify({"message": "Valide CSV"}) , 200
    
############  VERIFICATION ID_STUDENT EXIST ################
def id_exists(id_student):
    # Fonction pour verifier si l'id user existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.students WHERE id = %s", (id_student,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION INE EXIST ################
def ine_exists(ine):
    # Fonction pour verifier si l'ine de l'etudiant existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.students WHERE ine = %s", (ine,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION NUMERO ETUDIANT EXIST ################
def student_number_exists(student_number):
    # Fonction pour verifier si le numero etudiant existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.students WHERE student_number = %s", (student_number,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############  VERIFICATION EMAIL EXIST ################
def email_exists(email):
    # Fonction pour verifier si l'email existe deja dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE email = %s", (email,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

############ VERIFICATION DUPLICATE INE DANS LE CSV ############
def find_duplicate_ines(csv_path):
    ines = {}  # Utilisez un dictionnaire pour stocker les lignes ou chaque ine apparaît
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line_number = 1  # Initialisez le numero de ligne a 1
        for row in reader:
            ine = row.get('ine')
            if ine in ines:
                # Si l'ine existe deja dans le dictionnaire, ajoutez la ligne actuelle
                ines[ine].append(line_number)
            else:
                # Sinon, initialisez une nouvelle entree dans le dictionnaire avec le numero de ligne actuel
                ines[ine] = [line_number]
            line_number += 1  # Incrementez le numero de ligne pour la ligne suivante
    # Recherchez les ine en double et les lignes correspondantes
    duplicates = {ine: lines for ine, lines in ines.items() if len(lines) > 1}
    if duplicates:
        duplicate_ines = []
        for ine, lines in duplicates.items():
            duplicate_ines.append(f"duplicates ine : '{ine}' at lines : {' , '.join(map(str, lines))}")
        return jsonify({"message": "Your csv file contains duplicate ine", "duplicate ine": duplicate_ines }) , 400
    else:
        return jsonify({"message": "Your csv dont contains duplicate ine"}) , 200
    
############ VERIFICATION DUPLICATE NUMERO ETUDIANT DANS LE CSV ############
def find_duplicate_student_number(csv_path):
    student_numbers = {}  # Utilisez un dictionnaire pour stocker les lignes ou chaque student_number apparaît
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line_number = 1  # Initialisez le numero de ligne a 1
        for row in reader:
            student_number = row.get('student_number')
            if student_number in student_numbers:
                # Si student_number existe deja dans le dictionnaire, ajoutez la ligne actuelle
                student_numbers[student_number].append(line_number)
            else:
                # Sinon, initialisez une nouvelle entree dans le dictionnaire avec le numero de ligne actuel
                student_numbers[student_number] = [line_number]
            line_number += 1  # Incrementez le numero de ligne pour la ligne suivante
    # Recherchez les student_numbers en double et les lignes correspondantes
    duplicates = {student_number: lines for student_number, lines in student_numbers.items() if len(lines) > 1}
    if duplicates:
        duplicate_student_numbers = []
        for student_number, lines in duplicates.items():
            duplicate_student_numbers.append(f"duplicates student numbers : '{student_number}' at lines : {' , '.join(map(str, lines))}")
        return jsonify({"message": "Your csv file contains duplicate student numbers", "duplicate student numbers": duplicate_student_numbers }) , 400
    else:
        return jsonify({"message": "Your csv dont contains duplicate ine"}) , 200