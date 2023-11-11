from flask import request, jsonify, Blueprint
import psycopg2
import connect_pg
import logging
from DTO.absences import Absences

# Création d'un Blueprint pour les routes liées aux absences
absences_bp = Blueprint('absences', __name__)

# Configuration du journal pour enregistrer les messages d'erreur dans un fichier
logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

# Fonction utilitaire pour enregistrer les erreurs dans le journal
def log_error(message):
    logging.error(message)

@absences_bp.route('/absences/user/<int:id_user>', methods=['GET'])
def get_user_absences(id_user):
    if not does_entry_exist("Students", id_user):
            return jsonify({"message": "L'utilisateur spécifié n'existe pas."}), 404
    try:
                # Vérifie que l'utilisateur spécifié par 'id_user' existe
      
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ent.Absences WHERE id_Student = %s", (id_user,))
            rows = cursor.fetchall()
            absences = [Absences(row[0], row[1], row[2], row[3]) for row in rows]
            return jsonify([absence.jsonify() for absence in absences]), 200

    except psycopg2.Error as e:
        log_error(f"Erreur lors de la récupération des absences : {e}")
        return jsonify({"message": "Erreur lors de la récupération des absences"}), 500

    finally:
        if conn:
            connect_pg.disconnect(conn)

@absences_bp.route('/absences/user/<int:id_user>/course/<int:id_course>', methods=['PUT'])
def update_user_course_absence(id_user, id_course):
    json_data = request.json
    if not json_data or 'datas' not in json_data:
        return jsonify({"message": "Données manquantes"}), 400

    absence_data = json_data['datas']
    if 'reason' not in absence_data or 'justify' not in absence_data:
        return jsonify({"message": "Les raisons et les justifications sont requises"}), 400

    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE ent.Absences SET reason = %s, justify = %s WHERE id_Student = %s AND id_Course = %s RETURNING id_Student, id_Course",
                (absence_data["reason"], absence_data["justify"], id_user, id_course)
            )
            updated_row = cursor.fetchone()
            conn.commit()

            if updated_row:
                return jsonify({"message": f"Absence mise à jour pour l'utilisateur {updated_row[0]} et le cours {updated_row[1]}"})
            else:
                return jsonify({"message": "Absence non trouvée ou aucune modification effectuée"}), 404

    except psycopg2.Error as e:
        log_error(f"Erreur lors de la mise à jour de l'absence : {e}")
        return jsonify({"message": "Erreur lors de la mise à jour de l'absence"}), 500

    finally:
        if conn:
            connect_pg.disconnect(conn)


@absences_bp.route('/absences/user/<int:id_user>/course/<int:id_course>/add', methods=['POST'])
def add_user_course_absence(id_user, id_course):
    try:
        json_data = request.json

        # Vérifie la présence des données JSON et de la clé 'datas'
        if not json_data or 'datas' not in json_data:
            return jsonify({"message": "Données manquantes"}), 400

        absence_data = json_data['datas']

        # Valide la présence des champs obligatoires dans les données JSON
        required_fields = ['reason', 'justify']
        for field in required_fields:
            if field not in absence_data:
                return jsonify({"message": f"Le champ '{field}' est requis"}), 400

        # Vérifie que l'utilisateur spécifié par 'id_user' existe
        if not does_entry_exist("Students", id_user):
            return jsonify({"message": "L'utilisateur spécifié n'existe pas."}), 400

        # Vérifie que le cours spécifié par 'id_course' existe
        if not does_entry_exist("Courses", id_course):
            return jsonify({"message": "Le cours spécifié n'existe pas."}), 400

        # Insère l'absence dans la base de données
        conn = connect_pg.connect()
        query = "INSERT INTO ent.Absences (id_Student, id_Course, reason, justify) VALUES (%s, %s, %s, %s) RETURNING id_Student, id_Course"
        data = (id_user, id_course, absence_data["reason"], absence_data["justify"])

        with conn, conn.cursor() as cursor:
            cursor.execute(query, data)
            inserted_user_id, inserted_course_id = cursor.fetchone()

        success_message = {
            "message": f"Absence ajoutée avec succès pour l'utilisateur {inserted_user_id} lors du cours {inserted_course_id}"
        }
        return jsonify(success_message), 201

    except psycopg2.Error as e:
        log_error(f"Erreur lors de l'ajout de l'absence : {e}")
        return jsonify({"message": "Erreur lors de l'ajout de l'absence"}), 500

    finally:
        if conn:
            connect_pg.disconnect(conn)
            

@absences_bp.route('/absences/user/<int:id_user>/course/<int:id_course>', methods=['DELETE'])
def delete_user_course_absence(id_user, id_course):
    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM ent.Absences WHERE id_Student = %s AND id_Course = %s RETURNING id_Student, id_Course", (id_user, id_course))
            deleted_row = cursor.fetchone()
            conn.commit()

            if deleted_row:
                return jsonify({"message": f"Absence supprimée pour l'utilisateur {deleted_row[0]} et le cours {deleted_row[1]}"})
            else:
                return jsonify({"message": "Absence non trouvée ou déjà supprimée"}), 404

    except psycopg2.Error as e:
        log_error(f"Erreur lors de la suppression de l'absence : {e}")
        return jsonify({"message": "Erreur lors de la suppression de l'absence"}), 500

    finally:
        if conn:
            connect_pg.disconnect(conn)

def does_entry_exist(table_name, entry_id):
    """
    Vérifie si une entrée existe dans la table spécifiée en fonction de son ID.

    :param table_name: Le nom de la table dans laquelle effectuer la vérification.
    :param entry_id: L'identifiant de l'entrée à vérifier.
    :return: True si l'entrée existe, False autrement.
    """
    valid_tables = ['Users', 'Admin', 'Teachers', 'Degrees', 'Trainings', 'Promotions', 'Resources',
                    'TD', 'TP', 'Materials', 'Classroom', 'Courses', 'Students', 'Absences', 'Historique']
    if table_name not in valid_tables:
        raise ValueError(f"Invalid table name: {table_name}")

    conn = None
    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            # La table est maintenant vérifiée et sécurisée contre les injections SQL.
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM ent.{} WHERE id = %s)".format(table_name), (entry_id,))
            return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(
            f"Erreur lors de la vérification de l'existence de l'entrée: {e}")
        return False
    finally:
        if conn:
            connect_pg.disconnect(conn)