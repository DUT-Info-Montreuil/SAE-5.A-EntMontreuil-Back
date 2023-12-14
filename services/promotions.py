import psycopg2
import connect_pg
import pandas as pd
from entities.model.promotionsm import PromotionModel
from entities.DTO.promotions import Promotion
from entities.DTO.trainings import Training
from flask import jsonify
import datetime

class PromotionService:
    def __init__(self):
        pass

    # -------------------- Récupérer les informations d'une promotion --------------------------------------#
    def get_promotion_info(self, promotion_id, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer les informations de la promotion
                sql_query = """
                    SELECT P.id, P.year, P.level, D.id AS degree_id
                    FROM ent.Promotions P
                    INNER JOIN ent.Degrees D ON P.id_Degree = D.id
                    WHERE P.id = %s
                """

                cursor.execute(sql_query, (promotion_id,))
                row = cursor.fetchone()

                if row:
                    if output_format == "DTO":
                        promotion_info = Promotion(
                            id=row[0],
                            year=row[1],
                            level=row[2],
                            id_Degree=row[3]
                        )
                        return promotion_info.jsonify()
                    elif output_format == "model":
                        promotion_info = PromotionModel(
                            id=row[0],
                            year=row[1],
                            level=row[2],
                            id_Degree=row[3]
                        )
                        return promotion_info.jsonify()
                else:
                    return jsonify({"message": "Promotion non trouvée"}), 404
        except Exception as e:
            return jsonify({"message": f"Erreur lors de la récupération de la promotion : {str(e)}"}), 500
        finally:
            conn.close()

    # -------------------- Récupérer toutes les promotions --------------------------------------#
    def get_all_promotions(self, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer toutes les promotions
                sql_query = """
                    SELECT P.id, P.year, P.level, D.id AS degree_id , D.name AS degree_name
                    FROM ent.Promotions P
                    INNER JOIN ent.Degrees D ON P.id_Degree = D.id
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                promotions_list = []

                for row in rows:
                    if output_format == "DTO":
                        promotion = Promotion(
                            id=row[0],
                            year=row[1],
                            level=row[2],
                            id_Degree=row[3]
                        )
                        promotions_list.append(promotion.jsonify())
                    elif output_format == "model":
                        promotion = PromotionModel(
                            id=row[0],
                            year=row[1],
                            level=row[2],
                            id_Degree=row[3],
                            degree_name=row[4]
                        )
                        promotions_list.append(promotion.jsonify())

                return promotions_list
        except Exception as e:
            return jsonify({"message": f"Erreur lors de la récupération des promotions : {str(e)}"}), 500
        finally:
            conn.close()

    # -------------------- Ajouter une promotion --------------------------------------#
    def add_promotion(self, data):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Promotions (year, level, id_Degree) VALUES (%s, %s, %s) RETURNING id"
            values = (data["year"], data["level"], data["degree_id"])

            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_promotion_id = cursor.fetchone()[0]

            return jsonify({
                "message": f"Promotion ajoutée avec succès, ID : {inserted_promotion_id}"
            }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de l'ajout de la promotion : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Mettre à jour une promotion --------------------------------------#
    def update_promotion(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.Promotions SET year = %s, level = %s, id_Degree = %s WHERE id = %s RETURNING id",
                    (data["year"], data["level"], data["degree_id"], data["id"])
                )
                updated_promotion_id = cursor.fetchone()

                conn.commit()

                if updated_promotion_id:
                    return jsonify({
                        "message": f"Promotion mise à jour avec succès, ID : {updated_promotion_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Promotion non trouvée ou aucune modification effectuée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour de la promotion : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Supprimer une promotion --------------------------------------#
    def delete_promotion(self, promotion_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Promotions WHERE id = %s RETURNING id", (promotion_id,))
                deleted_promotion_id = cursor.fetchone()

                conn.commit()

                if deleted_promotion_id:
                    return jsonify({
                        "message": f"Promotion supprimée avec succès, ID : {deleted_promotion_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Promotion non trouvée ou déjà supprimée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression de la promotion : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Validation de l'année et récupération de l'entier correspondant ------------------#
    def validate_and_get_year(self, year_str):
        try:
            year_int = int(year_str)
            current_year = datetime.datetime.now().year

            if year_int < 2000 or year_int > current_year + 2:
                raise ValueError("L'année fournie n'est pas dans une plage valide")

            return year_int

        except ValueError:
            raise ValueError("L'année doit être un nombre")

 # -------------------- Créer un TD dans une promotion --------------------------------------#
    def create_td_in_promotion(self, promotion_id, td_name):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ent.TD (name, id_Promotion) VALUES (%s, %s) RETURNING id", (td_name, promotion_id))
                created_td_id = cursor.fetchone()

                conn.commit()

                if created_td_id:
                    return jsonify({
                        "message": f"TD '{td_name}' créé avec succès dans la promotion, ID : {created_td_id[0]}"
                    }), 201  # Code de statut 201 Created
                else:
                    return jsonify({"message": "Erreur lors de la création du TD"}), 500

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la création du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Créer un TP dans un TD --------------------------------------#
    def create_tp_in_td(self, td_id, tp_name):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ent.TP (name, id_Td) VALUES (%s, %s) RETURNING id", (tp_name, td_id))
                created_tp_id = cursor.fetchone()

                conn.commit()

                if created_tp_id:
                    return jsonify({
                        "message": f"TP '{tp_name}' créé avec succès dans le TD, ID : {created_tp_id[0]}"
                    }), 201  # Code de statut 201 Created
                else:
                    return jsonify({"message": "Erreur lors de la création du TP"}), 500

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la création du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Ajouter un étudiant dans une promotion, TD et TP --------------------------------------#
    def add_students_tp_td_promotion_from_csv(self, csv_path):
        conn = None
        try:
            # Charger le fichier CSV dans un DataFrame
            df = pd.read_csv(csv_path)

            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                for index, row in df.iterrows():
                    student_ine = str(row['ine'])
                    promotion_level = str(row['promotion'])
                    degree_name = str(row['degree'])
                    td_name = str(row['td'])
                    tp_name = str(row['tp'])

                    # Vérifier si l'étudiant existe
                    cursor.execute("SELECT id FROM ent.Students WHERE ine = %s", (student_ine,))
                    student_id = cursor.fetchone()

                    if not student_id:
                        return jsonify({"message": f"Étudiant avec INE {student_ine} non trouvé"}), 404
                    
                    # Vérifier si la promotion existe
                    cursor.execute("SELECT id FROM ent.Degrees WHERE name = %s", (degree_name,))
                    degree = cursor.fetchone()

                    if not degree:
                        return jsonify({"message": f"Degree {degree} non trouvée"}), 404

                    # Vérifier si la promotion existe
                    cursor.execute("SELECT id FROM ent.Promotions WHERE level = %s", (promotion_level,))
                    promotion_id = cursor.fetchone()

                    if not promotion_id:
                        return jsonify({"message": f"Promotion avec le niveau {promotion_level} non trouvée"}), 404

                    # Vérifier si le TD existe
                    cursor.execute("SELECT id FROM ent.TD WHERE name = %s AND id_Promotion = %s", (td_name, promotion_id))
                    td_id = cursor.fetchone()

                    if not td_id:
                        return jsonify({"message": f"TD avec le nom {td_name} non trouvé dans la promotion {promotion_level}"}), 404

                    # Vérifier si le TP existe
                    cursor.execute("SELECT id FROM ent.TP WHERE name = %s AND id_Td = %s", (tp_name, td_id))
                    tp_id = cursor.fetchone()

                    if not tp_id:
                        return jsonify({"message": f"TP avec le nom {tp_name} non trouvé dans le TD {td_name}"}), 404

                    # Ajouter l'étudiant à la promotion, TD et TP
                    cursor.execute("UPDATE ent.Students SET id_Promotion = %s, id_Td = %s, id_Tp = %s WHERE id = %s",
                                (promotion_id, td_id, tp_id, student_id))

            conn.commit()

            return jsonify({"message": "Étudiants ajoutés avec succès à la promotion, TD et TP"}), 200

        except Exception as e:
            return jsonify({"message": f"Erreur lors de l'ajout des étudiants à la promotion, TD et TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

     # -------------------- Retirer un étudiant de la promotion --------------------------------------#
    def remove_student_from_promotion(self, student_ine):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Vérifier si l'étudiant existe
                cursor.execute("SELECT id, id_Promotion, id_Td, id_Tp FROM ent.Students WHERE ine = %s", (student_ine,))
                student_data = cursor.fetchone()

                if not student_data:
                    return jsonify({"message": "Étudiant non trouvé"}), 404

                # Retirer l'étudiant de la promotion, du TD et du TP
                cursor.execute("UPDATE ent.Students SET id_Promotion = NULL, id_Td = NULL, id_Tp = NULL WHERE ine = %s", (student_ine,))

                conn.commit()

                return jsonify({
                    "message": f"Étudiant retiré avec succès de la promotion, TD et TP"
                }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors du retrait de l'étudiant de la promotion, TD et TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

     # -------------------- Retirer un étudiant d'un TD --------------------------------------#
    def remove_student_from_td(self, student_ine, td_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Vérifier si l'étudiant existe
                cursor.execute("SELECT id, id_Promotion, id_Td, id_Tp FROM ent.Students WHERE ine = %s", (student_ine,))
                student_data = cursor.fetchone()

                if not student_data:
                    return jsonify({"message": "Étudiant non trouvé"}), 404

                # Vérifier si l'étudiant est effectivement dans le TD spécifié
                if student_data[2] != td_id:
                    return jsonify({"message": "Étudiant non présent dans le TD spécifié"}), 400

                # Retirer l'étudiant du TD
                cursor.execute("UPDATE ent.Students SET id_Td = NULL WHERE ine = %s", (student_ine,))

                conn.commit()

                return jsonify({
                    "message": f"Étudiant retiré avec succès du TD, ID : {td_id}"
                }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors du retrait de l'étudiant du TD : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    # -------------------- Retirer un étudiant d'un TP --------------------------------------#
    def remove_student_from_tp(self, student_ine, tp_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Vérifier si l'étudiant existe
                cursor.execute("SELECT id, id_Promotion, id_Td, id_Tp FROM ent.Students WHERE ine = %s", (student_ine,))
                student_data = cursor.fetchone()

                if not student_data:
                    return jsonify({"message": "Étudiant non trouvé"}), 404

                # Vérifier si l'étudiant est effectivement dans le TP spécifié
                if student_data[3] != tp_id:
                    return jsonify({"message": "Étudiant non présent dans le TP spécifié"}), 400

                # Retirer l'étudiant du TP
                cursor.execute("UPDATE ent.Students SET id_Tp = NULL WHERE ine = %s", (student_ine,))

                conn.commit()

                return jsonify({
                    "message": f"Étudiant retiré avec succès du TP, ID : {tp_id}"
                }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors du retrait de l'étudiant du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)


    # -------------------- Récuperer les parcours d'une promo --------------------------------------#
    def get_training_of_promo(self, id_promo):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Vérifier si l'étudiant existe
                trainings = []
                cursor.execute("SELECT * FROM ent.Trainings WHERE id_Promotion = %s", (id_promo,))
                lis_tr = cursor.fetchall()
                for tr in lis_tr:
                    # Create instances of the Training class with data from the database
                    training = Training(id=tr[0], name=tr[1], id_Promotion=tr[2], semester=tr[3])
                    trainings.append(training)
                conn.commit()

                # Return a list of Training instances as JSON
                return jsonify({
                    "trainings": [training.jsonify() for training in trainings]
                }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors du retrait de l'étudiant du TP : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)