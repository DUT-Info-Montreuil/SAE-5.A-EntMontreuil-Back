from flask import jsonify, Blueprint, request
import json
import connect_pg
from modules.users import *

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


############ ADMINS/ADD ############
@admins_bp.route('/admins/add', methods=['POST'])
def add_admins():
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
        user_data["type"] = "admin"
        user_response, http_status = add_users(user_data)  # Appel de la fonction add_users
        # Si la requette user_add reussi
        if http_status != 200 :
            return user_response, http_status
        else :
            #on recupere le password de l'utilisateur ajouter pour savoir quel est sont mdp si il est generer aleatoirement
            password = user_response.json.get("password")
            # Recuperation du user id
            user_id = user_response.json.get("id")
            # Creation du admin data json
            admin_data = {
                "id_User" : user_id
            }
            # Si id est present
            if "id" in data :
                # Verification si id existe deja
                if admin_id_exists(data["id"]) :
                    return jsonify({"error": f"Id for admin '{data.get('id')}' already exist"}), 400
                else :
                    admin_data["id"] = data["id"]
            columns = list(admin_data.keys())
            values = list(admin_data.values())
            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            # Créez la requête SQL parametree
            query = f"INSERT INTO ent.admins ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
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
            return jsonify({"message": "Admin added","id" : row[0] ,  "json" : json_response}) , 200  
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}) , 400



############ ADMINS/REMOVE/<int:id_admin> ############
@admins_bp.route('/admins/remove/<int:id_admin>', methods=['DELETE'])
def delete_admin(id_admin):
    try:
        # Si id admin n'existe pas
        if admin_id_exists(id_admin) :
            return jsonify({"error": f"id_admin : '{id_admin}' not exists"}) , 400
        # Recuperation de l'id du user associer a l'admin
        id_user = get_user_id_with_id_admin(id_admin)

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.admins WHERE id = %s"
        cursor.execute(query, (id_admin,))
        conn.commit()
        conn.close()
        user_response, http_status = remove_users(id_user)
        return jsonify({"message": "Admin deleted", "id": id_admin}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

#--------------------------------------------------FONCTION--------------------------------------------------#

############ VERIFICATION ADMIN ID ############
def admin_id_exists(id_admin) :
    # Fonction pour verifier si l'id d'un admin n'existe pas dans la base de donnees
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.admins WHERE id = %s", (id_admin,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

############ RECUPERATION ID USER WITH ID ADMIN ############
def get_user_id_with_id_admin(id_admin):
    # Fonction pour recuperer l'id d'un utilisateur dans la base de donnees selon l'id_student
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id_User FROM ent.admins WHERE id = %s", (id_admin,))
    id_user = cursor.fetchone()[0]
    conn.close()
    return id_user