from flask import request, jsonify
from flask import request, jsonify, Blueprint
import psycopg2
import connect_pg
import json
import logging
import datetime

# Création  d'un Blueprint pour les routes liées aux promotions
training_bp = Blueprint('trainings', __name__)

# Configuration du journal pour enregistrer les messages d'erreur dans un fichier
logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

# Fonction utilitaire pour enregistrer les erreurs dans le journal


def log_error(message):
    logging.error(message)

@training_bp.route('/trainings/add', methods=['POST'])
def add_training():
    """
    Ajoute un nouveau parcours à la base de données.

    La fonction extrait les données de la requête, valide leur présence et leur format,
    puis insère le nouveau parcours dans la base de données. Les erreurs sont gérées
    et renvoyées sous forme de réponse JSON.
    """
    json_data = request.json

  
    # Vérifie la présence des données JSON et de la clé 'datas'
    if not json_data or 'datas' not in json_data:
        return jsonify({"message": "Données manquantes"}), 400

    training_data = json_data['datas']
   
    # Valide le nom du parcours et s'assure qu'il n'est pas vide
    if 'name' not in training_data or not training_data['name']:
        return jsonify({"message": "Le nom du parcours est requis"}), 400
    
    # Valide que le 'id_Degree' est présent et est un entier
    if 'id_Degree' not in training_data or not isinstance(training_data['id_Degree'], int):
        return jsonify({"message": "L'identifiant du diplôme doit être un entier"}), 400

   
    # Valide l'existence de la formation référencée par 'id_Degree'
    if not does_entry_exist("Degrees",training_data["id_Degree"]):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 400

    # Si les validations sont passées, procéder à l'insertion dans la base de données
    try:
        conn = connect_pg.connect()
        query = "INSERT INTO ent.Trainings (name, id_Degree) VALUES (%s, %s) RETURNING id"
        data = (training_data["name"], training_data["id_Degree"])

        with conn, conn.cursor() as cursor:
            cursor.execute(query, data)
            new_training_id = cursor.fetchone()[0]  # Récupère l'ID du parcours ajouté

        success_message = {
            "message": f"Le parcours '{training_data['name']}' a été ajouté avec succès.",
            "id": new_training_id
        }
        return jsonify(success_message), 201

    except psycopg2.IntegrityError as e:
        # Gère la violation de la contrainte unique pour la combinaison de id_Degree et name
        if 'trainings_id_degree_name_key' in str(e):
            return jsonify({"message": "Un parcours avec le même nom existe déjà pour ce diplôme."}), 409
        
    except Exception as e:
        # Gestion des autres erreurs
        return jsonify({"message": f"Erreur lors de l'ajout du parcours : {str(e)}"}), 500

    finally:
        # Nettoyage : fermeture de la connexion à la base de données
        connect_pg.disconnect(conn)


@training_bp.route('/trainings/get/<int:id_Training>', methods=['GET'])
def get_training(id_Training):
    """
    Récupère les détails d'un parcours spécifique par son ID.

    :param id_Training: L'identifiant du parcours à récupérer.
    :return: Un objet JSON contenant les détails du parcours ou un message d'erreur.
    """
    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ent.Trainings WHERE id = %s", (id_Training,))
            row = cursor.fetchone()
            if row:
                parcours = {
                    "id": row[0],
                    "name": row[1],
                    "id_Degree": row[2]
                }
                return jsonify(parcours), 200
            else:
                return jsonify({"message": "Parcours non trouvé"}), 404
    except psycopg2.Error as e:
        log_error(f"Erreur lors de la récupération du parcours: {e}")
        return jsonify({"message": "Erreur lors de la récupération des informations du parcours"}), 500
    finally:
        if conn:
            connect_pg.disconnect(conn)


        
@training_bp.route('/degrees/get', methods=['GET'])
def get_degrees():
    """ Return all ent.egrees in JSON format """
    query = "SELECT * FROM ent.Degrees"
    conn = connect_pg.connect()
    cur = conn.cursor()
    cur.execute(query)
    degrees = []

    for row in cur.fetchall():
        degree = {
            "id": row[0],
            "name": row[1]
        }
        degrees.append(degree)

    cur.close()
    connect_pg.disconnect(conn)

    return jsonify(degrees)

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