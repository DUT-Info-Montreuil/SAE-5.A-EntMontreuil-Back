from functools import wraps
from flask import Flask, request, jsonify
from jsonschema import validate

# Schéma JSON pour la validation
schema__add_course = {
  "type": "object",
  "properties": {
    "startTime": {"type": "string", "format": "time"},
    "endTime": {"type": "string", "format": "time"},
    "dateCourse": {"type": "string", "format": "date"},
    "control": {"type": "boolean"},
    "id_resource": {"type": "integer"},
    "id_tp": {"type": ["integer", "null"]},
    "id_td": {"type": ["integer", "null"]},
    "id_promotion": {"type": ["integer", "null"]},
    "id_training": {"type": ["integer", "null"]}
  },
  "required": ["startTime", "endTime", "dateCourse", "control", "id_resource"],
  "additionalProperties": False
}

schema__update_course = {
  "type": "object",
  "properties": {
    "startTime": {"type": "string", "format": "time"},
    "endTime": {"type": "string", "format": "time"},
    "dateCourse": {"type": "string", "format": "date"},
    "control": {"type": "string"},
    "id_resource": {"type": "integer"},
    "id_tp": {"type": ["integer", "null"]},
    "id_td": {"type": ["integer", "null"]},
    "id_promotion": {"type": ["integer", "null"]},
    "id_training": {"type": ["integer", "null"]}
  },
  "additionalProperties": False
}

class CoursesDecorators : 
    # Décorateur pour la validation JSON
    def validate_json_add_course(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema__add_course)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    def validate_json_update_course(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Le contenu de la requête n\'est pas au format JSON'}), 400
            try:
                data = request.get_json()
                # Validation du JSON avec le schéma
                validate(instance=data, schema=schema__update_course)
                # Si la validation réussit, exécute la fonction de vue
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'JSON invalide - {}'.format(str(e))}), 400
        return decorated_function
    
    


