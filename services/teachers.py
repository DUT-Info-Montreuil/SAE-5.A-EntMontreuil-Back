from flask import request, jsonify, Blueprint
import json
import connect_pg
from entities.DTO.teachers import Teachers
from entities.model.teachersm import TeachersModel
from services.users import UsersFonction


#--------------------------------------------------ROUTE--------------------------------------------------#
class TeachersService :
    
    ############  TEACHERS/GET ################
    def get_teachers(self, output_format):
        """ Return all teachers in JSON format """
        query = "select t.id, initial, desktop, id_User, u.last_name, u.first_name, u.username, u.email, u.isAdmin, r.id, r.name from ent.teachers t inner join ent.users u on u.id = t.id_User inner join ent.roles r on r.id = u.id_role order by t.id asc"
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
        user_data["role"] = "teacher"
        
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
            if "id" in data : 
                teacher_data["id"] = data.get("id")
            
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
            query = f"select t.id, initial, desktop, id_User, u.last_name, u.first_name, u.username, u.email, u.isAdmin, r.id, r.name from ent.teachers t inner join ent.users u on u.id = t.id_User inner join ent.roles r on r.id = u.id_role where {where_clause}"
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