from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema_add_classroom = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "capacity": {"type": "integer", "minimum": 1}
            },
            "required": ["name", "capacity"],  # Champs obligatoires dans le schéma global
            "additionalProperties": False  
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

schema_update_equipment_classroom = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "new_quantity": {"type": "integer", "minimum": 1}
            },
            "required": ["new_quantity"],  # Champs obligatoires dans le schéma global
            "additionalProperties": False  
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

schema_add_equipement_classroom = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "equipment_ids": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "minItems": 1  # Au moins un élément dans la liste est requis
                }
            },
            "required": ["equipment_ids"],  # Champ obligatoire dans 'datas'
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté à 'datas'
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  # Aucun autre attribut ne peut être ajouté à 'datas'
}

class ClassroomsDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_update_equipment_classroom(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_update_equipment_classroom)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    
    def validate_json_add_classroom(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_add_classroom)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    def validate_json_add_equipement_classroom(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_add_equipement_classroom)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    


