from flask import request, jsonify, Blueprint
from services.users import UsersServices  , ValidationError

# Création d'un Blueprint pour les routes liées aux absences
users_bp = Blueprint('users', __name__)

# Instanciation du service d'absences
users_service = UsersServices()


@users_bp.route('/users/model', methods=['GET'])
def get_all_users_model():
    try:
        data = request.get_json()
        result = users_service.get_users()
        return jsonify(result)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
