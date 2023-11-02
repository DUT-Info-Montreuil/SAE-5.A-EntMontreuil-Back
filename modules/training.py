from flask import request, jsonify, Blueprint
import psycopg2
import connect_pg
import json
import logging


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

   
        """    # Valide l'existence du diplôme référencé par 'id_Degree'
    if not does_entry_exist("Degrees",training_data["id_Degree"]):
        return jsonify({"message": "Le diplôme spécifié n'existe pas."}), 400"""

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
        # Ici, vous pouvez gérer les erreurs d'intégrité, comme un nom de parcours déjà existant
        return jsonify({"message": f"Erreur d'intégrité des données : {str(e)}"}), 409

    except Exception as e:
        # Gestion des autres erreurs
        return jsonify({"message": f"Erreur lors de l'ajout du parcours : {str(e)}"}), 500

    finally:
        # Nettoyage : fermeture de la connexion à la base de données
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