from flask import request, jsonify, Blueprint
from services.users import UsersServices  , ValidationError
import json

# Création d'un Blueprint pour les routes liées aux absences
users_bp = Blueprint('users', __name__)

# Instanciation du service d'absences
users_service = UsersServices()

#-----------get all users--------------
@users_bp.route('/users', methods=['GET'])
def get_all_users_dto():
    try:
        all_users = users_service.get_users().json
        return jsonify(all_users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#------------get one user with id-------------
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_one_users_dto(id):
    try:
        user = users_service.get_users_with_id(id)
        return jsonify(user)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500