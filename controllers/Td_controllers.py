from flask import Blueprint, jsonify, request
from services.td import TDService

td_bp = Blueprint('td_bp', __name__)
td_service = TDService()

# -------------------- Récupérer un TD par ID --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['GET'])
def get_td_by_id(td_id):
    return td_service.get_td_by_id(td_id)



# -------------------- Récupérer les TD d'un Training --------------------------------------#
@td_bp.route('/td/training/<int:id_training>', methods=['GET'])
def get_tds_by_training(id_training):
    # Call the service method to get TDs by training ID
    return td_service.get_tds_by_training_id(id_training)
# -------------------- Récupérer tous les TDs --------------------------------------#
@td_bp.route('/td', methods=['GET'])
def get_all_tds():
    return td_service.get_all_tds()

# -------------------- Mettre à jour un TD --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['PUT'])
def update_td(td_id):
    data = request.get_json()
    return td_service.update_td(td_id, data)

# -------------------- Supprimer un TD --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['DELETE'])
def delete_td(td_id):
    return td_service.delete_td(td_id)

# -------------------- Créer un TD --------------------------------------#
@td_bp.route('/td', methods=['POST'])
def create_td():
    try:
        data = request.json
        return td_service.add_td(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500