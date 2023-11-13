from flask import jsonify, request
import json
import connect_pg

from entities.DTO.admins import Admins
from entities.model.adminsm import AdminModel
from services.users import UsersFonction




class AdminsService :
    def __init__ (self):
        pass

    ############ ADMINS/GET ############
    def get_all_admins(self , output_format):
        """ Return all admins in JSON format """
        query = "select * from ent.admins a inner join ent.users u on a.id_User = u.id order by a.id asc"
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        admins = []
        for row in rows:
            if output_format == 'DTO' :
                admin = Admins(row[0] , row[1])
            if output_format == 'model' :
                admin = AdminModel(row[0] , row[1] ,row[3] ,row[5] ,row[6] ,row[7] ,row[8])
            admins.append(admin.jsonify())
        connect_pg.disconnect(conn)
        return jsonify(admins)

    ############ ADMINS/GET/<int:id_admin> ############
    def get_admin(self, id_admin, output_format):
        # Verification id admin existe
        if AdminsFonctions.admin_id_exists(id_admin) :
            raise ValidationError(f"id_admin : '{id_admin}' not exists")
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select * from ent.admins a inner join ent.users u on a.id_User = u.id WHERE a.id = %s"
        cursor.execute(query, (id_admin,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        if output_format == 'DTO' :
            admin = Admins(row[0] , row[1])
        if output_format == 'model' :
            admin = AdminModel(row[0] , row[1] ,row[3] ,row[5] ,row[6] ,row[7] ,row[8])
        return admin.jsonify()



    ############ ADMINS/ADD ############
    def add_admins(self, datas):

        # Si il manque datas renvoie une erreur
        if "datas" not in datas:
            raise ValidationError("Missing 'datas' field in JSON")
        data = datas["datas"]
        # Si il manque user renvoie une erreur
        if "user" not in data:
            raise ValidationError("Missing 'user' field in JSON")
        user_data = data["user"]
        user_data["type"] = "admin"
        user_response, http_status = UsersFonction.add_users(user_data)  # Appel de la fonction add_users
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
                if AdminsFonctions.admin_id_exists(data["id"]) :
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



    ############ ADMINS/REMOVE/<int:id_admin> ############
    def delete_admin(self , id_admin):
        # Si id admin n'existe pas
        if AdminsFonctions.admin_id_exists(id_admin) :
            raise ValidationError(f"id_admin : '{id_admin}' not exists")
        # Recuperation de l'id du user associer a l'admin
        id_user = AdminsFonctions.get_user_id_with_id_admin(id_admin)

        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "DELETE FROM ent.admins WHERE id = %s"
        cursor.execute(query, (id_admin,))
        conn.commit()
        conn.close()
        user_response, http_status = UsersFonction.remove_users(id_user)
        return jsonify({"message": "Admin deleted", "id": id_admin}), 200
        
        
    ############ ADMINS/UPDATE/<int:id_admin> ############
    def update_admins(self, id_admin, data):

        if data is None:
            raise ValidationError("Request data is empty")

        # Check if 'datas' field exists
        if "datas" not in data:
            raise ValidationError("Missing 'datas' field in JSON")

        admins_data = data["datas"]

        # Check if 'id' field is present in admins_data
        if "id" in admins_data:
            raise ValidationError("Unable to modify user id, remove id field")

        # Check if 'user' field exists in admins_data
        if "user" in admins_data:
            user_data = admins_data["user"]

            # Check if user data is empty
            if not user_data:
                raise ValidationError("Empty 'user' field in JSON")

            # Get user id associated with the admin
            if AdminsFonctions.admin_id_exists(id_admin) :
                raise ValidationError(f"id admin {id_admin} not exists") 
            else :
                id_user = AdminsFonctions.get_user_id_with_id_admin(id_admin)
            
            if id_user is None:
                raise ValidationError(f"No user found for admin with id {id_admin}")

            user_response, http_status = UsersFonction.update_users(user_data, id_user)
            # If user update fails
            if http_status != 200:
                return user_response, http_status
            else:
                return jsonify({"message": "Admin update", "id": id_admin}), 200
        else:
            raise ValidationError("Missing 'user' field in 'datas'")




#--------------------------------------------------FONCTION--------------------------------------------------#

class AdminsFonctions :
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
        id_user = cursor.fetchone()
        conn.close()
        return id_user[0]
    
#----------------------------------ERROR-------------------------------------
class ValidationError(Exception) :
    pass