from flask import request, jsonify, Blueprint
from services.teachers import TeachersService 
import json
from flask_jwt_extended import get_jwt_identity , jwt_required
from decorators.teachers_decorator import TeachersDecorators
from services.teachers import TeachersFonction

# Création d'un Blueprint pour les routes liées
teachers_bp = Blueprint('teachers', __name__)

# Instanciation du service
teachers_service = TeachersService()

#-----------get all teachers--------------
@teachers_bp.route('/teachers', methods=['GET'])
def get_all_teachers():
    """
    Get a list of all teachers.
    ---
    tags:
      - Teachers
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
        description: List of all teachers retrieved from the database.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during teacher retrieval.
    """
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
@TeachersDecorators.validate_json_add_teacher
def add_teachers():
    """
    Add a new teacher.
    ---
    tags:
      - Teachers
    parameters:
      - name: teacher_data
        in: body
        description: JSON data for the teacher to be added.
        required: true
        schema:
          type: object
          properties:
            datas:
              type: object
              properties:
                initial:
                  type: string
                  example: "PS"
                desktop:
                  type: string
                  example: "A2-09"
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
        description: Teacher successfully added.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during teacher addition.
    """
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
@TeachersDecorators.validate_json_update_teacher
def update_teachers(id_teacher):
    """
    Update information about a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to update.
        required: true
        type: integer
      - name: teacher_data
        in: body
        description: JSON data for updating the teacher's information.
        required: true
        schema:
          type: object
          properties:
            datas:
              type: object
              properties:
                initial:
                  type: string
                  example: "PS"
                desktop:
                  type: string
                  example: "A2-09"
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
        description: Teacher information successfully updated.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during teacher information update.
    """
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
@jwt_required()
def delete_teachers(id_teacher):
    """
    Delete a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to delete.
        required: true
        type: integer
    responses:
      200:
        description: Teacher successfully deleted.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during teacher deletion.
    """
    try:
        current_user = get_jwt_identity()
        id_user = TeachersFonction.get_user_id_with_id_teacher(id_teacher)
        if (current_user["id"] == id_user) :
          return jsonify({'error':"Vous ne pouvez supprimer cette utilisateur"}), 403
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
    """
    Get details of a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to retrieve details.
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
        description: Teacher details successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during teacher retrieval.
    """
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

@teachers_bp.route('/teachers/commentaries', methods=['GET'])
def get_all_commentaries():
    try:
        output_format = request.args.get('output_format', default='dto')
        all_commentaries = teachers_service.get_commentaries(output_format)
        return jsonify(all_commentaries)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teachers_bp.route('/teachers/commentaries', methods=['POST'])
def add_commentary():
    try:
        datas = request.json
        response, https_status = teachers_service.add_commentary(datas)
        return response, https_status
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teachers_bp.route('/teachers/commentaries/update/<int:id_commentary>', methods=['PUT'])
def update_commentary(id_commentary):
    try:
        datas = request.json
        response, https_status = teachers_service.update_commentary(id_commentary, datas)
        return response, https_status
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teachers_bp.route('/teachers/commentaries/remove/<int:id_commentary>', methods=['DELETE'])
def delete_commentary(id_commentary):
    try:
        response, https_status = teachers_service.delete_commentary(id_commentary)
        return response, https_status
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@teachers_bp.route('/teachers/commentaries/get/<int:id_commentary>', methods=['GET'])
def get_commentary(id_commentary):
    try:
        output_format = request.args.get('output_format', default='dto')
        commentary = teachers_service.get_commentary(id_commentary, output_format)
        return jsonify(commentary)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
#-----------get teacher hours number--------------
# Define the route to get the total hours of a specific teacher
@teachers_bp.route('/teachers/<int:id_teacher>/hours', methods=['GET'])
def get_teacher_hours_number(id_teacher):
    """
    Get the total hours of a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to retrieve total hours.
        required: true
        type: integer
    responses:
      200:
        description: Total hours successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during total hours retrieval.
    """
    try:
        # Utilisez la fonction du service pour obtenir le nombre total d'heures d'un enseignant
        hours_data = teachers_service.get_number_of_hours(id_teacher)

        # Retournez les données au format JSON
        return hours_data
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 500


#-----------get_teacher_number_of_hours_left--------------
# Define the route to get the total hours left of a specific teacher
@teachers_bp.route('/teachers/<int:id_teacher>/hoursleft', methods=['GET'])
def get_teacher_number_of_hours_left(id_teacher):
    """
    Get the left hours of a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to retrieve left hours.
        required: true
        type: integer
    responses:
      200:
        description: Left hours successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during left hours retrieval.
    """
    try:
        # Utilisez la fonction du service pour obtenir le nombre d'heures restantes d'un enseignant
        hours_data = teachers_service.get_number_of_hours_left(id_teacher)

        # Retournez les données au format JSON
        return hours_data
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 500
    
#-----------get_teacher_number_of_hours_passed--------------
# Define the route to get the total hours passed of a specific teacher
@teachers_bp.route('/teachers/<int:id_teacher>/hourspassed', methods=['GET'])
def get_teacher_number_of_hours_passed(id_teacher):
    """
    Get the passed hours of a specific teacher by ID.
    ---
    tags:
      - Teachers
    parameters:
      - name: id_teacher
        in: path
        description: ID of the teacher to retrieve passed hours.
        required: true
        type: integer
    responses:
      200:
        description: passed hours successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during passed hours retrieval.
    """
    try:
        # Utilisez la fonction du service pour obtenir le nombre d'heures effectuées d'un enseignant
        hours_data = teachers_service.get_number_of_hours_passed(id_teacher)

        # Retournez les données au format JSON
        return hours_data
    except Exception as e:
        # Gérez les erreurs
        return jsonify({"message": "Error", "error": str(e)}), 500