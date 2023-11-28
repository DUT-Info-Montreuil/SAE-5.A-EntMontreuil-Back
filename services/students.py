from flask import request, jsonify, Blueprint
import json
import connect_pg
import csv
import os
from entities.DTO.students import Students
from entities.model.studentsm import StudentsModel
from services.users import UsersFonction



class StudentsServices : 
    
    def __init__ (self):
        pass

    ############ STUDENTS/GET ############
    def get_all_students(self, output_format):
        """ Return all students in JSON format """
        query = """SELECT
                                        S.id, S.nip, S.apprentice, S.ine,
                                        U.username, U.last_name, U.first_name, U.email, U.isAdmin,
                                        TD.id,TD.name as td_name,
                                        TP.id,TP.name as tp_name,
                                        P.id, P.year as promotion_year, P.level as promotion_level,
                                        D.id as degree_id, D.name as degree_name,
                                        R.id as role_id, R.name as role_name,
                                        U.id
                    FROM
                        ent.Students S
                    INNER JOIN
                        ent.Users U ON S.id_User = U.id
                    LEFT JOIN
                        ent.TD TD ON S.id_Td = TD.id
                    LEFT JOIN
                        ent.TP TP ON S.id_Tp = TP.id
                    LEFT JOIN
                        ent.Promotions P ON S.id_Promotion = P.id
                    LEFT JOIN
                        ent.Degrees D ON P.id_Degree = D.id
                    LEFT JOIN
                        ent.Roles R ON U.id_Role = R.id
                    order  by s.id asc"""
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        returnStatement = []
        for row in rows:
            if output_format == 'dto' :
                student = Students(row[0], row[1], row[2], row[20], row[9], row[11], row[13], row[3])
            elif output_format == 'model' :
                student =  StudentsModel(*row[:-1])

            else :
                raise ValueError("Invalid output_format. Should be 'dto' or 'model'.")
            returnStatement.append(student.jsonify())
        connect_pg.disconnect(conn)
        return jsonify(returnStatement)

    ############ STUDENTS/GET/<int:id_students> ############
    def get_student(self, student_identifier):
            try:
                conn = connect_pg.connect()
                with conn.cursor() as cursor:
                    # Déterminer si student_identifier est un nombre (ID) ou une chaîne (username)
                    if isinstance(student_identifier, int) or student_identifier.isdigit():
                        where_clause = "S.id = %s"
                        params = (student_identifier,)
                    else:
                        where_clause = "U.username = %s"
                        params = (student_identifier,)

                    sql_query = f"""SELECT
                                        S.id, S.nip, S.apprentice, S.ine,
                                        U.username, U.last_name, U.first_name, U.email, U.isAdmin,
                                        TD.id,TD.name as td_name,
                                        TP.id,TP.name as tp_name,
                                        P.id, P.year as promotion_year, P.level as promotion_level,
                                        D.id as degree_id, D.name as degree_name,
                                        R.id as role_id, R.name as role_name,
                                        U.id
                    FROM
                        ent.Students S
                    INNER JOIN
                        ent.Users U ON S.id_User = U.id
                    LEFT JOIN
                        ent.TD TD ON S.id_Td = TD.id
                    LEFT JOIN
                        ent.TP TP ON S.id_Tp = TP.id
                    LEFT JOIN
                        ent.Promotions P ON S.id_Promotion = P.id
                    LEFT JOIN
                        ent.Degrees D ON P.id_Degree = D.id
                    LEFT JOIN
                        ent.Roles R ON U.id_Role = R.id
                    WHERE {where_clause}"""
                    
                    cursor.execute(sql_query, params)
                    row = cursor.fetchone()
                    if row:
                        return StudentsModel(*row[:-1]).jsonify()
                    else:
                        return None

            except Exception as e:
                raise e
            finally:
                conn.close()
    ############ STUDENTS/ADD ############
    def add_students(self, datas):
        data = datas["datas"]
        user_data = data["user"]
        # INE deja existant
        if StudentsFonction.field_exists('ine', data["ine"]) :
            return jsonify({"error": f"Ine '{data.get('ine')}' already exist"}) , 400
        # nip deja existant
        if StudentsFonction.field_exists('nip', data["nip"]) :
            return jsonify({"error": f"nip  {data.get('nip')} already exist"}) , 400

        if UsersFonction.field_exists('email',user_data["email"]) :
            return jsonify({"error": f"email {data.get('email')} already exist"}) , 400
        
        #Attribution du role student
        user_data["role"] = "student"
        
        # Si apprentice est mentionner sinon valeur par defaut a false
        if "apprentice" in data :
            apprentice = data["apprentice"]
        else :
            apprentice = False
        # Creation du student data json
        student_data = {
            "apprentice": apprentice,
            "ine" : data["ine"],
            "nip" : data["nip"]
        }
        
        # Recuperation du user id
        # Si id est present
        if "id" in data :
            # Verification si id existe deja
            if StudentsFonction.field_exists('id', data["id"]) :
                return jsonify({"error": f"Id for student '{data.get('id')}' already exist"}), 400
            else :
                student_data["id"] = data["id"]
        user_response, http_status = UsersFonction.add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status
        else :
            #on recupere le password de l'utilisateur ajouter pour savoir quel est sont mdp si il est generer aleatoirement
            password = user_response.json.get("password")
            
            user_id = user_response.json.get("id")
            student_data["id_User"] = user_id,
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

    ############ STUDENTS/REMOVE/<int:id_student> ############
    def delete_students(self, id_student):
        # Si id student n'existe pas
        if not StudentsFonction.field_exists('id',id_student) :
            raise ValidationError(f"id_student : '{id_student}' not exists")
        
        id_user = StudentsFonction.get_user_id_with_id_student(id_student)
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.students WHERE id = %s"
        cursor.execute(query, (id_student,))
        conn.commit()
        conn.close()
        UsersFonction.remove_users(id_user)
        return jsonify({"message": "Student deleted", "id": id_student}), 200


    ############ STUDENTS/UPDATE/<int:id_student> ############
    def update_students(self, id_student, datas):
        # Si il manque datas renvoie une erreur
        if not StudentsFonction.field_exists('id' , id_student) : 
            return jsonify({"error": f"id '{id_student} not exist"}) , 400
        if "ine" in student_data : 
            if StudentsFonction.field_exists('ine' , student_data["ine"] ) :
                return jsonify({"error": f"ine '{student_data.get('ine')}' already exist"}), 400
        if "nip" in student_data :
            if StudentsFonction.field_exists('nip' , student_data["nip"] ) :
                return jsonify({"error": f"nip '{student_data.get('nip')}' already exist"}), 400
        # Si il manque user renvoie une erreur
        if "user" in student_data:
            user_data = student_data["user"]
            # Supression du champ user pour garder les datas de l'etudiant
            
            del student_data["user"]
            # Si user data est vide
            if UsersFonction.field_exists('email' , user_data["email"] ) :
                return jsonify({"error": f"email '{user_data.get('email')}' already exist"}), 400
            # Recuperation du user id
            id_user = StudentsFonction.get_user_id_with_id_student(id_student)
            user_response, http_status = UsersFonction.update_users(user_data, id_user)
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

    ############ STUDENTS/CSV ############
    def csv_add_students(self, csv_path):
        #test avec : C:/Users/xxp90/Documents/BUT INFO/SAE EDT/csv_students.csv
        # Verification fichier valide
        response, http_status = StudentsFonction.verification_csv_file(csv_path) 
        if http_status != 200 :
            return response, http_status
        # Tableau de tout les mdp des user ajouter
        passwords = []
        # Recuperation du nom du fichier
        parts = csv_path.split("/") 
        filename = parts[-1]
        
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Pour chaque ligne ajoute l'etudiant
            for row in reader:
                add_student_response, http_status = StudentsFonction.add_students_fonction(row)
                if http_status != 200 :
                    return add_student_response, http_status
                # Recuperation des password des students ajouter
                json_with_password = add_student_response.json.get("json")
                passwords.append(json_with_password)
        return jsonify({"csv file": f"All students add from {filename}" ,"message" : "Saved all passwords for all user they will not be recoverable", "password" : passwords} ) , 200 


