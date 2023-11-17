from flask import request, jsonify, Blueprint
from services.students import StudentsServices , ValidationError
import json

# Création d'un Blueprint pour les routes liées
students_bp = Blueprint('students', __name__)

# Instanciation du service
students_services = StudentsServices()

#-----------get all students--------------
@students_bp.route('/students', methods=['GET'])
def get_all_students_controller():
    try:
        # Obtenez la valeur de l'argument output_format à partir des paramètres de la requête
        output_format = request.args.get('output_format', default='dto')

        # Utilisez la fonction du service pour récupérer les etudiants
        students_data = students_services.get_all_students(output_format).json

        # Retournez les etudiants au format JSON
        return jsonify(students_data)
    except ValueError as ve:
        # Gérez les erreurs liées à des valeurs incorrectes
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Gérez les autres erreurs
        return jsonify({'error': str(e)}), 500
    
#-----------get one students--------------
@students_bp.route('/students/<int:id_students>', methods=['GET'])
def get_student_controller(id_students):
    try:
        # Obtenez la valeur de l'argument output_format à partir des paramètres de la requête
        output_format = request.args.get('output_format', default='dto')
        # Utilisez la fonction du service pour obtenir les détails d'un etudiant
        student_data = students_services.get_student(id_students , output_format)

        # Retournez les données au format JSON
        return jsonify(student_data)
    except ValidationError as va :
        return jsonify({'error': str(ve)}), 400
    except ValueError as ve:
        # Gérez les erreurs liées à des valeurs incorrectes
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------delete students--------------
@students_bp.route('/students/<int:id_student>', methods=['DELETE'])
def delete_student(id_student):
    try:
        # Utilisez la fonction du service pour supprimer un etudiant
        message, status_code = students_services.delete_students(id_student)
        # Retournez la réponse au format JSON
        return message, status_code
    except ValidationError as va :
        return jsonify({'error': str(va)}), 400
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------add students--------------
@students_bp.route('/students', methods=['POST'])
def add_students():
    try:
        request_data = request.json
        # Utilisez la fonction du service pour ajouter un etudiant
        message, status_code = students_services.add_students(request_data)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------update students--------------
@students_bp.route('/students/<int:id_student>', methods=['PATCH'])
def update_students(id_student):
    try:
        request_data = request.json
        # Utilisez la fonction du service pour modifier un etudiant
        message, status_code = students_services.update_students(id_student,request_data)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------update students--------------
@students_bp.route('/students/add_csv', methods=['POST'])
def csv_add_students():
    try:
        request_data = request.json
        path = request_data["file_path"]
        message, status_code = students_services.csv_add_students(path)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400