from flask import request, jsonify, Blueprint
import json
import connect_pg
from entities.DTO.teachers import Teachers
from entities.model.teachersm import TeachersModel
from entities.DTO.commentary import Commentary
from entities.model.commentarym import CommentaryModel
from services.users import UsersFonction
from datetime import datetime as D
from datetime import timedelta


#--------------------------------------------------ROUTE--------------------------------------------------#
class TeachersService :
    
    ############  TEACHERS/GET ################
    def get_teachers(self, output_format):
        """ Return all teachers in JSON format """
        query = "select t.id, initial, desktop, id_User, u.last_name, u.first_name, u.username, u.email, u.isAdmin, r.id, r.name, u.isTTManager from ent.teachers t inner join ent.users u on u.id = t.id_User inner join ent.roles r on r.id = u.id_role order by t.id asc"
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        returnStatement = []

        for row in rows:
            if output_format == 'dto':
                teacher_instance = Teachers(row[0], row[1], row[2], row[3])
            elif output_format == 'model':
                teacher_instance = TeachersModel(*row)
            else:
                raise ValueError("Invalid output_format. Should be 'dto' or 'model'.")
            returnStatement.append(teacher_instance.jsonify())

        connect_pg.disconnect(conn)
        return jsonify(returnStatement)

    ############ TEACHERS/ADD ############
    def add_teachers(self, datas):

        data = datas["datas"]
        user_data = data["user"]
        user_data["role"] = "enseignant"
        
        if TeachersFonction.field_exists('initial', data.get("initial")) :
            return jsonify({"error": f"Les initials '{data.get('initial')}' sont déjà utilisé"}), 400
         # Si data est present
        if "id" in data :
            if TeachersFonction.field_exists('id', data["id"]) :
                return jsonify({"error": f"Id for teacher '{data.get('id')}' already exist"}), 400
            
        user_response, http_status = UsersFonction.add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status 
        else :
            # Recuperation du password (si il est generer aleatoirement)
            password = user_response.json.get("password")
            # Recuperation du user id
            user_id = user_response.json.get("id")
            # Construction json de teacher_data
            teacher_data = {
                "desktop": data.get("desktop"),
                "initial": data.get("initial"),
                "id_User" : user_id
            }
            teacher_data["id"] = user_id
            
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
            return jsonify({"message": "Teachers added, save the password for this user it will not be recoverable", "id": row[0], "username" : user_data["username"] , "password" : password}) , 200  

    ############ TEACHERS/UPDATE/<int:id_teacher> ############
    def update_teachers(self, id_teacher, datas):
        if not TeachersFonction.field_exists('id' , id_teacher) : 
            return jsonify({"error": f"id '{id_teacher} not exist"}) , 400 
        
        teacher_data = datas["datas"]
        # Si initial est present
        if "initial" in teacher_data :
            
            # Verification initial existe deja
            if TeachersFonction.field_exists_initial( teacher_data.get('initial'), teacher_data.get('old_initial')) :
                return jsonify({"error": f"Les initials '{teacher_data.get('initial')}'éxiste déjà"}), 400
            del teacher_data["old_initial"]
        # Si id est present
        if "id" in teacher_data :
            return jsonify({"error": "Unable to modify user id, remove id field"}), 400
        # Si user est present
        if "user" in teacher_data:
            user_data = teacher_data["user"]
            # Supprimer les user data pour avoir que les data du teacher
            del teacher_data["user"]
            # Si user data est vide
            if not user_data:
                return jsonify({"error": "Empty 'user' field in JSON"}), 400
            # Recuperation de l'id utilisateur
            id_user = TeachersFonction.get_user_id_with_id_teacher(id_teacher)
            # Update de user
            user_response, http_status = UsersFonction.update_users(user_data, id_user)
            # Si erreur dans l'update du user
            if http_status != 200 :
                return user_response, http_status
        # Si teacher data n'est pas vide
        if teacher_data :
            conn = connect_pg.connect()
            cursor = conn.cursor()
            update_clause = ", ".join([f"{key} = %s" for key in teacher_data.keys()])
            values = list(teacher_data.values())
            values.append(id_teacher)  # Ajoutez l'ID de l'enseignant à la fin pour identifier l'enregistrement a mettre a jour
            query = f"UPDATE ent.teachers SET {update_clause} WHERE id = %s"
            cursor.execute(query, values)
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
        return jsonify({"message": "Teacher update", "id": id_teacher}) , 200 


    ############ TEACHERS/REMOVE/<int:id_teacher> ############
    def delete_teachers(self, id_teacher):

        if not TeachersFonction.field_exists('id' , id_teacher) :
            return jsonify({"error": f"id_teacher : '{id_teacher}' not exists"}) , 400
        id_user = TeachersFonction.get_user_id_with_id_teacher(id_teacher)

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.teachers WHERE id = %s"
        cursor.execute(query, (id_teacher,))
        conn.commit()
        conn.close()
        user_response, http_status = UsersFonction.remove_users(id_user)
        return jsonify({"message": "Teacher deleted", "id": id_teacher}), 200

    ############ TEACHERS/GET/<int:id_teacher> ############
    #@teachers_bp.route('/teachers/<int:id_teacher>', methods=['GET', 'POST'])
    def get_teacher(self, teacher_identifier , output_format):
        try:
            
            if isinstance(teacher_identifier, int) or teacher_identifier.isdigit():
                if not TeachersFonction.field_exists('id' , teacher_identifier) :
                    return jsonify({"error": f"id_teacher : '{teacher_identifier}' not exists"}) , 400
                where_clause = "t.id = %s"
            else:
                if not UsersFonction.field_exists('username' , teacher_identifier) :
                    return jsonify({"error": f"username : '{teacher_identifier}' not exists"}) , 400
                where_clause = "u.username = %s"
            conn = connect_pg.connect()
            cursor = conn.cursor()
            query = f"select t.id, initial, desktop, id_User, u.last_name, u.first_name, u.username, u.email, u.isAdmin, r.id, r.name, u.isTTManager from ent.teachers t inner join ent.users u on u.id = t.id_User inner join ent.roles r on r.id = u.id_role where {where_clause}"
            cursor.execute(query, (teacher_identifier,))
            row = cursor.fetchone()
            conn.commit()
            conn.close()
            if output_format == 'dto':
                return Teachers(row[0], row[1], row[2], row[3]).jsonify()
            elif output_format == 'model':
                return TeachersModel(*row).jsonify()
            else:
                raise ValueError("Invalid output_format. Should be 'dto' or 'model'.")
        except Exception as e:
            return jsonify({"message": "Error", "error": str(e)}), 400

        

    ############ TEACHERS : GET_NUMBER_OF_HOURS  <int:id_teacher> ############
    def get_number_of_hours(self, id_teacher):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL avec conversion des heures au format TIME pour PostgreSQL
            query = """
                SELECT (SUM(EXTRACT(EPOCH FROM ent.Courses.endTime) - EXTRACT(EPOCH FROM ent.Courses.startTime)) * INTERVAL '1 second') AS total_hours
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s
            """
            cursor.execute(query, (id_teacher,))
            total_hours = cursor.fetchone()[0]

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher,'total_hours': str(total_hours)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

    ############ TEACHERS : GET_NUMBER_OF_HOURS_LEFT <int:id_teacher> ############
    def get_number_of_hours_left(self, id_teacher):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures restantes (non encore passées)
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_left
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND (ent.Courses.dateCourse > CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime > CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher,))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_left = result[0]
            else:
                hours_left = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_left': str(hours_left)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    ############ TEACHERS : GET_NUMBER_OF_HOURS_PASSED <int:id_teacher> ############    
    def get_number_of_hours_passed(self, id_teacher):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures déjà passées
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_passed
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND (ent.Courses.dateCourse < CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime <= CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher,))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_passed = result[0]
            else:
                hours_passed = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_passed': str(hours_passed)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    ##########################################################################################################

    ############ TEACHERS : GET_HOURS_BY_MONTH ############    
    def get_hours_by_month(self, id_teacher, year, month):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par mois
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND EXTRACT(YEAR FROM ent.Courses.dateCourse) = %s
                    AND EXTRACT(MONTH FROM ent.Courses.dateCourse) = %s
            """
            cursor.execute(query, (id_teacher, year, month))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_worked': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    
    ############ TEACHERS : GET_LEFT_HOURS_BY_MONTH ############    
    def get_left_hours_by_month(self, id_teacher, year, month):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures à effectuer par mois
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND EXTRACT(YEAR FROM ent.Courses.dateCourse) = %s
                    AND EXTRACT(MONTH FROM ent.Courses.dateCourse) = %s
                    AND (ent.Courses.dateCourse > CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime > CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, year, month))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_left': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        
    ############ TEACHERS : GET_PASSED_HOURS_BY_MONTH ############    
    def get_passed_hours_by_month(self, id_teacher, year, month):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par mois
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND EXTRACT(YEAR FROM ent.Courses.dateCourse) = %s
                    AND EXTRACT(MONTH FROM ent.Courses.dateCourse) = %s
                    AND (ent.Courses.dateCourse < CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime <= CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, year, month))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_passed': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        


    ##########################################################################################################

    ############ TEACHERS : GET_HOURS_BY_RESOURCE ############    
    def get_hours_by_resource(self, id_teacher, id_resource):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par matière
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s AND ent.Courses.id_Resource = %s
            """
            cursor.execute(query, (id_teacher, id_resource))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_worked': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    ############ TEACHERS : GET_LEFT_HOURS_BY_RESOURCE ############    
    def get_left_hours_by_resource(self, id_teacher, id_resource):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures à effectuer par matière
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND ent.Courses.id_Resource = %s
                    AND (ent.Courses.dateCourse > CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime > CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, id_resource))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_left': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    
    ############ TEACHERS : GET_PASSED_HOURS_BY_RESOURCE ############    
    def get_passed_hours_by_resource(self, id_teacher, id_resource):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par matière
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND ent.Courses.id_Resource = %s
                    AND (ent.Courses.dateCourse < CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime <= CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, id_resource))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_passed': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    ##########################################################################################################

    ############ TEACHERS : GET_HOURS_BY_PROMOTION ############    
    def get_hours_by_promotion(self, id_teacher, id_promotion):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par promotion
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s AND ent.Courses.id_promotion = %s
            """
            cursor.execute(query, (id_teacher, id_promotion))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_worked': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    ############ TEACHERS : GET_LEFT_HOURS_BY_PROMOTION ############    
    def get_left_hours_by_promotion(self, id_teacher, id_promotion):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures à effectuer par promotion
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND ent.Courses.id_promotion = %s
                    AND (ent.Courses.dateCourse > CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime > CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, id_promotion))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_left': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
     
     ############ TEACHERS : GET_PASSED_HOURS_BY_PROMOTION ############    
    def get_passed_hours_by_promotion(self, id_teacher, id_promotion):
        try:
            if not TeachersFonction.field_exists('id', id_teacher):
                return jsonify({"error": f"id_teacher: '{id_teacher}' not exists"}), 400

            # Connexion à la base de données
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour obtenir les heures effectuées par promotion
            query = """
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM ent.Courses.endTime - ent.Courses.startTime)), 0) * INTERVAL '1 second' AS hours_worked
                FROM ent.Courses
                JOIN ent.Courses_Teachers ON ent.Courses.id = ent.Courses_Teachers.id_Course
                WHERE ent.Courses_Teachers.id_Teacher = %s 
                    AND ent.Courses.id_promotion = %s
                    AND (ent.Courses.dateCourse < CURRENT_DATE OR 
                        (ent.Courses.dateCourse = CURRENT_DATE AND ent.Courses.endTime <= CURRENT_TIME))
            """
            cursor.execute(query, (id_teacher, id_promotion))
            result = cursor.fetchone()

            if result and result[0] is not None:
                hours_worked = result[0]
            else:
                hours_worked = 0

            # Fermeture de la connexion
            conn.close()

            return jsonify({'id_Teacher': id_teacher, 'hours_passed': str(hours_worked)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
     
    ##########################################################################################################
        
    ############  TEACHERS/GETBYIDUSER/<int:id_user> ################
    def get_teacher_by_id_user(self, id_user):
        try:
            # Vérifiez si l'ID utilisateur est valide
            if not UsersFonction.field_exists('id', id_user):
                return jsonify({"error": f"id_user: '{id_user}' not exists"}), 400

            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Requête SQL pour récupérer l'enseignant par id_user
            query = """
            SELECT t.id
            FROM ent.teachers t 
            INNER JOIN ent.users u ON u.id = t.id_User 
            INNER JOIN ent.roles r ON r.id = u.id_role 
            WHERE t.id_User = %s
            """

            cursor.execute(query, (id_user,))
            row = cursor.fetchone()

            conn.commit()
            conn.close()

            if not row:
                return jsonify({"error": f"No teacher found with id_user: '{id_user}'"}), 404

            return jsonify({'id_Teacher': row[0], 'id_user': id_user}), 200

        except Exception as e:
            return jsonify({"message": "Error", "error": str(e)}), 400


    ############  GET_TEACHERS_PROMOTIONS ################
    def get_teacher_promotions(self, teacher_id):
        """ Return promotions for a given teacher in JSON format with teacher's ID and promotions data """
        
        query = """
        SELECT DISTINCT p.id, p.year, p.level, d.name
        FROM ent.promotions p
        INNER JOIN ent.courses c ON p.id = c.id_Promotion
        INNER JOIN ent.courses_teachers ct ON c.id = ct.id_Course
        INNER JOIN ent.teachers t ON ct.id_Teacher = t.id
        INNER JOIN ent.degrees d ON p.id_Degree = d.id
        WHERE t.id = %s
        ORDER BY p.year, p.level;
        """
        
        conn = connect_pg.connect()

        with conn.cursor() as cursor:

            cursor.execute(query, (teacher_id,))
            
            rows = cursor.fetchall()
            
            promotions_list = []
            
            for row in rows:
                promotion = {
                    "id": row[0],
                    "year": row[1],
                    "level": row[2],
                    "degree_name": row[3]
                }
                promotions_list.append(promotion)
            
            result = {
                "id_teacher": teacher_id,
                "data": promotions_list
            }

            connect_pg.disconnect(conn)
        
        return jsonify(result)



#--------------------------------------------------FONCTION--------------------------------------------------#
class TeachersFonction :

    ############  RECUPERATION USER ID SELON ID_TEACHER  ################
    def get_user_id_with_id_teacher(id_teacher):
        # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_teacher
        conn = connect_pg.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id_User FROM ent.teachers WHERE id = %s", (id_teacher,))
        id_user = cursor.fetchone()[0]
        conn.close()
        return id_user

    
    ############  VERIFICATION FIELD EXIST ################
    # Fonction pour verifier un champ existe deja dans la base de donnees
    def field_exists( field,data):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.teachers WHERE {field} = %s"
        cursor.execute(query, (data,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    
    def field_exists_initial( initial,old_initial):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.teachers WHERE initial = %s AND initial != '{old_initial}'"
        cursor.execute(query, (initial,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    

    

#--------------------------------------------------ERROR--------------------------------------------------#

class ValueError(Exception):
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