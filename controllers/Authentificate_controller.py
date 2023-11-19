from flask import request, jsonify, Blueprint
from services.authentificate import AuthentificateService
import connect_pg
from flask_jwt_extended import get_jwt_identity , jwt_required , create_access_token

# Création d'un Blueprint pour les routes liées 
authentificate_bp = Blueprint('authentificate', __name__)

# Instanciation du service 
authentificate_service = AuthentificateService()



@authentificate_bp.route('/authentification' , methods = ['POST'])
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
            access_token = create_access_token(identity=username)
            return jsonify({'token':access_token , 'id_user' : id , 'first_name' : first_name, 'last_name' : last_name})
    except Exception as e:
        # Gérez les autres erreurs
        return jsonify({'error': str(e)}), 400
    
    
    
@authentificate_bp.route('/protected' , methods = ['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
        
               