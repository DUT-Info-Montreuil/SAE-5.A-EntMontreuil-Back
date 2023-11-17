from flask import jsonify, Blueprint, request
from services.roles import RolesServices , ValidationError

roles_bp = Blueprint('roles', __name__)
roles_service = RolesServices()

# Route pour créer un nouveau rôle
@roles_bp.route('/roles', methods=['POST'])
def create_role():
    try:
        role_data = request.json
        new_role = roles_service.create_role(role_data)
        return new_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour mettre à jour un rôle existant
@roles_bp.route('/roles/<int:role_id>', methods=['PATCH'])
def update_role(role_id):
    try:
        role_data = request.json
        updated_role = roles_service.update_role(role_id, role_data)
        return updated_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour supprimer un rôle existant
@roles_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    try:
        deleted_role = roles_service.delete_role(role_id)
        return deleted_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir tous les rôles
@roles_bp.route('/roles', methods=['GET'])
def get_all_roles():
    try:
        all_roles = roles_service.get_roles()
        return all_roles
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir un rôle spécifique par ID
@roles_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    try:
        role = roles_service.get_role_by_id(role_id)
        return role
    except ValidationError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500