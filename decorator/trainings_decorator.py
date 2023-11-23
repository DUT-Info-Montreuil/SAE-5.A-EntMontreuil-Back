from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema_add_training = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "id_Degree": {"type": "integer"},
                    
                
            },
            "required": ["name", "id_Degree" ],  # Champs obligatoires dans 'datas'
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}


schema_update_training = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "id_Degree": {"type": "integer"},
            },
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

class TrainingsDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_add_training(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_add_training)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    
    def validate_json_update_training(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_update_training)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function


