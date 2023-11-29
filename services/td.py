import psycopg2
import connect_pg
from flask import jsonify

class TDService:
    # -------------------- Récupérer un TD par ID --------------------------------------#
    def get_td_by_id(self, td_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer les informations du TD
                sql_query = """
                    SELECT id, name, id_Promotion
                    FROM ent.TD
                    WHERE id = %s
                """

                cursor.execute(sql_query, (td_id,))
                row = cursor.fetchone()

                if row:
                    td_info = {
                        "id": row[0],
                        "name": row[1],
                        "id_Promotion": row[2]
                    }
                    return jsonify(td_info), 200
                else:
                    return jsonify({"message": "TD non trouvé"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Récupérer tous les TDs --------------------------------------#
    def get_all_tds(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer tous les TDs
                sql_query = """
                    SELECT id, name, id_Promotion
                    FROM ent.TD
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                tds_list = []

                for row in rows:
                    td = {
                        "id": row[0],
                        "name": row[1],
                        "id_Promotion": row[2]
                    }
                    tds_list.append(td)

                return jsonify(tds_list), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération des TDs : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Mettre à jour un TD --------------------------------------#
    def update_td(self, td_id, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.TD SET name = %s, id_Promotion = %s WHERE id = %s RETURNING id",
                    (data["name"], data["id_Promotion"], td_id)
                )
                updated_td_id = cursor.fetchone()

                conn.commit()

                if updated_td_id:
                    return jsonify({
                        "message": f"TD mis à jour avec succès, ID : {updated_td_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "TD non trouvé ou aucune modification effectuée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Supprimer un TD --------------------------------------#
    def delete_td(self, td_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.TD WHERE id = %s RETURNING id", (td_id,))
                deleted_td_id = cursor.fetchone()

                conn.commit()

                if deleted_td_id:
                    return jsonify({
                        "message": f"TD supprimé avec succès, ID : {deleted_td_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "TD non trouvé ou déjà supprimé"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)