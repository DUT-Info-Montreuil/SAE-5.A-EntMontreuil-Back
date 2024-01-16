from flask import Blueprint, request, jsonify
from services.resources import ResourceService

resources_bp = Blueprint("resources_bp", __name__)
resource_service = ResourceService()

@resources_bp.route("/resources/<int:resource_id>", methods=["GET"])
def get_resource_by_id(resource_id):
    """
    Récupérer les informations d'une ressource.

    ---
    tags:
      - Resources
    parameters:
      - name: resource_id
        in: path
        required: true
        type: integer
        description: ID de la ressource
    responses:
      200:
        description: Succès
      404:
        description: Ressource non trouvée
      500:
        description: Erreur serveur
    """
    return resource_service.get_resource_by_id(resource_id)

@resources_bp.route("/resources", methods=["GET"])
def get_all_resources():
    """
    Récupérer toutes les ressources.

    ---
    tags:
      - Resources
    responses:
      200:
        description: Succès
      500:
        description: Erreur serveur
    """
    return resource_service.get_all_resources()

@resources_bp.route("/resources", methods=["POST"])
def add_resource():
    """
    Ajouter une ressource.

    ---
    tags:
      - Resources
    parameters:
      - name: body
        in: body
        required: true
        description: Données de la ressource à ajouter
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nom de la ressource
            id_Training:
              type: integer
              description: ID du parcours associé
            color:
              type: string
              description: Couleur de la ressource
    responses:
      200:
        description: Ressource ajoutée avec succès
      409:
        description: Une ressource avec ce nom et ce parcours existe déjà
      500:
        description: Erreur serveur
    """
    data = request.json
    return resource_service.add_resource(data)

@resources_bp.route("/resources/<int:resource_id>", methods=["PUT"])
def update_resource(resource_id):
    """
    Mettre à jour une ressource.

    ---
    tags:
      - Resources
    parameters:
      - name: resource_id
        in: path
        required: true
        type: integer
        description: ID de la ressource à mettre à jour
      - name: body
        in: body
        required: true
        description: Données de la ressource à mettre à jour
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nouveau nom de la ressource
            id_Training:
              type: integer
              description: Nouvel ID du parcours associé
            color:
              type: string
              description: Nouvelle couleur de la ressource
    responses:
      200:
        description: Ressource mise à jour avec succès
      404:
        description: Ressource non trouvée ou aucune modification effectuée
      500:
        description: Erreur serveur
    """
    data = request.json
    data["id"] = resource_id
    return resource_service.update_resource(data)

@resources_bp.route("/resources/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    """
    Supprimer une ressource.

    ---
    tags:
      - Resources
    parameters:
      - name: resource_id
        in: path
        required: true
        type: integer
        description: ID de la ressource à supprimer
    responses:
      200:
        description: Ressource supprimée avec succès
      404:
        description: Ressource non trouvée ou déjà supprimée
      500:
        description: Erreur serveur
    """
    return resource_service.delete_resource(resource_id)

@resources_bp.route("/resources/training/<int:id_Training>", methods=["GET"])
def get_resource_by_id_training(id_Training):
    """
    Récupérer les ressources par ID de parcours.

    ---
    tags:
      - Resources
    parameters:
      - name: id_Training
        in: path
        required: true
        type: integer
        description: ID du parcours
    responses:
      200:
        description: Succès
      500:
        description: Erreur serveur
    """
    return resource_service.get_resource_by_id_training(id_Training)
