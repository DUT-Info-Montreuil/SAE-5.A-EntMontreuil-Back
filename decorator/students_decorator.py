from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema_add_student = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id" : {"type": "integer"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "username" : {"type": "string"},
                        "email" : {"type": "string"},
                        "password" : {"type": "string"}
                    },
                    "required": ["first_name", "last_name", "username", "email"],  # Champs obligatoires dans 'user'
                    "additionalProperties": False  
                },
                "apprentice" : {"type" : "boolean"},
                "ine" : {"type" : "integer"},
                "nip" : {"type" : "integer"},
                "id" : {"type" : "integer"}
            },
            "required": ["user", "ine", "nip"],  # Champs obligatoires dans 'datas'
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}


schema_update_student = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "username" : {"type": "string"},
                        "email" : {"type": "string"},
                        "password" : {"type": "string"}
                    },
                    "additionalProperties": False  
                },
                "apprentice" : {"type" : "boolean"},
                "ine" : {"type" : "integer"},
                "nip" : {"type" : "integer"}
            },
            "required": ["user"],  # Champs obligatoires dans 'datas'
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}


schema_add_student_csv = {
    "type": "object",
    "properties": {
        "file_path": {"type": "string"}
    },
    "required": ["file_path"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

class StudentsDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_add_student(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_add_student)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    
    def validate_json_update_student(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_update_student)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'}), 400
        return decorated_function
    
    
    def validate_json_add_student_csv(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_add_student_csv)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function


