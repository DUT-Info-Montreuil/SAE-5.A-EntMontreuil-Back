from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema__add_absence = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "justify": {"type": "object",},
                "reason" : {"type" : "string"}
            },
            "required": ["justify", "reason"],  # Champs obligatoires dans 'datas'
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

schema__update_absence = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "justify": {"type": "object",},
                "reason" : {"type" : "string"}
            },
            "additionalProperties": False  # Aucun autre attribut ne peut être ajouté 
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

class AbsencesDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_add_absence(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema__add_absence)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    def validate_json_update_absence(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema__update_absence)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    


