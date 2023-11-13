from flask import request, jsonify, Blueprint
from services.training import TrainingService  # Importer le service de gestion des parcours
import connect_pg

from entities.DTO.trainings import Training
# Création d'un Blueprint pour les routes liées aux parcours
training_bp = Blueprint('trainings', __name__)


training_service = TrainingService()

#---------------- récuperer tout les trainings -------------------#
@training_bp.route('/trainings', methods=['GET'])
def get_all_trainings():
    """
    Récupère tous les parcours en fonction du format de sortie spécifié.

    Cette route permet de récupérer la liste de tous les parcours disponibles. Vous pouvez spécifier le format de
    sortie en utilisant le paramètre 'output_format' avec les valeurs possibles 'DTO' (par défaut) ou 'model'.

    Vous pouvez également filtrer les résultats en spécifiant l'identifiant de la formation ('id_degree') pour
    récupérer uniquement les parcours associés à une formation particulière.

    :return: Une liste de parcours au format spécifié (DTO ou model).
    :rtype: list
    :raises: 500 (Internal Server Error) en cas d'erreur lors de la récupération des données.
    """
    try:
        output_format = request.args.get('output_format', default='DTO', type=str)
        id_Degree = request.args.get('id_Degree', default=None, type=int)  # Ajout de la récupération de id_degree

        # Appel de la fonction get_all_trainings avec ou sans id_degree en fonction de sa présence
        if id_Degree is not None:
            trainings = training_service.get_all_trainings(output_format, id_Degree=id_Degree)
        else:
            trainings = training_service.get_all_trainings(output_format)

        return jsonify(trainings), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({"message": str(e)}), 500


#--------------------ajouter  un  parcours--------------------------------------#
@training_bp.route('/trainings/add', methods=['POST'])
def add_training():
    """
    Ajoute un nouveau parcours à la base de données.

    La fonction extrait les données de la requête, valide leur présence et leur format,
    puis insère le nouveau parcours dans la base de données. Les erreurs sont gérées
    et renvoyées sous forme de réponse JSON.

    :return: Un message de confirmation ou un message d'erreur.
    :rtype: dict
    """
    try:
        json_data = request.json

        # Vérifie la présence des données JSON et de la clé 'datas'
        if not json_data or 'datas' not in json_data:
            return jsonify({"message": "Données manquantes"}), 400


        training_data = json_data['datas']

        # Valide la présence des champs obligatoires dans les données JSON
        required_fields = ['name', 'id_Degree']
        for field in required_fields:
            if field not in training_data:
                return jsonify({"message": f"Le champ '{field}' est requis"}), 400
        # Valide le nom du parcours et s'assure qu'il n'est pas vide
        if 'name' not in training_data or not training_data['name']:
          return jsonify({"message": "Le nom du parcours est requis"}), 400
        
        if 'id_Degree' not in training_data or not isinstance(training_data['id_Degree'], int):
            return jsonify({"message": "L'identifiant du diplôme doit être un entier"}), 400
        # Valide que la formation spécifiée existe
        if not connect_pg.does_entry_exist("Degrees", training_data['id_Degree']):
            return jsonify({"message": "La formation spécifiée n'existe pas."}), 400

        # Crée un objet Training (DTO) à partir des données JSON
        training = Training(
            id=0,
            name=training_data["name"],
            id_Degree=training_data["id_Degree"]
        )

        # Appelle le service pour ajouter la formation
        message = training_service.add_training(training)

        # Retourne un message de confirmation
        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    
#-------------------- Récuperer un parcours via son id ----------------------#
@training_bp.route('/trainings/get/<int:id_training>', methods=['GET'])
def get_training(id_training):
    """
    Récupère les détails d'un parcours spécifique par son ID.
    """

    if not connect_pg.does_entry_exist("Trainings", id_training):
        return jsonify({"message": "Le parcours spécifié n'existe pas."}), 404
    try:
        output_format = request.args.get('output_format',default='model', type=str)
        training = training_service.get_training(id_training,output_format)
        return jsonify(training), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération du parcours : {str(e)}"}), 500


@training_bp.route('/trainings/update/<int:id_training>', methods=['PUT'])
def update_training(id_training):
    """
    Met à jour un parcours existant dans la base de données par son ID.

    Cette route permet de mettre à jour les informations d'un parcours en spécifiant son ID.

    Args:
        id_training (int): L'identifiant unique du parcours à mettre à jour.

    Returns:
        tuple: Un tuple contenant un message de résultat et un code d'état HTTP.

    Raises:
        Exception: En cas d'erreur lors de la mise à jour du parcours.

    Example:
        Pour mettre à jour un parcours avec l'ID 1, envoyez une requête PUT avec les nouvelles données au format DTO.
    """
    try:
        json_data = request.json

        # Vérifie la présence des données JSON et de la clé 'datas'
        if not json_data or 'datas' not in json_data:
            return jsonify({"message": "Données manquantes"}), 400

        if not connect_pg.does_entry_exist("Trainings", id_training):
            return jsonify({"message": "Le parcours spécifié n'existe pas."}), 404
        training_data = json_data['datas']
        # Crée un objet Training DTO à partir des données JSON
        training = Training(
            id=id_training,
            name=training_data['name'],
            id_Degree=training_data['id_Degree']
        )
        message= training_service.update_training(training)
        return jsonify(message)
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour du parcours : {str(e)}"}), 500


@training_bp.route('/trainings/delete/<int:id_training>', methods=['DELETE'])
def delete_training(id_training):
    """
    Supprime un parcours existant de la base de données par son ID.
    """
    try:
        result, status_code = training_service.delete_training(id_training)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression du parcours : {str(e)}"}), 500
