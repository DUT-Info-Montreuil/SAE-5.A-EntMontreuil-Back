from flask import Blueprint, jsonify, request
from services.tp import TPService

tp_bp = Blueprint('tp_bp', __name__)
tp_service = TPService()

# -------------------- Récupérer un TP par ID --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['GET'])
def get_tp_by_id(tp_id):
    return tp_service.get_tp_by_id(tp_id)

# -------------------- Récupérer tous les TPs --------------------------------------#
@tp_bp.route('/tp', methods=['GET'])
def get_all_tps():
    return tp_service.get_all_tps()

# -------------------- Mettre à jour un TP --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['PUT'])
def update_tp(tp_id):
    data = request.get_json()
    return tp_service.update_tp(tp_id, data)

# -------------------- Supprimer un TP --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['DELETE'])
def delete_tp(tp_id):
    return tp_service.delete_tp(tp_id)

# -------------------- Ajouter un TP --------------------------------------#
@tp_bp.route('/tp', methods=['POST'])
def add_tp(tp_id):
    data = request.json
    return tp_service.add_tp(data)
