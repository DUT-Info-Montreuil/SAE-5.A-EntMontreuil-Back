from flask import jsonify, Blueprint, request
from services.roles import RolesServices , ValidationError
from decorators.roles_decorator import RolesDecorators

roles_bp = Blueprint('roles', __name__)
roles_service = RolesServices()

# Route pour créer un nouveau rôle
@roles_bp.route('/roles', methods=['POST'])
@RolesDecorators.validate_json_role
def create_role():
    """
    Create a new role.
    ---
    tags:
      - Roles
    parameters:
      - name: role_data
        in: body
        description: JSON data for creating a new role.
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
        example:
          name: "role_name"
    responses:
      200:
        description: New role successfully created.
      500:
        description: Server error in case of a problem during role creation.
    """
    try:
        role_data = request.json
        new_role = roles_service.create_role(role_data)
        return new_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour mettre à jour un rôle existant
@roles_bp.route('/roles/<int:role_id>', methods=['PATCH'])
@RolesDecorators.validate_json_role
def update_role(role_id):
    """
    Update an existing role by ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        description: ID of the role to update.
        required: true
        type: integer
      - name: role_data
        in: body
        description: JSON data for updating an existing role.
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
        example:
          name: "updated_role_name"
    responses:
      200:
        description: Role successfully updated.
      500:
        description: Server error in case of a problem during role update.
    """
    try:
        role_data = request.json
        updated_role = roles_service.update_role(role_id, role_data)
        return updated_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour supprimer un rôle existant
@roles_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """
    Delete an existing role by ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        description: ID of the role to delete.
        required: true
        type: integer
    responses:
      200:
        description: Role successfully deleted.
      500:
        description: Server error in case of a problem during role deletion.
    """
    try:
        deleted_role = roles_service.delete_role(role_id)
        return deleted_role
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir tous les rôles
@roles_bp.route('/roles', methods=['GET'])
def get_all_roles():
    """
    Get a list of all roles.
    ---
    tags:
      - Roles
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
        description: List of all roles retrieved from the database.
      500:
        description: Server error in case of a problem during role retrieval.
    """
    try:
        all_roles = roles_service.get_roles()
        return all_roles
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir un rôle spécifique par ID
@roles_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    """
    Get information about a specific role by ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        description: ID of the role to retrieve.
        required: true
        type: integer
    responses:
      200:
        description: Role information successfully retrieved.
      500:
        description: Server error in case of a problem during role retrieval.
    """
    try:
        role = roles_service.get_role_by_id(role_id)
        return role
    except ValidationError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour obtenir tous les rôles sauf étudiant et enseignant
@roles_bp.route('/roles/nee', methods=['GET'])
def get_roles_not_student_teacher():
    """
    Get a list of all roles.
    ---
    tags:
      - Roles
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
        description: List of all roles retrieved from the database.
      500:
        description: Server error in case of a problem during role retrieval.
    """
    try:
        all_roles = roles_service.get_roles_not_student_teacher()
        return all_roles
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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