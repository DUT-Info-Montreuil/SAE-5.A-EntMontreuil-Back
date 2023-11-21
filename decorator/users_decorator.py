from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema = {
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
                        "role" : {"type": "string"},
                        "password" : {"type": "string"}
                    },
                    "required": ["first_name", "last_name", "username", "email", "role"]  # Champs obligatoires dans 'user'
                }
            },
            "required": ["user"]  # Champs obligatoires dans 'datas'
        }
    },
    "required": ["datas"]  # Champs obligatoires dans le schéma global
}

class UsersDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_add_user(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function


