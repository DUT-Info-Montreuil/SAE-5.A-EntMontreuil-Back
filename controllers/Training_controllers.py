from flask import request, jsonify, Blueprint
from services.training import TrainingService  # Importer le service de gestion des parcours
import connect_pg
from decorators.trainings_decorator import TrainingsDecorators
from entities.DTO.trainings import Training
# Création d'un Blueprint pour les routes liées aux parcours
training_bp = Blueprint('trainings', __name__)


training_service = TrainingService()

#---------------- récuperer tout les trainings -------------------#
@training_bp.route('/trainings', methods=['GET'])
def get_all_trainings():
    """
Récupérer tous les parcours.

---
tags:
  - Trainings
parameters:
  - name: output_format
    in: /trainings?output_format=model
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "model"
    enum: ["DTO", "model"]
  - name: id_Degree
    in: /trainings?is_degree=1
    description: L'identifiant de la formation pour filtrer les parcours (optionnel).
    required: false
    type: integer
responses:
  200:
    description: Liste des parcours récupérés depuis la base de données (model).
    examples:
      application/json:
        [
            {
                "degree_name": "GAGO",
                "id": 2,
                "id_Degree": 2,
                "name": "Formation2"
            },
            {
                "degree_name": "INFO",
                "id": 2,
                "id_Degree": 1,
                "name": "PARCOUR A"
            }
        ]
    
  500:
    description: Erreur serveur en cas de problème lors de la récupération des parcours.
"""

    try:
        output_format = request.args.get('output_format', default='model', type=str)
        id_Degree = request.args.get('id_Degree', default=None, type=int)  # Ajout de la récupération de id_degree
        
        # Appel de la fonction get_all_trainings avec ou sans id_degree en fonction de sa présence
        if id_Degree is not None:
            trainings = training_service.get_all_trainings(output_format, id_Degree=id_Degree)
        else:
            trainings = training_service.get_all_trainings(output_format)
        
        return jsonify(trainings), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({"message": str(e)}), 500


#--------------------ajouter  un  parcours--------------------------------------#
@training_bp.route('/trainings', methods=['POST'])
@TrainingsDecorators.validate_json_add_training
def add_training():

    """
    Add a new training.
    ---
    tags:
      - Trainings
    parameters:
      - in: body
        name: training
        description: Training object to be added.
        required: true
        schema:
          $ref: '#/definitions/TrainingInput'
    responses:
      200:
        description: Training successfully added.
        schema:
          $ref: '#/definitions/SuccessMessage'
      400:
        description: Bad request or validation error.
      500:
        description: Server error in case of a problem during training addition.
    definitions:
      TrainingInput:
        type: object
        properties:
          datas:
            type: object
            properties:
              name:
                type: string
                description: The name of the training.
              id_Degree:
                type: integer
                description: The ID of the degree associated with the training.
        required:
          - datas
          - name
          - id_Degree
        additionalProperties: false

      SuccessMessage:
        type: object
        properties:
          message:
            type: string
            description: Confirmation message.
        required:
          - message
    """
    try:
        json_data = request.json
        training_data = json_data['datas']

        # Valide que la formation spécifiée existe
        if not connect_pg.does_entry_exist("Promotions", training_data['id_Promotion']):
            return jsonify({"message": "La promotion spécifiée n'existe pas."}), 400

        # Crée un objet Training (DTO) à partir des données JSON
        training = Training(
            id=0,
            name=training_data["name"],
            id_Promotion=training_data["id_Promotion"],
            semester=training_data["semester"]
        )

        # Appelle le service pour ajouter la formation
        message = training_service.add_training(training)

        # Retourne un message de confirmation
        return jsonify(message)

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    
#-------------------- Récuperer un parcours via son id ----------------------#
@training_bp.route('/trainings/<int:id_training>', methods=['GET'])
def get_training(id_training):
    """
Récupère les détails d'un parcours spécifique par son ID.

Cette route permet de récupérer les informations détaillées d'un parcours en spécifiant son ID.

---
tags:
  - Trainings
parameters:
  - name: id_training
    in: path
    description: L'identifiant unique du parcours à récupérer.
    required: true
    type: integer
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "model"
    enum: ["DTO", "model"]
responses:
  200:
    description: Informations détaillées du parcours récupérées avec succès.
    examples:
      application/json:
        {
            "degree_name": "GAGO",
            "id": 2,
            "id_Degree": 2,
            "name": "Formation2"
        }
  404:
    description: Parcours non trouvé en cas d'ID inexistant.
    examples:
      application/json: {"message": "Le parcours spécifié n'existe pas."}
  500:
    description: Erreur serveur en cas de problème lors de la récupération du parcours.
    examples:
      application/json: {"message": "Erreur lors de la récupération du parcours : [message d'erreur]"}
"""

    if not connect_pg.does_entry_exist("Trainings", id_training):
        return jsonify({"message": "Le parcours spécifié n'existe pas."}), 404
    try:
        output_format = request.args.get('output_format',default='model', type=str)
        training = training_service.get_training(id_training,output_format)
        return jsonify(training), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération du parcours : {str(e)}"}), 500


