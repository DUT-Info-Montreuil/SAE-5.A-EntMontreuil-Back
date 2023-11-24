from flask import request, jsonify, Blueprint
from services.authentificate import AuthentificateService
import connect_pg
from flask_jwt_extended import get_jwt_identity , jwt_required , create_access_token, create_refresh_token
import jwt
from datetime import datetime
from decorators.authentification_decorator import AuthentificationDecorators

# Création d'un Blueprint pour les routes liées 
authentificate_bp = Blueprint('authentificate', __name__)

# Instanciation du service 
authentificate_service = AuthentificateService()



@authentificate_bp.route('/authentification' , methods = ['POST'])
@AuthentificationDecorators.validate_json_authentification
def authentification():
    """
    Authentification de l'utilisateur.

    Cette route permet à l'utilisateur de s'authentifier et de recevoir un jeton d'accès.

    ---
    tags:
      - Authentification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nom d'utilisateur de l'utilisateur.
            password:
              type: string
              description: Mot de passe de l'utilisateur.
    responses:
      200:
        description: Authentification réussie. Renvoie un jeton d'accès.
        schema:
          type: object
          properties:
            token:
              type: string
              description: Jeton d'accès JWT.
      400:
        description: Erreur de requête. Renvoie un message d'erreur.

    """
    try :
        auth_data = request.json
        response, http_status = authentificate_service.authentification(auth_data)
        if http_status != 200 :  
            return response, http_status
        else :
            username = response.json.get('username')
            id = response.json.get('id_user')
            first_name = response.json.get('first_name')
            last_name = response.json.get('last_name')
            role = response.json.get('role')
            user = {
              "id": id,
              "first_name" : first_name,
              "last_name" : last_name,
              "username" : username,
              "role" : role
            }
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return jsonify({'token':access_token , 'refresh_token' : refresh_token, 'id_user' : id , 'first_name' : first_name, 'last_name' : last_name})
    except Exception as e:
        # Gérez les autres erreurs
        return jsonify({'error': str(e)}), 400

# Route pour rafraîchir le temps de validité du token d'accès
@authentificate_bp.route('/refresh_token', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
  """
  refresh token
  ---
  tags:
    - Authentification
  summary: Rafraîchir le token d'accès
  description: Rafraîchit le token d'accès pour prolonger sa durée de validité.
  parameters:
        - name: Authorization
          in: header
          description: Jeton d'authentification JWT, Bearer <token>.
          required: true
          type: string
          pattern: '^Bearer [A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+$'
  responses:
    200:
      description: Nouveau token d'accès généré avec succès.
      content:
        application/json:
          schema:
            type: object
            properties:
              access_token:
                type: string
                description: Nouveau token d'accès.
    400:
      description: Erreur de requête en cas de problème lors du rafraîchissement du token.
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Description de l'erreur survenue.

  """
  try :
    current_user = get_jwt_identity()
    # Émettre un nouveau token d'accès avec une nouvelle date d'expiration étendue
    new_access_token = create_access_token(identity=current_user)
    return jsonify(new_access_token=new_access_token), 200
  except Exception as e:
    # Gérez les autres erreurs
    return jsonify({'error': str(e)}), 400
        
               