from flask import request, jsonify, Blueprint
from services.students import StudentsServices , ValidationError
from services.absences import AbsencesService
import connect_pg
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
    """
    Ajoutez des étudiants à partir d'un fichier CSV.
    ---
    tags:
      - Students
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Fichier CSV contenant les données des étudiants.
    responses:
      200:
        description: Étudiants ajoutés avec succès.
      400:
        description: Aucune partie de fichier ou fichier non sélectionné.
      500:
        description: Erreur serveur interne.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        message, status_code = students_services.csv_add_students(file)
        return message, status_code
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

@students_bp.route('/students/verify_csv', methods=['POST'])
def csv_verify_students():
    """
    Vérifiez la validité du fichier CSV pour l'ajout d'étudiants.
    ---
    tags:
      - Students
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Fichier CSV à vérifier.
    responses:
      200:
        description: Fichier CSV valide.
      400:
        description: Aucune partie de fichier ou fichier non sélectionné.
      500:
        description: Erreur serveur interne.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        message, status_code = students_services.verification_csv_file(file)
        return message, status_code
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 400

@students_bp.route('/students/promotion/<int:promotion_id>', methods=['GET'])
def get_students_in_promotion(promotion_id):
    """
    Obtenez la liste des étudiants dans une promotion spécifique.
    ---
    tags:
      - Students
    parameters:
      - name: promotion_id
        in: path
        type: integer
        required: true
        description: ID de la promotion.
    responses:
      200:
        description: Liste des étudiants dans la promotion récupérée avec succès.
      500:
        description: Erreur serveur interne.
    """
    try:
        return students_services.get_all_students_in_promo(promotion_id)
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

@students_bp.route('/students/all', methods=['GET'])
def get_all_students_cohort():
    """
    Obtenez la liste de tous les étudiants dans la cohorte.
    ---
    tags:
      - Students
    responses:
      200:
        description: Liste de tous les étudiants récupérée avec succès.
      500:
        description: Erreur serveur interne.
    """
    try:
        return students_services.get_all_students_cohort()
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

@students_bp.route('/students/no-promotion', methods=['GET'])
def get_students_without_promotion():
    """
    Obtenez la liste des étudiants sans promotion.
    ---
    tags:
      - Students
    responses:
      200:
        description: Liste des étudiants sans promotion récupérée avec succès.
      500:
        description: Erreur serveur interne.
    """
    try:
        return students_services.get_students_without_promotion()
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

@students_bp.route('/students/set-promotion', methods=['POST'])
def set_students_promotion_route():
    """
    Associez des étudiants à une promotion spécifique.
    ---
    tags:
      - Students
    parameters:
      - name: promotion_id
        in: body
        type: integer
        required: true
        description: ID de la promotion à laquelle associer les étudiants.
      - name: student_ids
        in: body
        type: array
        items:
          type: integer
        required: true
        description: Liste des ID des étudiants à associer à la promotion.
    responses:
      200:
        description: Étudiants associés à la promotion avec succès.
      400:
        description: ID de promotion ou ID d'étudiant non fournis.
    """
    data = request.json
    promotion_id = data.get('promotion_id')
    student_ids = data.get('student_ids')

    if not promotion_id or not student_ids:
        return jsonify({"error": "Promotion ID ou identifiants d'étudiants non fournis"}), 400

    return students_services.set_students_promotion(promotion_id, student_ids)

@students_bp.route('/students/group', methods=['GET'])
def get_students_by_group():
    group_type = request.args.get('groupType')
    group_id = request.args.get('id')
    course_id = request.args.get('courseId')

    if not group_type or not group_id:
      return jsonify({"message": "Invalid request"}), 400

    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
        # Requête de base pour récupérer les étudiants
          base_query = """
          SELECT s.*, u.username, u.last_name, u.first_name, u.email, 
               CASE WHEN a.id_course IS NOT NULL THEN TRUE ELSE FALSE END as is_absent
          FROM ent.students s
          JOIN ent.users u ON s.id_user = u.id
          LEFT JOIN ent.absences a ON s.id = a.id_student AND a.id_course = %s
          """
         # Ajout de conditions spécifiques en fonction du type de groupe
          if group_type == 'promotion':
              sql_query = base_query + "WHERE s.id_promotion = %s;"
          elif group_type == 'training':
              sql_query = base_query + """
              JOIN ent.td ON s.id_td = ent.td.id
              WHERE ent.td.id_training = %s;
              """
          elif group_type == 'td':
              sql_query = base_query + "WHERE s.id_td = %s;"
          elif group_type == 'tp':
              sql_query = base_query + "WHERE s.id_tp = %s;"
          else:
              return jsonify({"message": "Invalid group type"}), 400

          # Exécution de la requête SQL avec les paramètres group_id et course_id
          cursor.execute(sql_query, (course_id, group_id))
          students = cursor.fetchall()
        
          students_list = [
              {
                  "student_id": row[0],
                  "apprentice": row[1],
                  "username": row[8],
                  "last_name": row[9],
                  "first_name": row[10],
                  "email": row[11],
                  "is_absent": row[12]  # Ajout du champ is_absent
              } 
              for row in students
          ]
        
        # Structuration de la réponse
        response = {
            "group_type": group_type,
            "group_id": group_id,
            "course_id": course_id,
            "students": students_list
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    finally:
      conn.close()
"""ENT Montreuil is a Desktop Working Environnement for the students of the IUT of Montreuil
    Copyright (C) 2024  Steven CHING, Emilio CYRIAQUE-SOURISSEAU ALVARO-SEMEDO, Ismail GADA, Yanis HAMANI, Priyank SOLANKI

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""