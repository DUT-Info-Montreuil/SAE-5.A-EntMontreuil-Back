from flask import jsonify, Blueprint
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
def get_user_id_with_id_students(id_students):
    # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_students
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id_User FROM ent.students WHERE id = %s", (id_students,))
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