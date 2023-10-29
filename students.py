from flask import request, jsonify, Blueprint
import json
import connect_pg
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
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status 
        else :
            user_id = user_response.json.get("id")
            student_data = {
                "apprentice": False,
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
            return jsonify({"message": "Student added", "id": row[0]}) , 200  
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