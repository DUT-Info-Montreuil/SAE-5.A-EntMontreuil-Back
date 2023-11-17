from flask import request, jsonify, Blueprint
from services.authentificate import AuthentificateService
import connect_pg

# Création d'un Blueprint pour les routes liées 
authentificate_bp = Blueprint('authentificate', __name__)

# Instanciation du service 
authentificate_service = AuthentificateService()

@authentificate_bp.route('/authentification' , methods = ['POST'])
def authentification():
    try :
        auth_data = request.json
        response, http_status = authentificate_service.authentification(auth_data)
        
        return response, http_status
    except Exception as e:
        # Gérez les autres erreurs
        return jsonify({'error': str(e)}), 500
        
               