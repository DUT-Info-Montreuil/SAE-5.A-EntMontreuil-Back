from flask import jsonify, Blueprint, request
from services.settings import SettingsService
from decorators.settings_decorator import SettingsDecorators

settings_bp = Blueprint('settings', __name__)
settings_service = SettingsService()

# une route pour mofifier les paramètres d'un utilisateur en fonction de son id
@settings_bp.route('/settings/<int:user_id>', methods=['PUT'])
@SettingsDecorators.validate_json_update_settings
def update_settings(user_id):
    """
    Update user settings by user ID.
    ---
    tags:
      - Settings
    parameters:
      - name: user_id
        in: path
        description: ID of the user whose settings need to be updated.
        required: true
        type: integer
      - name: body
        in: body
        description: JSON data for updating user settings.
        required: true
        schema:
          type: object
          properties:
            notification_mail:
              type: boolean
              example: true
            notification_website:
              type: boolean
              example: true
    responses:
      200:
        description: User settings successfully updated.
      400:
        description: Bad request - JSON validation failed.
      500:
        description: Server error in case of a problem during update.
    """
    try:
        data = request.json
        updated_settings = settings_service.update_settings(user_id, data)
        return updated_settings
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# une route pour obtenir les paramètres d'un utilisateur en fonction de son id
@settings_bp.route('/settings/<int:user_id>', methods=['GET'])
def get_settings(user_id):
    """
    Get user settings by user ID.
    ---
    tags:
      - Settings
    parameters:
      - name: user_id
        in: path
        description: ID of the user whose settings need to be retrieved.
        required: true
        type: integer
    responses:
      200:
        description: User settings successfully retrieved.
      500:
        description: Server error in case of a problem during retrieval.
    """
    try:
        user_settings = settings_service.get_settings(user_id)
        return user_settings
    except Exception as e:
        return jsonify({'error': str(e)}), 500
