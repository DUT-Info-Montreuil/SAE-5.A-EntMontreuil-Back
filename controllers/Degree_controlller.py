from flask import request, jsonify, Blueprint
from services.degrees import DeegreeService
from entities.DTO.degrees import Degrees
import connect_pg
from decorator.degrees_decorator import DegreesDecorators

degrees_bp = Blueprint('degrees', __name__)

degree_service = DeegreeService()

@degrees_bp.route('/degrees', methods=['GET'])
def get_all_degrees():
    """
    Récupérer toutes les informations sur les Formation.

    ---
    tags:
      - Degree
    parameters:
      - name: output_format
        in: query
        description: Le format de sortie des données (par défaut "model").
        required: false
        type: string
        default: "dto"
        enum: ["model", "dto"]
    responses:
      200:
        description: Liste des Formation récupérés depuis la base de données.
      500:
        description: Erreur serveur en cas de problème lors de la récupération des Formation.
    """
    try:
        output_format = request.args.get('output_format', 'model')
        degrees = degree_service.get_all_degrees(output_format)
        return degrees
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@degrees_bp.route('/degrees', methods=['POST'])
@DegreesDecorators.validate_json_degree
def create_degree():
    """
Créer une nouvelle Formation.

---
tags:
  - Degree
parameters:
  - in: body
    name: degree_data
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            name:
              type: string
              description: Le nom de la formation.
responses:
  201:
    description: Nouvelle formation créée avec succès.
  400:
    description: Données invalides fournies.
  500:
    description: Erreur serveur lors de la création de la formation.
"""

    try:
        data = request.json.get('datas', {})
        name = data.get('name')
        degree = Degrees(id=0, name=name)
        result = degree_service.create_degree(degree)

        if "error" in result:
            return jsonify(result), 500

        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degrees_bp.route('/degrees/<int:degree_id>', methods=['DELETE'])
def delete_degree(degree_id):
    """
    Supprime une formation par son ID.

    Cette route permet de supprimer une formation en fournissant son ID.

    ---
    tags:
      - Degree
    parameters:
      - name: degree_id
        in: path
        description: ID de la formation à supprimer
        required: true
        type: integer
    responses:
      200:
        description: Formation supprimée avec succès
      404:
        description: Formation non trouvée
      500:
        description: Erreur interne du serveur
    """
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.delete_degree(degree_id)
    return jsonify(result)

# Route pour récupérer une formation par son ID
@degrees_bp.route('/degrees/<int:degree_id>', methods=['GET'])
def get_degree_by_id(degree_id):
    """
Récupère une formation par son ID.

Cette route permet de récupérer une formation en fournissant son ID.

---
tags:
  - Degree
parameters:
  - name: degree_id
    in: path
    description: ID de la formation à récupérer
    required: true
    type: integer
  - name: output_format
    in: query
    description: Format de sortie des données (par défaut "model")
    required: false
    type: string
    default: "model"
    enum: ["model", "dto"]
responses:
  200:
    description: Formation récupérée avec succès
  404:
    description: Formation non trouvée
  500:
    description: Erreur interne du serveur
"""

    output_format = request.args.get('output_format', 'model')
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.get_degree_by_id(degree_id, output_format)
    return result

# Route pour mettre à jour une formation
@degrees_bp.route('/degrees/<int:degree_id>', methods=['PUT'])
@DegreesDecorators.validate_json_degree
def update_degree(degree_id):
    """
Met à jour une formation par son ID.

Cette route permet de mettre à jour le nom d'une formation en fournissant son ID.

---
tags:
  - Degree
parameters:
  - name: degree_id
    in: path
    description: ID de la formation à mettre à jour
    required: true
    type: integer
  - in: body
    name: data
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            name:
              type: string
              description: Nouveau nom de la formation
              example: "Nouveau nom de formation"
responses:
  200:
    description: Formation mise à jour avec succès
  400:
    description: Requête invalide ou données manquantes
  404:
    description: Formation non trouvée
  500:
    description: Erreur interne du serveur
"""

    data = request.json.get('datas', {})
    new_name = data.get('name')
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.update_degree(degree_id, new_name)
    return jsonify(result)
