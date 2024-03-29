from flask import request, jsonify, Blueprint
import json
from decorators.users_decorator import UsersDecorators
from flask_jwt_extended import get_jwt_identity , jwt_required
from services.students import StudentsServices
from services.teachers import TeachersService
from services.users import UsersServices, ValidationError, UsersFonction
# Création d'un Blueprint pour les routes liées 
users_bp = Blueprint('users', __name__)

# Instanciation du service 
users_service = UsersServices()

#-----------get all users--------------
@users_bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Get a list of all users.
    ---
    tags:
      - Users
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
        description: List of all users retrieved from the database.
      500:
        description: Server error in case of a problem during user retrieval.
    """
    try:
        output_format = request.args.get('output_format', default='dto')
        all_users = users_service.get_users(output_format).json
        return jsonify(all_users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
    
#------------get one user with id-------------
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_one_user(id):
    """
    Get information about a specific user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        description: ID of the user to retrieve.
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
        description: User information successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during user retrieval.
    """
    try:
        output_format = request.args.get('output_format', default='dto')
        user = users_service.get_users_with_id(id, output_format)
        return jsonify(user)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
#------------add user-------------
@users_bp.route('/users', methods=['POST'])
@UsersDecorators.validate_json_add_user
def add_user():
    """
    Add a new user.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: user
        description: User object to be added.
        required: true
        schema:
          $ref: '#/definitions/UserSchema'
    responses:
      200:
        description: User successfully added.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Confirmation message.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during user addition.
    definitions:
      UserSchema:
        type: object
        properties:
          datas:
            type: object
            properties:
              user:
                $ref: '#/definitions/UserData'
            required:
              - user
        required:
          - datas
      UserData:
        type: object
        properties:
          first_name:
            type: string
          last_name:
            type: string
          username:
            type: string
          email:
            type: string
          role:
            type: string
        required:
          - first_name
          - last_name
          - username
          - email
          - role
        additionalProperties: false
    """

    try:
        datas = request.json
        response , https_status = users_service.add_user(datas['datas']['user'])
        return response , https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
#------------ user info-----------------
@users_bp.route('/user/info', methods=['GET'])
@jwt_required()
def get_user_info():
  
    """
    Get information about the current user.
    ---
    tags:
      - Users
    security:
      - jwt: []
    responses:
      200:
        description: User information successfully retrieved.
        schema:
          $ref: '#/definitions/UserModel'
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during user retrieval.
    definitions:
      UserModel:
        type: object
        properties:
          id:
            type: integer
          first_name:
            type: string
          last_name:
            type: string
          username:
            type: string
          email:
            type: string
          role:
            type: string
        required:
          - id
          - first_name
          - last_name
          - username
          - email
          - role
    """
    try:
        current_user = get_jwt_identity()
        if current_user['role'] == 'étudiant' :
          user = StudentsServices.get_student(StudentsServices, current_user['username'])
        elif current_user['role'] == 'enseignant' :
          user = TeachersService.get_teacher(TeachersService, current_user['username'] , 'model')
        else: 
          user = users_service.get_users_with_id(current_user['id'] ,'model')
        return jsonify(user)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
#------------update user-------------
@users_bp.route('/users/<int:id_user>', methods=['PATCH'])
@UsersDecorators.validate_json_update_user
def update_user(id_user):
    """
    Update user information by ID.
    ---
    tags:
      - Users
    parameters:
      - name: id_user
        in: path
        description: ID of the user to update.
        required: true
        type: integer
      - in: body
        name: user
        description: User object to update.
        required: true
        schema:
          $ref: '#/definitions/UserUpdate'
    responses:
      200:
        description: User information successfully updated.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during user update.
    definitions:
      UserUpdate:
        type: object
        properties:
          datas:
            type: object
            properties:
              user:
                $ref: '#/definitions/UserData'
            required:
              - user
        required:
          - datas
      UserData:
        type: object
        properties:
          first_name:
            type: string
          last_name:
            type: string
          username:
            type: string
          email:
            type: string
          role:
            type: string
          password:
            type: string
        additionalProperties: false
    """
    try:
        datas = request.json
        response , https_status = UsersFonction.update_users(datas['datas']['user'] , id_user)
        return response , https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
      
#------------delete user-------------
@users_bp.route('/users/<int:id_user>', methods=['DELETE'])
@jwt_required()
def delete_user(id_user):
    """
    Delete user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: id_user
        in: path
        description: ID of the user to delete.
        required: true
        type: integer
    responses:
      204:
        description: User successfully deleted.
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during user deletion.
    """
    
    try:
        current_user = get_jwt_identity()
        if (current_user["id"] == id_user) :
          return jsonify({'error':"Vous ne pouvez supprimer cette utilisateur"}), 403
        
        response , https_status = UsersFonction.remove_users(id_user)
        return response , https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/reminders', methods=['GET'])
def get_all_reminders():
    """
    Get all reminders.
    ---
    tags:
      - Reminders
    parameters:
      - name: output_format
        in: query
        type: string
        default: "dto"
        enum: ["dto", "model"]
        description: Output format (default is "dto").
    responses:
      200:
        description: List of all reminders.
      400:
        description: Bad request or validation error.
      500:
        description: Server error.
    """
    try:
        output_format = request.args.get('output_format', default='dto')
        all_reminders = UsersFonction.get_all_reminders(output_format)
        return jsonify(all_reminders)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/reminders/<int:id_user>', methods=['GET'])
@jwt_required()
def get_reminder_by_id(id_user):
  """
    Get reminder by ID.
    ---
    tags:
      - Reminders
    parameters:
      - name: id_user
        in: path
        type: integer
        required: true
        description: ID of the user.
      - name: output_format
        in: query
        type: string
        default: "DTO"
        description: Output format (default is "DTO").
    responses:
      200:
        description: Reminder information.
      404:
        description: Reminder not found.
      500:
        description: Server error.
    """
  try:
      current_user = get_jwt_identity()
      id_user = current_user["id"]
      output_format = request.args.get('output_format', default='DTO')
      reminders = UsersFonction.get_reminder_by_id(id_user, output_format)
      return jsonify(reminders), 200
  except ValidationError as e:
      return jsonify({'error': str(e)}), 404
  except Exception as e:
      return jsonify({'error': str(e)}), 500

@users_bp.route('/users/reminders', methods=['POST'])
@jwt_required()
def add_reminder():
    """
    Add a new reminder.
    ---
    tags:
      - Reminders
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Reminder successfully added.
      400:
        description: Bad request or validation error.
      500:
        description: Server error during reminder addition.
    """
    try:
        current_user = get_jwt_identity()
        data = request.json
        response, https_status = UsersFonction.add_reminder(current_user['id'], data)
        return response, https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/reminders/<int:reminder_id>', methods=['PUT'])
@jwt_required()
def update_reminder(reminder_id):
    """
    Update reminder by ID.
    ---
    tags:
      - Reminders
    parameters:
      - name: reminder_id
        in: path
        type: integer
        required: true
        description: ID of the reminder to update.
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Reminder successfully updated.
      400:
        description: Bad request or validation error.
      500:
        description: Server error during reminder update.
    """
    try:
        current_user = get_jwt_identity()
        data = request.json
        response, https_status = UsersFonction.update_reminder(current_user['id'], data, reminder_id)
        return response, https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/reminders/<int:reminder_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    """
    Delete reminder by ID.
    ---
    tags:
      - Reminders
    parameters:
      - name: reminder_id
        in: path
        type: integer
        required: true
        description: ID of the reminder to delete.
    responses:
      204:
        description: Reminder successfully deleted.
      400:
        description: Bad request or validation error.
      500:
        description: Server error during reminder deletion.
    """
    try:
        current_user = get_jwt_identity()
        response, https_status = UsersFonction.delete_reminder(current_user['id'], reminder_id)
        return response, https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/user/notifications', methods=['GET'])
@jwt_required()
def get_user_notifications():
    """
    Get user notifications.
    ---
    tags:
      - Notifications
    parameters:
      - name: reading
        in: query
        type: string
        default: "false"
        enum: ["true", "false"]
        description: Mark notifications as read if set to "true".
      - name: display
        in: query
        type: string
        description: Display parameter.
    responses:
      200:
        description: User notifications successfully retrieved.
      400:
        description: Bad request or validation error.
      500:
        description: Server error during notification retrieval.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        if request.args.get('reading') == 'true':
            UsersFonction.set_notifications_to_read(user_id)

        # Récupérer le paramètre display, s'il est présent
        display = request.args.get('display')
        notifications = UsersFonction.get_notifications(user_id, display)

        return jsonify(notifications)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
