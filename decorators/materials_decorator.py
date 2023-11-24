from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema_material = {
    "type": "object",
    "properties": {
        "datas": {
            "type": "object",
            "properties": {
                "equipment": {"type": "string", "minLength": 1}
            },
            "required": ["equipment"],  # Champs obligatoires dans le schéma global
            "additionalProperties": False  
        }
    },
    "required": ["datas"],  # Champs obligatoires dans le schéma global
    "additionalProperties": False  
}

class MaterialsDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_material(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema_material)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    


