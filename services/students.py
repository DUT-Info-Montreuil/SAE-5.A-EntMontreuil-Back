from flask import request, jsonify, Blueprint
import json
import connect_pg
import csv
import os
import io
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
                
                
    ############  ############
    def get_all_students_in_promo(self, promotion_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                SELECT s.*, u.username, u.last_name, u.first_name, u.email, 
                   td.name AS td_name, tp.name AS tp_name,
                   p.year, p.level, d.name AS degree_name
                FROM ent.students s
                JOIN ent.users u ON s.id_user = u.id
                LEFT JOIN ent.tp tp ON s.id_tp = tp.id
                LEFT JOIN ent.td td ON tp.id_td = td.id
                JOIN ent.promotions p ON s.id_promotion = p.id
                JOIN ent.degrees d ON p.id_degree = d.id
                WHERE s.id_promotion = %s;
                """
                cursor.execute(sql_query, (promotion_id,))
                students = cursor.fetchall()
                students_list = [
                    {
                        "student_id": row[0], "apprentice": row[1], 
                        "username": row[8], "last_name": row[9], 
                        "first_name": row[10], "email": row[11],
                        "td_name": row[12], "tp_name": row[13],
                        "promotion_year": row[14], "promotion_level": row[15], 
                        "degree_name": row[16]
                    } 
                    for row in students
            ]
                return jsonify(students_list), 200
        except Exception as e:
            raise e
        finally:
            conn.close()
            
    def get_all_students_cohort(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                SELECT s.*, u.username, u.last_name, u.first_name, u.email, 
                td.name AS td_name, tp.name AS tp_name,
                p.year, p.level, d.name AS degree_name
                FROM ent.students s
                JOIN ent.users u ON s.id_user = u.id
                LEFT JOIN ent.tp tp ON s.id_tp = tp.id
                LEFT JOIN ent.td td ON tp.id_td = td.id
                LEFT JOIN ent.promotions p ON s.id_promotion = p.id
                LEFT JOIN ent.degrees d ON p.id_degree = d.id;      
                """
                cursor.execute(sql_query)
                students = cursor.fetchall()
                students_list = [
                    {
                        "student_id": row[0], "apprentice": row[1], 
                        "username": row[8], "last_name": row[9], 
                        "first_name": row[10], "email": row[11],
                        "td_name": row[12], "tp_name": row[13],
                        "promotion_year": row[14] if row[14] else None,  # Gère les valeurs NULL
                        "promotion_level": row[15] if row[15] else None,  # Gère les valeurs NULL
                        "degree_name": row[16] if row[16] else None  # Gère les valeurs NULL
                    } 
                for row in students
        ]
            return jsonify(students_list), 200
        except Exception as e:
            raise e
        finally:
            conn.close()
            
    def get_students_without_promotion(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                SELECT s.*, u.username, u.last_name, u.first_name, u.email, 
                td.name AS td_name, tp.name AS tp_name,
                p.year, p.level, d.name AS degree_name
                FROM ent.students s
                JOIN ent.users u ON s.id_user = u.id
                LEFT JOIN ent.tp tp ON s.id_tp = tp.id
                LEFT JOIN ent.td td ON tp.id_td = td.id
                LEFT JOIN ent.promotions p ON s.id_promotion = p.id
                LEFT JOIN ent.degrees d ON p.id_degree = d.id
                WHERE s.id_promotion IS NULL;      
                """
                cursor.execute(sql_query)
                students = cursor.fetchall()
                students_list = [
                    {
                        "student_id": row[0], "apprentice": row[1], 
                        "username": row[8], "last_name": row[9], 
                        "first_name": row[10], "email": row[11],
                        "td_name": row[12], "tp_name": row[13],
                        "promotion_year": row[14] if row[14] else None,
                        "promotion_level": row[15] if row[15] else None,
                        "degree_name": row[16] if row[16] else None
                    } 
                for row in students
            ]
                return jsonify(students_list), 200
        except Exception as e:
            raise e
        finally:
            conn.close()
            
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

   
    def get_all_students_without_td_tp(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                SELECT s.*, u.username, u.last_name, u.first_name, u.email 
                FROM ent.students s
                JOIN ent.users u ON s.id_user = u.id
                WHERE s.id_td IS NULL AND s.id_tp IS NULL;
                """
                cursor.execute(sql_query)
                students = cursor.fetchall()
                students_list = [{"student_id": row[0], "apprentice": row[1], "id_td": row[5], "id_tp": row[6], "id_promotion": row[7], "username": row[8], "last_name": row[9], "first_name": row[10], "email": row[11]} for row in students]
                return jsonify(students_list), 200
            
        except Exception as e:
            raise e
        finally:
            conn.close()
            
            
    def set_students_promotion(self, promotion_id, student_ids):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Mettre à jour l'id_promotion pour chaque étudiant et réinitialiser id_tp et id_td
                for student_id in student_ids:
                    cursor.execute("""
                        UPDATE ent.Students 
                        SET id_promotion = %s, id_tp = NULL, id_td = NULL
                        WHERE id = %s
                    """, (promotion_id, student_id))

            conn.commit()
            return jsonify({"message": "Promotion et associations TP/TD mises à jour avec succès pour les étudiants sélectionnés"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)


                
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
        user_data["role"] = "étudiant"
        
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
        user_response, http_status = UsersFonction.add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status
        else :
            #on recupere le password de l'utilisateur ajouter pour savoir quel est sont mdp si il est generer aleatoirement
            password = user_response.json.get("password")
            
            user_id = user_response.json.get("id")
            student_data["id"] = user_id
            student_data["id_User"] = user_id
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
            return jsonify({"message": "Veuillez à bien enregistrer le mot de passe générer aléatoirement, il ne sera pas récupérable.", "id": row[0], "username" : user_data["username"] , "password" : password }) , 200  

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
    def update_students(self, id_student, student_data):
        # Si il manque datas renvoie une erreur
        if not StudentsFonction.field_exists('id' , id_student) : 
            return jsonify({"error": f"id '{id_student} not exist"}) , 400
        if "ine" in student_data : 
            if StudentsFonction.field_exists_with_old_field('ine' , student_data["ine"], student_data["old_ine"] ) :
                return jsonify({"error": f"INE '{student_data.get('ine')}' déjà existant"}), 400
        if "nip" in student_data :
            if StudentsFonction.field_exists_with_old_field('nip' , student_data["nip"], student_data["old_nip"] ) :
                return jsonify({"error": f"NIP '{student_data.get('nip')}' déjà existant"}), 400
        # Si il manque user renvoie une erreur
        if "user" in student_data:
            user_data = student_data["user"]
            # Supression du champ user pour garder les datas de l'etudiant
            
            del student_data["user"]
            # Si user data est vide

            # Recuperation du user id
            id_user = StudentsFonction.get_user_id_with_id_student(id_student)
            user_response, http_status = UsersFonction.update_users(user_data, id_user)
            # Si user update echoue
            if http_status != 200 :
                return user_response, http_status
        # Si student data n'est pas vide
        if student_data :
            del student_data['old_ine']
            del student_data['old_nip']
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
    def csv_add_students(self, file):
        # Verification fichier valide
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.DictReader(stream, delimiter=',')
        data_list = list(reader)
        # Tableau de tout les mdp des user ajouter
        passwords = []
        # Recuperation du nom du fichier
        filename = file.filename
        # Pour chaque ligne ajoute l'etudiant
        for row in data_list:
            add_student_response, http_status = StudentsFonction.add_students_fonction(row)
            if http_status != 200 :
                return add_student_response, http_status
            # Recuperation des password des students ajouter
            json_with_password = add_student_response.json.get("json")
            passwords.append(json_with_password)
        return jsonify({"csv file": f"All students add from {filename}" ,"message" : "Saved all passwords for all user they will not be recoverable", "password" : passwords} ) , 200 
    
    ############ VERIFICATION CSV VALIDE ############
    def verification_csv_file(self, file):
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.DictReader(stream, delimiter=',')
        data_list = list(reader)
        response , http_status = StudentsFonction.all_field_csv(data_list)
        if http_status !=200:
            return response , http_status
        # verification des champs dupliquer dans le fichier csv
        duplicate_fields = ['username', 'email', 'ine', 'nip']
        for field in duplicate_fields : 
            response_duplicate , http_status_2 = StudentsFonction.find_duplicate_field(data_list, field)
            if http_status_2 != 200 :
                return response_duplicate , http_status_2
        
        # verification emails syntaxe in csv
        response_emails_syntaxe_csv , http_status_es = StudentsFonction.emails_syntaxe_csv(data_list)
        if http_status_es != 200 :
            return response_emails_syntaxe_csv , http_status_es
        
        
        # verification des champs de users deja existant dans la bd    
        existing_user_field = ['email', 'username']
        for user_field in existing_user_field : 
            response_existing_user_field , http_status_u = StudentsFonction.field_users_exists_csv(data_list, user_field)
            if http_status_u != 200 :
                return response_existing_user_field , http_status_u
            
        # verification des champs de students deja existant dans la bd    
        existing_student_field = ['ine', 'nip']
        for field in existing_student_field : 
            response_existing_student_field , http_status_sf = StudentsFonction.field_students_exists_csv(data_list, field)
            if http_status_sf != 200 :
                return response_existing_student_field , http_status_sf
            
        # verification username len < 4 in csv
        response_username_csv , http_status_uc = StudentsFonction.username_4_char_csv(data_list)
        if http_status_uc != 200 :
            return response_username_csv , http_status_uc
            
        return jsonify({"error": "OUIIII", "valide_csv" : "true" }), 200 


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
            user_data["role"] = "étudiant"
            student_data = {
                "apprentice" : False,
                "ine" : data["ine"],
                "nip" : data["nip"]
            }
            user_response, http_status = UsersFonction.add_users(user_data)  
            password = user_response.json.get("password")
            user_id = user_response.json.get("id")
            student_data["id_User"] = user_id
            student_data["id"] = user_id
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
    
    def field_exists_with_old_field( field,data, old_data):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.students WHERE {field} = %s AND {field} != '{old_data}'"
        cursor.execute(query, (data,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    
    
    ############ VERIFICATION DUPLICATE FILDS IN CSV ############
    def find_duplicate_field(data_list, param):
        try:
            line_number = 1
            fields = {}
            for row in data_list:
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
                    duplicate_fields.append(f"il y a une duplication du champ {param} : '{field}' à la ligne : {', '.join(map(str, lines))}")
                return jsonify({"error": duplicate_fields}), 400
            else:
                return jsonify({"message": f"Your CSV file doesn't contain duplicate '{param}'"}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    ############ VERIFICATION USER FIELD EXISTES IN CSV ############
    def field_users_exists_csv(data_list,param):
        existing_field = []
        line_number = 1 
        for row in data_list:
            field = row[param]
            if UsersFonction.field_exists(param,field) :
                existing_field.append(f"{param} déjà existant : '{field}' à la ligne {line_number} du fichier CSV")
            line_number += 1
        if existing_field :
            return jsonify({"error": existing_field}) , 400
        else :
            return jsonify({"message": "Valide CSV"}) , 200
        
    ############ VERIFICATION STUDENT FIELD EXISTES IN CSV ############
    def field_students_exists_csv(data_list,param):
        existing_field = []
        line_number = 1 
        for row in data_list:
            field = row[param]
            if StudentsFonction.field_exists(param,field) :
                existing_field.append(f"{param} déjà existant : '{field}' à la ligne {line_number} du fichier CSV")
            line_number += 1
        if existing_field :
            return jsonify({"error": existing_field}) , 400
        else :
            return jsonify({"message": "Valide CSV"}) , 200

    ############ VERIFICATION EMAILS SYNTAXE IN CSV ############
    def emails_syntaxe_csv(data_list):
        invalid_email = []
        line_number = 1  
        for row in data_list:
            email = row.get("email")
            if not UsersFonction.is_valid_email(email) :
                invalid_email.append( f"Le format de l'email : '{email}' est invalid à la ligne {line_number} du fichier CSV") , 400
            line_number += 1
        if invalid_email :
            return jsonify({"error": invalid_email}) , 400
        else :
            return jsonify({"message" : "Valide CSV"}) , 200
         
        
    ############ VERIFICATION ALL FIELD IN CSV ############
    def all_field_csv(data_list) :
        try:
            field_obligatoire = ['username','email','ine','nip','last_name','first_name']
            for row in data_list:
                for field in field_obligatoire:
                    if field not in row:
                        return jsonify({"error" : f"Le champ {field} n'est pas présent ou mal écrit dans votre fichier CSV."}) , 400
            return jsonify({"message" : "Valide CSV all field"}) , 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 400
        
    ############ VERIFICATION EMAILS SYNTAXE IN CSV ############
    def username_4_char_csv(data_list):
        invalid_username = []
        line_number = 1  
        for row in data_list:
            username = row.get("username")
            if len(username) < 4:
                invalid_username.append( f"Le username : '{username}' doit contenir minimum 4 caractères à la ligne {line_number} du fichier CSV") , 400
            line_number += 1
        if invalid_username :
            return jsonify({"error": invalid_username}) , 400
        else :
            return jsonify({"message" : "Valide CSV"}) , 200
        
        


#----------------------------------ERROR-------------------------------------
class ValidationError(Exception) :
    pass
"""ENT Montreuil is a Desktop Working Environnement for the students of the IUT of Montreuil
    Copyright (C) 2024  Steven CHING, Emilio CYRIAQUE-SOURISSEAU ALVARO-SEMEDO, Ismail GADA, Yanis HAMANI, Priyank SOLANKI

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""