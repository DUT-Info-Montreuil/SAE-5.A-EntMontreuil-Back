from flask import request, jsonify, Blueprint
from services.teachers import TeachersService 
import json

# Création d'un Blueprint pour les routes liées
teachers_bp = Blueprint('teachers', __name__)

# Instanciation du service
teachers_service = TeachersService()

#-----------get all teachers--------------
@teachers_bp.route('/teachers', methods=['GET'])
def get_all_teachers():
    try:
        # Obtenez la valeur de l'argument output_format à partir des paramètres de la requête
        output_format = request.args.get('output_format', default='dto')

        # Utilisez la fonction du service pour récupérer les enseignants
        teachers_data = teachers_service.get_teachers(output_format).json

        # Retournez les enseignants au format JSON
        return jsonify(teachers_data)
    except ValueError as ve:
        # Gérez les erreurs liées à des valeurs incorrectes
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Gérez les autres erreurs
        return jsonify({'error': str(e)}), 500
    
    
    
#-----------add teachers--------------
# Définissez la route pour ajouter des enseignants
@teachers_bp.route('/teachers', methods=['POST'])
def add_teachers():
    try:
        # Obtenez les données JSON de la requête
        json_data = request.json

        # Utilisez la fonction du service pour ajouter des enseignants
        message, status_code = teachers_service.add_teachers(json_data)

        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------update teachers--------------
# Définissez la route pour mettre à jour un enseignant
@teachers_bp.route('/teachers/<int:id_teacher>', methods=['PATCH'])
def update_teachers(id_teacher):
    try:
        # Obtenez les données JSON de la requête
        json_data = request.json

        # Utilisez la fonction du service pour mettre à jour un enseignant
        message, status_code = teachers_service.update_teachers(id_teacher, json_data)

        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------delete teachers--------------
# Définissez la route pour supprimer un enseignant
@teachers_bp.route('/teachers/<int:id_teacher>', methods=['DELETE'])
def delete_teachers(id_teacher):
    try:
        # Utilisez la fonction du service pour supprimer un enseignant
        message, status_code = teachers_service.delete_teachers(id_teacher)

        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------get one teacher--------------
# Définissez la route pour obtenir les détails d'un enseignant
@teachers_bp.route('/teachers/<int:id_teacher>', methods=['GET'])
def get_teacher(id_teacher):
    try:
        # Obtenez la valeur de l'argument output_format à partir des paramètres de la requête
        output_format = request.args.get('output_format', default='dto')
        # Utilisez la fonction du service pour obtenir les détails d'un enseignant
        teacher_data = teachers_service.get_teacher(id_teacher , output_format)

        # Retournez les données au format JSON
        return teacher_data
    except ValueError as ve:
        # Gérez les erreurs liées à des valeurs incorrectes
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400

    