#--------------------------------------------------FONCTION--------------------------------------------------#
class StudentsFonction : 

    ############  RECUPERATION USER ID SELON ID_STUDENT  ################
    def get_user_id_with_id_student(id_student):
        # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_student
        conn = connect_pg.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id_User FROM ent.students WHERE id = %s", (id_student,))
        id_user = cursor.fetchone()[0]
        conn.close()
        return id_user

    ############ STUDENTS/ADD ############
    def add_students_fonction(data):
        try :
            user_data = {
                "email" : data["email"],
                "last_name" : data["last_name"],
                "first_name" : data["first_name"],
                "username" : data["username"]
            }
            user_data["role"] = "student"
            student_data = {
                "apprentice" : False,
                "ine" : data["ine"],
                "nip" : data["nip"]
            }
            user_response, http_status = UsersFonction.add_users(user_data)  
            password = user_response.json.get("password")
            user_id = user_response.json.get("id")
            student_data["id_User"] = user_id
            columns = list(student_data.keys())
            values = list(student_data.values())
            conn = connect_pg.connect()
            cursor = conn.cursor()
            query = f"INSERT INTO ent.students ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
            cursor.execute(query, values)
            row = cursor.fetchone()
            conn.commit()
            conn.close()  
            json_response = {
                "password" : password,
                "username" : user_data["username"]
            }
            return jsonify({"message": f"Student added id : {row[0]} ", "json":json_response }) , 200  
        except Exception as e:
            return jsonify({"message": "Error", "error": str(e)}) , 400 

    ############  VERIFICATION FIELD EXIST ################
    # Fonction pour verifier un champ existe deja dans la base de donnees
    def field_exists( field,data):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.students WHERE {field} = %s"
        cursor.execute(query, (data,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    ############ VERIFICATION CSV VALIDE ############
    def verification_csv_file(csv_path):
        if not os.path.exists(csv_path):
            return jsonify({"error": "file not found" , "invalid path" : csv_path }), 400

        # verification des champs dupliquer dans le fichier csv
        duplicate_fields = ['username', 'email', 'ine', 'nip']
        for field in duplicate_fields :
            response_duplicate , http_status = StudentsFonction.find_duplicate_field(csv_path, field)
            if http_status != 200 :
                return response_duplicate , http_status
            
        # verification si un champs est vide dans le csv
        response_empty_field_csv , http_status_ef = StudentsFonction.empty_field_csv(csv_path)
        if http_status_ef != 200 :
            return response_empty_field_csv , http_status_ef
        
        # verification emails syntaxe in csv
        response_emails_syntaxe_csv , http_status_es = StudentsFonction.emails_syntaxe_csv(csv_path)
        if http_status_es != 200 :
            return response_emails_syntaxe_csv , http_status_es
        
        
        # verification des champs de users deja existant dans la bd    
        existing_user_field = ['email', 'username']
        for user_field in existing_user_field : 
            response_existing_user_field , http_status = StudentsFonction.field_users_exists_csv(csv_path, user_field)
            if http_status != 200 :
                return response_existing_user_field , http_status
            
        # verification des champs de students deja existant dans la bd    
        existing_student_field = ['ine', 'nip']
        for field in existing_student_field : 
            response_existing_student_field , http_status = StudentsFonction.field_students_exists_csv(csv_path, field)
            if http_status != 200 :
                return response_existing_student_field , http_status
        return jsonify({"messsage": "Valid CSV"}), 200 
        
    ############ VERIFICATION DUPLICATE FILDS IN CSV ############
    def find_duplicate_field(csv_path , param):
        fields = {} 
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            line_number = 1  
            for row in reader:
                field = row[param]
                if field in fields:
                    fields[field].append(line_number)
                else:
                    fields[field] = [line_number]
                line_number += 1 
        duplicates = {field: lines for field, lines in fields.items() if len(lines) > 1}
        if duplicates:
            duplicate_fields = []
            for field, lines in duplicates.items():
                duplicate_fields.append(f"duplicates {param} : '{field}' at lines : {' , '.join(map(str, lines))}")
            return jsonify({"message": f"Your csv file contains duplicate {field}s", f"duplicate {param}": duplicate_fields }) , 400
        else:
            return jsonify({"message":f"Your csv dont contains duplicate '{param}'"}) , 200

    ############ VERIFICATION USER FIELD EXISTES IN CSV ############
    def field_users_exists_csv(csv_path,param):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_field = []
            line_number = 1 
            for row in reader:
                field = row[param]
                if UsersFonction.field_exists(param,field) :
                    existing_field.append(f"Existing {param} : '{field}' , line {line_number} in CSV")
                line_number += 1
        if existing_field :
            return jsonify({"error": existing_field}) , 400
        else :
            return jsonify({"message": "Valide CSV"}) , 200
        
    ############ VERIFICATION STUDENT FIELD EXISTES IN CSV ############
    def field_students_exists_csv(csv_path,param):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_field = []
            line_number = 1 
            for row in reader:
                field = row[param]
                if StudentsFonction.field_exists(param,field) :
                    existing_field.append(f"Existing {param}   : '{field}' , line {line_number} in CSV")
                line_number += 1
        if existing_field :
            return jsonify({"error": existing_field}) , 400
        else :
            return jsonify({"message": "Valide CSV"}) , 200

    ############ VERIFICATION EMAILS SYNTAXE IN CSV ############
    def emails_syntaxe_csv(csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            invalid_email = []
            line_number = 1  
            for row in reader:
                email = row.get("email")
                if not UsersFonction.is_valid_email(email) :
                    invalid_email.append( f"Invalid email format for : {email} , line {line_number} in CSV") , 400
                line_number += 1
        if invalid_email :
            return jsonify({"error": invalid_email}) , 400
        else :
            return jsonify({"message" : "Valide CSV"}) , 200
         
     ############ VERIFICATION EMPTY FIELD IN CSV ############
    def empty_field_csv(path) :
        try:
            with open(path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row_number, row in enumerate(csv_reader, start=1):
                    for field in row:
                        if not field:
                            return jsonify({"message": f"Field {row} is empty in row {row_number}"}), 400
            return jsonify({"message": "No empty fields found in CSV"}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400
#----------------------------------ERROR-------------------------------------
class ValidationError(Exception) :
    pass