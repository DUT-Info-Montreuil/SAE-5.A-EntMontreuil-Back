import psycopg2
import connect_pg
from flask import jsonify
from entities.DTO.tp import TP

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


 # -------------------- Récupérer tous les TDs par id_training -------------------#
    def get_tds_by_training_id(self, id_training):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer tous les TDs liés à un id_training spécifique
                sql_query = """
                    SELECT id, name, id_Promotion
                    FROM ent.TD
                    WHERE id_Training = %s
                """

                cursor.execute(sql_query, (id_training,))
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
                # Mettre à jour les étudiants en définissant id_td et id_tp à NULL
                cursor.execute("UPDATE ent.students SET id_td = NULL, id_tp = NULL WHERE id_td = %s", (td_id,))

                # Supprimer les TP associés au TD
                cursor.execute("DELETE FROM ent.tp WHERE id_td = %s", (td_id,))

                # Supprimer le TD
                cursor.execute("DELETE FROM ent.td WHERE id = %s RETURNING id", (td_id,))
                deleted_td_id = cursor.fetchone()

                conn.commit()

                if deleted_td_id:
                    return jsonify({ "message": f"TD supprimé avec succès, ID : {deleted_td_id[0]}"}), 200
                else:
                    return jsonify({"message": "TD non trouvé ou déjà supprimé"}), 404
        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TD : {str(e)}"}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)
                
        # -------------------- Ajouter un TD --------------------------------------#
    def add_td(self, data):
        try:
            conn = connect_pg.connect()
            
            if not connect_pg.does_entry_exist('Promotions', data["id_promotion"]) :
                return jsonify({"error": f"L'id promotion {data.get('id_promotion')} n'existe pas"}), 400 
            
            if not connect_pg.does_entry_exist('Trainings', data["id_training"]) :
                return jsonify({"error": f"L'id training {data.get('id_promotion')} n'existe pas"}), 400 
                
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ent.TD (name, id_Training, id_Promotion) VALUES (%s,%s,%s) RETURNING id" , (data["name"], data["id_training"], data["id_promotion"]))
                id = cursor.fetchone()[0]
                conn.commit()
                if id :
                    return jsonify({
                        "message": f"TD ajouté avec succès, ID : {id}"
                    }), 200
                else:
                    return jsonify({"error": "Erreur lors de l'ajout du TD"}), 400

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)
                
    # -------------------- Get td by tp--------------------------------------#       
    def get_tp_by_td(self, id_td):
        try:
            conn = connect_pg.connect()
            if not connect_pg.does_entry_exist('TD', id_td) :
                return jsonify({"error": f"L'id td {id_td} n'existe pas"}), 400 
                
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, id_td FROM ent.TP Where id_Td = %s" , (id_td,))
                rows = cursor.fetchall()
                tp_list = []
                for row in rows :
                    tp = TP(id=row[0], name=row[1], id_Td=row[2]).jsonify()
                    tp_list.append(tp)
                return jsonify(tp_list), 200
        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)
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