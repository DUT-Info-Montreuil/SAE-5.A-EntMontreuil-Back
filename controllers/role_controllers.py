from flask import jsonify, Blueprint, request
from services.role import RoleServices , ValidationError

role_bp = Blueprint('role', __name__)
role_service = RoleServices()

# Route pour créer un nouveau rôle
@role_bp.route('/roles', methods=['POST'])
def create_role():
    try:
        role_data = request.json
        new_role = role_service.create_role(role_data)
        return new_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour mettre à jour un rôle existant
@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    try:
        role_data = request.json
        updated_role = role_service.update_role(role_id, role_data)
        return updated_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour supprimer un rôle existant
@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    try:
        deleted_role = role_service.delete_role(role_id)
        return deleted_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir tous les rôles
@role_bp.route('/roles', methods=['GET'])
def get_all_roles():
    try:
        all_roles = role_service.get_roles()
        return all_roles
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir un rôle spécifique par ID
@role_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    try:
        role = role_service.get_role_by_id(role_id)
        return role
    except ValidationError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
