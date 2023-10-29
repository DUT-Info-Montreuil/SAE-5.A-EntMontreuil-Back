from flask import request, jsonify, Blueprint
import json
import connect_pg
from users import *


teachers_bp = Blueprint('teachers', __name__)

#--------------------------------------------------ROUTE--------------------------------------------------#

############  TEACHERS/GET ################
@teachers_bp.route('/teachers', methods=['GET','POST'])
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

############  TEACHERS/GET/TIMETABLE_MANAGER ################
@teachers_bp.route('/teachers/ttm', methods=['GET','POST'])
def get_teachers_timetable_manager():
    """ Return all teachers who are timetable manager in JSON format """
    query = "select * from ent.teachers where timetable_manager = true order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_teacher_statement(row))
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

############ TEACHERS/ADD ############
@teachers_bp.route('/teachers/add', methods=['POST'])
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

############ TEACHERS/UPDATE/<int:id_teacher> ############
@teachers_bp.route('/teachers/update/<int:id_teacher>', methods=['PATCH'])
def update_teachers(id_teacher):
    try:
        jsonObject = request.json
        if "datas" not in jsonObject:
            return jsonify({"error": "Missing 'datas' field in JSON"}) , 400 
        teacher_data = jsonObject["datas"]
        if "initial" in teacher_data :
            if initial_exists(teacher_data.get("initial")) :
                return jsonify({"error": f"Initial '{teacher_data.get('initial')}' already exists"}), 400
        if "user" in teacher_data:
            user_data = teacher_data["user"]
            del teacher_data["user"]
            if not user_data:
                return jsonify({"error": "Empty 'user' field in JSON"}), 400
            id_user = get_user_id_with_id_teacher(id_teacher)
            user_response, http_status = update_users(user_data, id_user)
            if http_status != 200 :
                return user_response, http_status
        

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
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400

############ TEACHERS/REMOVE/<int:id_teacher> ############
@teachers_bp.route('/teachers/remove/<int:id_teacher>', methods=['DELETE'])
def delete_teachers(id_teacher):
    try:
        if teacher_id_exists(id_teacher) :
            return jsonify({"error": f"id_teacher : '{id_teacher}' not exists"}) , 400
        id_user = get_user_id_with_id_teacher(id_teacher)
        if user_id_exists(id_user) :
            return jsonify({"error": f"id_user : '{id_user}' not exists"}) , 400

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.teachers WHERE id = %s"
        cursor.execute(query, (id_teacher,))
        conn.commit()
        conn.close()
        user_response, http_status = remove_users(id_user)
        return jsonify({"message": "Teacher deleted", "id": id_teacher}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

############ TEACHERS/GET/<int:id_teacher> ############
@teachers_bp.route('/teachers/<int:id_teacher>', methods=['GET', 'POST'])
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


#--------------------------------------------------FONCTION--------------------------------------------------#

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

############  RECUPERATION USER ID SELON ID_TEACHER  ################
def get_user_id_with_id_teacher(id_teacher):
    # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_teacher
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id_User FROM ent.teachers WHERE id = %s", (id_teacher,))
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