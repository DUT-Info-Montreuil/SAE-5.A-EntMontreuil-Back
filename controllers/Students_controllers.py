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
        output_format = request.args.get('output_format', default='dto')
        # Utilisez la fonction du service pour obtenir les détails d'un etudiant
        student_data = students_services.get_student(id_students , output_format)

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
        message, status_code = students_services.update_students(id_student,request_data)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400
    
#-----------update students--------------
@students_bp.route('/students/add_csv', methods=['POST'])
def csv_add_students():
    """
    Add multiple students from a CSV file.
    ---
    tags:
      - Students
    parameters:
      - name: file_path
        in: body
        description: Path to the CSV file containing student data.
        required: true
        schema:
          type: object
          properties:
            file_path:
              type: string
              example: "C:/Users/xxp90/Documents/BUT INFO/SAE EDT/csv_students.csv"
    responses:
      200:
        description: Students successfully added from the CSV file.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during student addition from the CSV file.
    """
    try:
        request_data = request.json
        path = request_data["file_path"]
        message, status_code = students_services.csv_add_students(path)
        # Retournez la réponse au format JSON
        return message, status_code
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 400