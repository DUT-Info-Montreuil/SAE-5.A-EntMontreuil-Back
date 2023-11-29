import psycopg2
import connect_pg
from flask import jsonify

class ResourceService:
    def __init__(self):
        pass

    # -------------------- Ajouter une ressource --------------------------------------#
    def add_resource(self, data):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Resources (name, id_Promotion) VALUES (%s, %s) RETURNING id"
            values = (data["name"], data["id_Promotion"])

            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_resource_id = cursor.fetchone()[0]

            return jsonify({
                "message": f"Ressource ajoutée avec succès, ID : {inserted_resource_id}"
            }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de l'ajout de la ressource : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Supprimer une ressource --------------------------------------#
    def delete_resource(self, resource_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Resources WHERE id = %s RETURNING id", (resource_id,))
                deleted_resource_id = cursor.fetchone()

                conn.commit()

                if deleted_resource_id:
                    return jsonify({
                        "message": f"Ressource supprimée avec succès, ID : {deleted_resource_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Ressource non trouvée ou déjà supprimée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression de la ressource : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Mettre à jour une ressource --------------------------------------#
    def update_resource(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.Resources SET name = %s, id_Promotion = %s WHERE id = %s RETURNING id",
                    (data["name"], data["id_Promotion"], data["id"])
                )
                updated_resource_id = cursor.fetchone()

                conn.commit()

                if updated_resource_id:
                    return jsonify({
                        "message": f"Ressource mise à jour avec succès, ID : {updated_resource_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Ressource non trouvée ou aucune modification effectuée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour de la ressource : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Récupérer les informations d'une ressource --------------------------------------#
    def get_resource_by_id(self, resource_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer les informations de la ressource
                sql_query = """
                    SELECT R.id, R.name, R.id_Promotion
                    FROM ent.Resources R
                    WHERE R.id = %s
                """

                cursor.execute(sql_query, (resource_id,))
                row = cursor.fetchone()

                if row:
                    resource_info = {
                        "id": row[0],
                        "name": row[1],
                        "id_Promotion": row[2]
                    }
                    return jsonify(resource_info), 200
                else:
                    return jsonify({"message": "Ressource non trouvée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération de la ressource : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Récupérer toutes les ressources --------------------------------------#
    def get_all_resources(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer toutes les ressources
                sql_query = """
                    SELECT R.id, R.name, R.id_Promotion
                    FROM ent.Resources R
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                resources_list = []

                for row in rows:
                    resource = {
                        "id": row[0],
                        "name": row[1],
                        "id_Promotion": row[2]
                    }
                    resources_list.append(resource)

                return jsonify(resources_list), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération des ressources : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)