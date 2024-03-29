import psycopg2
import connect_pg
from flask import jsonify

class TPService:
    # -------------------- Récupérer un TP par ID --------------------------------------#
    def get_tp_by_id(self, tp_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer les informations du TP
                sql_query = """
                    SELECT id, name, id_Td
                    FROM ent.TP
                    WHERE id = %s
                """

                cursor.execute(sql_query, (tp_id,))
                row = cursor.fetchone()

                if row:
                    tp_info = {
                        "id": row[0],
                        "name": row[1],
                        "id_Td": row[2]
                    }
                    return jsonify(tp_info), 200
                else:
                    return jsonify({"message": "TP non trouvé"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Récupérer tous les TPs --------------------------------------#
    def get_all_tps(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer tous les TPs
                sql_query = """
                    SELECT id, name, id_Td
                    FROM ent.TP
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                tps_list = []

                for row in rows:
                    tp = {
                        "id": row[0],
                        "name": row[1],
                        "id_Td": row[2]
                    }
                    tps_list.append(tp)

                return jsonify(tps_list), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la récupération des TPs : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Mettre à jour un TP --------------------------------------#
    def update_tp(self, tp_id, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.TP SET name = %s WHERE id = %s RETURNING id",
                    (data["name"], tp_id)
                )
                updated_tp_id = cursor.fetchone()

                conn.commit()

                if updated_tp_id:
                    return jsonify({
                        "message": f"TP mis à jour avec succès, ID : {updated_tp_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "TP non trouvé ou aucune modification effectuée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Supprimer un TP --------------------------------------#
    def delete_tp(self, tp_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Mettre à jour les étudiants en définissant id_tp à NULL
                cursor.execute("UPDATE ent.students SET id_tp = NULL, id_td = NULL WHERE id_tp = %s", (tp_id,))

                # Supprimer le TP
                cursor.execute("DELETE FROM ent.tp WHERE id = %s RETURNING id", (tp_id,))
                deleted_tp_id = cursor.fetchone()

                conn.commit()

            if deleted_tp_id:
                return jsonify({
                    "message": f"TP supprimé avec succès, ID : {deleted_tp_id[0]}"
                }), 200
            else:
                return jsonify({"message": "TP non trouvé ou déjà supprimé"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

       # -------------------- Ajouter un TP --------------------------------------#
    def add_tp(self, data):
        try:
            conn = connect_pg.connect()
            
            if not connect_pg.does_entry_exist('TD', data["id_td"]) :
                return jsonify({"error": f"L'id td {data.get('id_td')} n'existe pas"}), 400 
            
                
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ent.TP (name, id_Td) VALUES (%s,%s) RETURNING id" , (data["name"], data["id_td"]))
                id = cursor.fetchone()[0]
                conn.commit()
                if id :
                    return jsonify({
                        "message": f"TP ajouté avec succès, ID : {id}"
                    }), 200
                else:
                    return jsonify({"error": "Erreur lors de l'ajout du TP"}), 400

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Ajouter students à TP --------------------------------------#
    def add_students_to_tp(self, tp_id, student_ids):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Trouver l'identifiant du TD associé et la promotion liée
                cursor.execute("""
                    SELECT td.id, td.id_promotion 
                    FROM ent.TP tp 
                    JOIN ent.TD td ON tp.id_td = td.id 
                    WHERE tp.id = %s
                """, (tp_id,))
                td_info = cursor.fetchone()
                if not td_info:
                    return jsonify({"error": "TP ou TD associé non trouvé"}), 404

                td_id, promotion_id = td_info

                # Mettre à jour les étudiants
                for student_id in student_ids:
                    cursor.execute("""
                        UPDATE ent.Students 
                        SET id_tp = %s, id_td = %s, id_promotion = %s 
                        WHERE id = %s
                    """, (tp_id, td_id, promotion_id, student_id))

                conn.commit()
                return jsonify({"message": "Étudiants ajoutés avec succès au TP, au TD associé et à la promotion"}), 200

        except psycopg2.Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)
                
    # -------------------- Supprimer students à TP --------------------------------------#
    def remove_student_from_tp_td_promotion(self, student_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Mettre à jour l'étudiant en définissant les champs à NULL
                cursor.execute("""
                    UPDATE ent.Students 
                    SET id_tp = NULL, id_td = NULL, id_promotion = NULL 
                    WHERE id = %s
                """, (student_id,))

                conn.commit()
                return jsonify({"message": "Étudiant retiré du TP, TD et promotion avec succès"}), 200

        except psycopg2.Error as e:
            return jsonify({"error": str(e)}), 500
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