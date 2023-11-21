from flask import request, jsonify, Blueprint
from services.users import UsersServices  , ValidationError, UsersFonction
import json
from decorator.users_decorator import UsersDecorators
from flask_jwt_extended import get_jwt_identity , jwt_required
from services.students import StudentsServices
from services.teachers import TeachersService

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
        if current_user['role'] == 'student' :
          user = StudentsServices.get_student(StudentsServices, current_user['username'], 'model')
        elif current_user['role'] == 'teacher' :
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
        response , https_status = UsersFonction.remove_users(id_user)
        return response , https_status
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500