@training_bp.route('/trainings/<int:id_training>', methods=['PUT'])
@TrainingsDecorators.validate_json_update_training
def update_training(id_training):
    """
Met à jour un parcours existant dans la base de données par son ID.

Cette route permet de mettre à jour les informations d'un parcours en spécifiant son ID.

---
tags:
  - Trainings
parameters:
  - name: id_training
    in: path
    description: L'identifiant unique du parcours à mettre à jour.
    required: true
    type: integer
  - name: body
    in: body
    description: Les données du parcours à mettre à jour au format JSON.
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            name:
              type: string
              description: Le nouveau nom du parcours.
            id_Degree:
              type: integer
              description: L'identifiant de la formation associée au parcours.
responses:
  200:
    description: Message de réussite de la mise à jour.
    examples:
      application/json: {"message": "Parcours mis à jour avec succès."}
  400:
    description: Requête incorrecte en cas de données manquantes ou mal formatées.
    examples:
      application/json: {"message": "Données manquantes ou mal formatées."}
  404:
    description: Parcours non trouvé en cas d'ID inexistant.
    examples:
      application/json: {"message": "Le parcours spécifié n'existe pas."}
  500:
    description: Erreur serveur en cas de problème lors de la mise à jour du parcours.
    examples:
      application/json: {"message": "Erreur lors de la mise à jour du parcours : [message d'erreur]"}
"""

    try:
        json_data = request.json

        if not connect_pg.does_entry_exist("Trainings", id_training):
            return jsonify({"message": "Le parcours spécifié n'existe pas."}), 404
        training_data = json_data['datas']
        # Crée un objet Training DTO à partir des données JSON
        training = Training(
            id=id_training,
            name=training_data['name'],
            id_Promotion=training_data['id_Promotion'],
            semester=training_data["semester"]
        )
        message= training_service.update_training(training)
        return jsonify(message)
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour du parcours : {str(e)}"}), 500


@training_bp.route('/trainings/<int:id_training>', methods=['DELETE'])
def delete_training(id_training):
    """
Supprime un parcours existant de la base de données par son ID.

Cette route permet de supprimer un parcours en spécifiant son ID.

---
tags:
  - Trainings
parameters:
  - name: id_training
    in: path
    description: L'identifiant unique du parcours à supprimer.
    required: true
    type: integer
responses:
  200:
    description: Message de réussite de la suppression.
    examples:
      application/json: {"message": "Parcours supprimé avec succès."}
  404:
    description: Parcours non trouvé en cas d'ID inexistant.
    examples:
      application/json: {"message": "Le parcours spécifié n'existe pas."}
  500:
    description: Erreur serveur en cas de problème lors de la suppression du parcours.
    examples:
      application/json: {"message": "Erreur lors de la suppression du parcours : [message d'erreur]"}
"""

    try:
        result = training_service.delete_training(id_training)
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression du parcours : {str(e)}"}), 500


#-------------------get_training_by_id_promotion_and_semester

@training_bp.route('/trainings/<int:id_promotion>/<int:semester>', methods=['GET'])
def get_training_by_id_promotion_and_semester(id_promotion,semester):
  
    try:
        
        trainings = training_service.get_training_by_id_promotion_and_semester(id_promotion, semester)
        return jsonify(trainings), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({"message": str(e)}), 500
      
#---------------- récuperer tout les trainings -------------------#
@training_bp.route('/trainings_gb', methods=['GET'])
def get_all_trainings_gb():
    """
Récupérer tous les parcours.

---
tags:
  - Trainings
parameters:
  - name: output_format
    in: /trainings?output_format=model
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "model"
    enum: ["DTO", "model"]
  - name: id_Degree
    in: /trainings?is_degree=1
    description: L'identifiant de la formation pour filtrer les parcours (optionnel).
    required: false
    type: integer
responses:
  200:
    description: Liste des parcours récupérés depuis la base de données (model).
    examples:
      application/json:
        [
            {
                "degree_name": "GAGO",
                "id": 2,
                "id_Degree": 2,
                "name": "Formation2"
            },
            {
                "degree_name": "INFO",
                "id": 2,
                "id_Degree": 1,
                "name": "PARCOUR A"
            }
        ]
    
  500:
    description: Erreur serveur en cas de problème lors de la récupération des parcours.
"""

    try:

        trainings = training_service.get_all_trainings_gb()
        
        return jsonify(trainings), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({"message": str(e)}), 500

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