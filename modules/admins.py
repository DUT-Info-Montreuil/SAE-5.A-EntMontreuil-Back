from flask import jsonify, Blueprint
import json
import connect_pg

admins_bp = Blueprint('admins', __name__)


#--------------------------------------------------ROUTE--------------------------------------------------#

############ ADMINS/GET ############
@admins_bp.route('/admins', methods=['GET','POST'])
def get_admins():
    """ Return all admins in JSON format """
    query = "select * from ent.admins order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_admin_statement(row))
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

############ ADMINS/GET/<int:id_admin> ############
@admins_bp.route('/admins/<int:id_admin>', methods=['GET', 'POST'])
def get_admin(id_admin):
    try:
        # Verification id admin existe
        if admin_id_exists(id_admin) :
            return jsonify({"error": f"id_admin : '{id_admin}' not exists"}) , 400
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM ent.admins WHERE id = %s"
        cursor.execute(query, (id_admin,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return get_admin_statement(row)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400



#--------------------------------------------------FONCTION--------------------------------------------------#

def admin_id_exists(id_admin) :
    # Fonction pour verifier si l'id d'un admin n'existe pas dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.admins WHERE id = %s", (id_admin,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0