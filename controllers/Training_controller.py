from flask import request, jsonify, Blueprint
from services.training import TrainingService  # Importer le service de gestion des parcours
import connect_pg
# Création d'un Blueprint pour les routes liées aux parcours
training_bp = Blueprint('trainings', __name__)


training_service = TrainingService()

#---------------- récuperer tout les trainings -------------------#
@training_bp.route('/trainings', methods=['GET'])
def get_all_trainings():
    output_format = request.args.get('output_format', default='DTO', type=str)
    trainings = training_service.get_all_trainings(output_format)
    return jsonify(trainings), 200

#--------------------ajouter  un  parcours--------------------------------------#
@training_bp.route('/trainings/add', methods=['POST'])
def add_training():
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

        if not connect_pg.does_entry_exist("Degrees", training_data['id_Degree']):
            return jsonify({"message": "La formation spécifiée n'existe pas."}), 400

        data = {
            "name": training_data["name"],
            "id_Degree": training_data["id_Degree"]
        }

        message = training_service.add_training(data)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@training_bp.route('/trainings/get/<int:id_training>', methods=['GET'])
def get_training(id_training):
    """
    Récupère les détails d'un parcours spécifique par son ID.
    """
    try:
        result, status_code = training_service.get_training(id_training)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération du parcours : {str(e)}"}), 500

@training_bp.route('/trainings/update/<int:id_training>', methods=['PUT'])
def update_training(id_training):
    """
    Met à jour un parcours existant dans la base de données par son ID.
    """
    try:
        result, status_code = training_service.update_training(id_training, request.json)
        return jsonify(result), status_code
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
