from flask import request, jsonify, Blueprint
from services.materials import MaterialService
from entities.DTO.materials import Material
import connect_pg
from decorators.materials_decorator import MaterialsDecorators

# Création d'un Blueprint pour les routes liées aux absences
materials_bp = Blueprint('materials', __name__)

# Instanciation du service d'absences
materials_service = MaterialService()


#--------------------Récuperer toutes les equipements--------------------------------------#

@materials_bp.route('/materials', methods=['GET'])
def get_all_materials():
    """
    Récupérer toutes les équipements

    ---
   tags:
      - Materials
   responses:
      200:
        description: Liste des équipements récupérés depuis la base de données.
        examples:
          application/json: [
            {
                "equipment": "projecteur",
                "id": 4
            },
            {
                "equipment": "tablette",
                "id": 6
            },
            {
                "equipment": "PC portable Asus",
                "id": 8
            }
          ]
      500:
        description: Erreur serveur en cas de problème lors de la récupération des équipements.
    """
    
    try:
        material_list = materials_service.get_all_materials()
        return jsonify(material_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#------------------- Récuperer un équipment par son id -----------------------#
@materials_bp.route('/materials/<int:id_Material>', methods=['GET'])
def get_material(id_Material):
    """
Récupérer un équipement par son ID.

---
tags:
  - Materials
parameters:
  - in: path
    name: id_Material
    required: true
    description: L'identifiant unique de l'équipement à récupérer.
responses:
  200:
    description: Équipement récupéré avec succès.
    examples:
      application/json: [
        {
          "equipment": "projecteur",
          "id": 4
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération de l'équipement.
"""

    try:
        material = materials_service.get_material(id_Material)
        return jsonify(material), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#--------------------Créer un  equipement--------------------------------------#

@materials_bp.route('/materials', methods=['POST'])
@MaterialsDecorators.validate_json_material
def add_material():
    """
Créer un équipement.

---
tags:
  - Materials
parameters:
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            equipment:
              type: string
              description: Le nom de l'équipement à créer.
responses:
  201:
    description: L'équipement a été créé avec succès.
  400:
    description: Requête invalide ou données manquantes.
  500:
    description: Erreur serveur lors de la création de l'équipement.
"""

    try:
        
        donnees_equipement = request.json.get('datas', {})        
        message = materials_service.add_material(donnees_equipement)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": "Erreur lors de l'ajout de l'équipement : " + str(e)}), 500


#--------------------Supprimer un  equipement--------------------------------------#

@materials_bp.route('/materials/<int:id_material>', methods=['DELETE'])
def delete_material(id_material):
    """
    Supprimer un équipement.

    ---
    tags:
      - Materials
    parameters:
      - in: path
        name: id_material
        required: true
        type: integer
        description: L'identifiant unique de l'équipement à supprimer.
    responses:
      200:
        description: L'équipement a été supprimé avec succès.
      404:
        description: L'équipement spécifié n'existe pas.
      500:
        description: Erreur serveur lors de la suppression de l'équipement.
    """
    try:
        if not connect_pg.does_entry_exist("Materials", id_material):
            return jsonify({"message": "L'équiment spécifié n'existe pas."}), 404
        
        result, status_code = materials_service.delete_material(id_material)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression de l'équipement : {str(e)}"}), 500

#--------------------Modifier un  equipement--------------------------------------#
@materials_bp.route('/materials/<int:id_material>', methods=['PUT'])
@MaterialsDecorators.validate_json_material
def update_material(id_material):
    """
Mettre à jour un équipement.

---
tags:
  - Materials
parameters:
  - in: path
    name: id_material
    required: true
    type: integer
    description: L'identifiant unique de l'équipement à mettre à jour.
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            equipment:
              type: string
              description: La nouvelle valeur de l'équipement.
responses:
  201:
    description: L'équipement a été mis à jour avec succès.
  400:
    description: Données de l'équipement manquantes ou incorrectes.
  404:
    description: L'équipement spécifié n'existe pas.
  500:
    description: Erreur serveur lors de la mise à jour de l'équipement.
"""

    try:
        donnees_equipement = request.json.get('datas', {})        
        equipment = donnees_equipement['equipment']
                
        if not connect_pg.does_entry_exist("Materials", id_material):
            return jsonify({"message": "L'équipement spécifié n'existe pas."}), 404

        material = Material(
            id=id_material,
            equipment=equipment
        )

        message = materials_service.update_material(material)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": "Erreur lors de la mise à jour de l'équipement : " + str(e)}), 500
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