@users_bp.route('/user/notifications', methods=['DELETE'])
@jwt_required()
def delete_all_user_notifications():
    """
    Delete all user notifications.
    ---
    tags:
      - Notifications
    responses:
      200:
        description: All notifications deleted successfully.
      400:
        description: Bad request or validation error.
      500:
        description: Server error during notification deletion.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        UsersFonction.delete_user_notifications(user_id)

        return jsonify({'message': 'Toutes les notifications ont été supprimées.'}), 200
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/commentaries', methods=['GET'])
@jwt_required()
def get_commentaries():
    """
    Get commentaries.
    ---
    tags:
      - Comments
    parameters:
      - name: output_format
        in: query
        type: string
        default: "DTO"
        description: Output format.
      - name: id_promotion
        in: query
        type: integer
        description: ID of the promotion to filter comments (optional).
    responses:
      200:
        description: Commentaries retrieved successfully.
      500:
        description: Server error during commentary retrieval.
    """
    try:
        output_format = request.args.get('output_format', default='DTO')
        id_promotion = request.args.get('id_promotion', type=int)
        comments = UsersFonction.get_commentaries(id_promotion, output_format)
        return jsonify(comments)

    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}), 500

@users_bp.route('/users/comments/<int:comment_id>', methods=['GET'])
@jwt_required()
def get_comment_by_id(comment_id):
    """
    Get a comment by ID.
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
        description: ID of the comment to retrieve.
      - name: output_format
        in: query
        type: string
        default: "DTO"
        description: Output format.
    responses:
      200:
        description: Comment retrieved successfully.
      500:
        description: Server error during comment retrieval.
    """
    try:
        output_format = request.args.get('output_format', default='DTO')
        comment = UsersFonction.get_commentary_by_id(comment_id, output_format)
        return jsonify(comment)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/comments', methods=['POST'])
@jwt_required()
def add_comment():
    """
    Add a new comment.
    ---
    tags:
      - Comments
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Comment added successfully.
      500:
        description: Server error during comment addition.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.json
        response, https_status = UsersFonction.add_commentary(user_id, data)
        return response, https_status
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """
    Update a comment by ID.
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
        description: ID of the comment to update.
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Comment updated successfully.
      500:
        description: Server error during comment update.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.json
        response, https_status = UsersFonction.update_commentary(user_id, comment_id, data)
        return response, https_status
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """
    Delete a comment by ID.
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
        description: ID of the comment to delete.
    responses:
      200:
        description: Comment deleted successfully.
      500:
        description: Server error during comment deletion.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        response, https_status = UsersFonction.delete_commentary(user_id, comment_id)
        return response, https_status
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/commentaries/week/<int:week_start_date>', methods=['GET'])
@jwt_required()
def get_commentaries_by_week(week_start_date):
    """
    Get commentaries by week.
    ---
    tags:
      - Comments
    parameters:
      - name: week_start_date
        in: path
        type: int
        required: true
        description: Start date of the week in timestamp format.
      - name: output_format
        in: query
        type: string
        default: "DTO"
        description: Output format.
      - name: id_promotion
        in: query
        type: integer
        description: ID of the promotion to filter comments (optional).
    responses:
      200:
        description: Commentaries retrieved successfully.
      500:
        description: Server error during commentary retrieval.
    """
    try:
        output_format = request.args.get('output_format', default='DTO')
        id_promotion = request.args.get('id_promotion', type=int)
        
        if id_promotion is not None:
            comments = UsersFonction.get_commentary_by_week(week_start_date, id_promotion, output_format)
        else:
            comments = UsersFonction.get_commentary_by_week(week_start_date, output_format)

        return jsonify(comments)

    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}), 500
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