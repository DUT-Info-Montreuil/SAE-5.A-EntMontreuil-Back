from flask import request, jsonify, Blueprint
from services.students import StudentsServices , ValidationError
from services.absences import AbsencesService
import json
from flask_jwt_extended import get_jwt_identity , jwt_required
from decorators.students_decorator import StudentsDecorators
import os
# Création d'un Blueprint pour les routes liées
students_bp = Blueprint('students', __name__)

# Instanciation du service
students_services = StudentsServices()
absences_services = AbsencesService()  # Créez une instance de AbsencesService

@students_bp.route('/student/absences', methods=['GET'])
@jwt_required()
def get_student_absences_route():
    """
    Récupère les absences d'un étudiant spécifique à partir de son nom d'utilisateur à partir du token.
    ---
    tags:
      - Students
    descriptions: 
      - Cette route permet d'obtenir la liste des absences pour un étudiant, identifié par son nom d'utilisateur extrait du token JWT.
    responses:
      200:
        description: Liste des absences de l'étudiant retournée avec succès.
        examples:
          application/json: 
            [
                {
                    "course_date": "2023-11-15",
                    "course_end_time": "12:30:00",
                    "course_start_time": "10:30:00",
                    "id_Course": 2,
                    "id_Student": 6,
                    "justify": true,
                    "reason": "Raison personnelle",
                    "resource_name": "Ressource2",
                    "student_first_name": "teset",
                    "student_last_name": "teset"
                }
            ]
      400:
        description: Erreur de requête ou problème de validation.
      500:
        description: Erreur serveur interne.
    """
    try:
        # Extraire le username du token JWT
        current_user = get_jwt_identity()
        
        # Appeler la fonction du service en passant le username
        absences = absences_services.get_student_absences(current_user["username"], justified=None,output_format="model")

        # Retourner la réponse
        return jsonify(absences), 200
    except Exception as e:
        # Gérer les exceptions ici
        return jsonify({'error': str(e)}), 500


#-----------get all students--------------
@students_bp.route('/students', methods=['GET'])
def get_all_students_controller():
    """
    Get a list of all students.
    ---
    tags:
      - Students
    parameters:
      - name: output_format
        in: query
        description: Output format (default is "dto").
        required: false
        type: string
        default: "dto"
        enum: ["dto", "model"]
    responses:
      200:
        description: List of all students retrieved from the database.
        examples:
          application/json: [
            {
              "id": 1,
              "ine": "12345",
              "nip": "12345",
              "apprentice": true,
              "user": {
                "email": "test@test.fr",
                "username": "teste",
                "first_name": "test",
                "last_name": "test",
                "password": "Ouinon#1234"
              }
            },
            # ... (other students)
          ]
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student retrieval.
    """
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
    """
    Get information about a specific student by ID.
    ---
    tags:
      - Students
    parameters:
      - name: id_students
        in: path
        description: ID of the student to retrieve.
        required: true
        type: integer
      - name: output_format
        in: query
        description: Output format (default is "dto").
        required: false
        type: string
        default: "dto"
        enum: ["dto", "model"]
    responses:
      200:
        description: Information about the specified student retrieved from the database.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student retrieval.
    """
    try:
        # Obtenez la valeur de l'argument output_format à partir des paramètres de la requête
        # Utilisez la fonction du service pour obtenir les détails d'un etudiant
        student_data = students_services.get_student(id_students)

        # Retournez les données au format JSON
        return jsonify(student_data)
    except ValidationError as va :
        return jsonify({'error': str(va)}), 400
    except ValueError as ve:
        # Gérez les erreurs liées à des valeurs incorrectes
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------delete students--------------
@students_bp.route('/students/<int:id_student>', methods=['DELETE'])
def delete_student(id_student):
    """
    Delete a specific student by ID.
    ---
    tags:
      - Students
    parameters:
      - name: id_student
        in: path
        description: ID of the student to delete.
        required: true
        type: integer
    responses:
      200:
        description: Student successfully deleted.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student deletion.
    """
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
@StudentsDecorators.validate_json_add_student
def add_students():
    """
    Add a new student.
    ---
    tags:
      - Students
    parameters:
      - name: student_data
        in: body
        description: JSON data for the student to be added.
        required: true
        schema:
          type: object
          properties:
            datas:
              type: object
              properties:
                ine:
                  type: string
                  example: "12345"
                nip:
                  type: string
                  example: "12345"
                apprentice:
                  type: boolean
                  example: true
                user:
                  type: object
                  properties:
                    email:
                      type: string
                      example: "test@test.fr"
                    username:
                      type: string
                      example: "teste"
                    first_name:
                      type: string
                      example: "test"
                    last_name:
                      type: string
                      example: "test"
                    password:
                      type: string
                      example: "Ouinon#1234"
    responses:
      200:
        description: Student successfully added.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student addition.
    """
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
@StudentsDecorators.validate_json_update_student
def update_students(id_student):
    """
    Update information about a specific student by ID.
    ---
    tags:
      - Students
    parameters:
      - name: id_student
        in: path
        description: ID of the student to update.
        required: true
        type: integer
      - name: student_data
        in: body
        description: JSON data for updating the student's information.
        required: true
        schema:
          type: object
          properties:
            datas:
              type: object
              properties:
                ine:
                  type: string
                  example: "12345"
                nip:
                  type: string
                  example: "12345"
                apprentice:
                  type: boolean
                  example: true
                user:
                  type: object
                  properties:
                    email:
                      type: string
                      example: "test@test.fr"
                    username:
                      type: string
                      example: "teste"
                    first_name:
                      type: string
                      example: "test"
                    last_name:
                      type: string
                      example: "test"
                    password:
                      type: string
                      example: "Ouinon#1234"
    responses:
      200:
        description: Student information successfully updated.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student information update.
    """
    try:
        request_data = request.json
        # Utilisez la fonction du service pour modifier un etudiant
        message, status_code = students_services.update_students(id_student,request_data['datas'])
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------update students--------------
@students_bp.route('/students/add_csv', methods=['POST'])
def csv_add_students():
    try:
      
        if 'file' not in request.files:
          return jsonify({'message': 'No file part'}), 400
      
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        message, status_code = students_services.csv_add_students(file)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
      
@students_bp.route('/students/verify_csv', methods=['POST'])
def csv_verify_students():
    try:
      
        if 'file' not in request.files:
          return jsonify({'message': 'No file part'}), 400
      
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        message, status_code = students_services.verification_csv_file(file)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
      
      
@students_bp.route('/students/promotion/<int:promotion_id>', methods=['GET'])
def get_students_in_promotion(promotion_id):
    try:
        return students_services.get_all_students_in_promo(promotion_id)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
      

@students_bp.route('/students/all', methods=['GET'])
def get_all_students():
    try:
        return students_services.get_all_students()
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
      
