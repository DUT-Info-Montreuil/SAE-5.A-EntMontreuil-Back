from flask import request, jsonify, Blueprint
from services.classroom import ClassroomService
from entities.DTO.materials import Material
import connect_pg
Classroom_bp = Blueprint('classrooms', __name__)


Classroom_service = ClassroomService()
#------------------------------- récuperer toute les salles de classe -------------------#
@Classroom_bp.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    """
Récupérer toutes les salles de classe.

---
tags:
  - Salles de classe
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
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        },
        {
            "id": 2,
            "name": "Salle2",
            "capacity": 40,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 8
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 12
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_classroom=None)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
 #------------------------------- chercher  une salle de classe en focntion de critère -------------------#   
@Classroom_bp.route('/classrooms/<int:id_Classroom>', methods=['GET'])
def get_classroom(id_Classroom):
    """
Récupérer une salle de classe via son id
---
tags:
  - Salles de classe
parameters:
  - name: id_Classroom
    in: path
    description: L'identifiant unique de la salle de classe à laquelle ajouter les équipements.
    required: true
    type: integer
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "dto"
    enum: ["model", "dto"]
responses:
  200:
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_Classroom,)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

# Add a new route for searching classrooms with criteria
@Classroom_bp.route('/classrooms/search', methods=['GET'])
def search_classrooms():
    """
    Rechercher des salles de classe en fonction de critères spécifiés.
    ---
    tags:
      - Salles de classe
    parameters:
      - name: name
        in: query
        description: Le nom de la salle de classe à rechercher (optionnel).
        required: false
        type: string
      - name: capacity
        in: query
        description: La capacité de la salle de classe à rechercher (optionnel).
        required: false
        type: integer
      - name: equipment
        in: query
        description: Le matériel présent dans la salle de classe à rechercher (optionnel).
        required: false
        type: string
      - name: output_format
        in: query
        description: Le format de sortie des données (par défaut "model").
        required: false
        type: string
        default: "dto"
        enum: ["model", "dto"]
    responses:
      200:
        description: Liste des salles de classe récupérées depuis la base de données.
        examples:
          application/json: [
            {
                "id": 1,
                "name": "Salle1",
                "capacity": 30,
                "materials": [
                  {
                    "id": 1,
                    "equipment": "Ordinateur portable",
                    "quantity": 10
                  },
                  {
                    "id": 2,
                    "equipment": "Tableau blanc",
                    "quantity": 5
                  }
                ]
            },
            # ... (other classrooms)
          ]
      500:
        description: Erreur serveur en cas de problème lors de la recherche des salles de classe.
    """
    try:
        # Extract query parameters
        name = request.args.get('name', None)
        capacity = request.args.get('capacity', None)
        equipment = request.args.get('equipment', None)
        output_format = request.args.get('output_format', 'model')

        # Call the search function in your ClassroomService
        classrooms = Classroom_service.search_classrooms(name, capacity, equipment, output_format)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
 ##------------------------------- ajouter un equipement dans une salle -----------------------#   
@Classroom_bp.route('/classrooms/<int:id_Classroom>/equipments', methods=['POST'])
def add_equipments_to_classroom(id_Classroom ):
    """
Ajouter des équipements à une salle de classe.

---
tags:
  - Salles de classe
parameters:
  - name: id_Classroom
    in: path
    description: L'identifiant unique de la salle de classe à laquelle ajouter les équipements.
    required: true
    type: integer
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        equipment_ids:
          type: array
          description: La liste des IDs des équipements à ajouter.
          items:
            type: integer
          example: [1, 2, 3]
responses:
  201:
    description: Les équipements ont été ajoutés avec succès à la salle de classe.
  400:
    description: Requête invalide ou données manquantes.
  404:
    description: La salle de classe spécifiée n'existe pas.
  500:
    description: Erreur serveur lors de l'ajout des équipements.

Example:
  Pour ajouter plusieurs équipements à une salle de classe avec l'ID 1, envoyez une requête POST avec les données JSON
  comme indiqué ci-dessus.
"""

    try:
        equipment_ids = request.json.get('equipment_ids', [])
        
        if not connect_pg.does_entry_exist("Classroom", id_Classroom):
            return jsonify({"message": "La salle de classe spécifiée n'existe pas."}), 404

        if not equipment_ids:
            return jsonify({"message": "Aucun équipement spécifié à ajouter."}), 400

        Classroom_service.add_equipments_to_classroom(id_Classroom, equipment_ids)

        return jsonify({"message": "Les équipements ont été ajoutés avec succès à la salle de classe"}), 201
    except Exception as e:
        return jsonify({"message": f"Erreur lors de l'ajout des équipements : {str(e)}"}), 500

#----------------- modifer la quantité d'un equipement dans une salle  ----------------------#

@Classroom_bp.route('/classrooms/<int:id_classroom>/equipments/<int:id_equipment>', methods=['PUT'])
def update_classroom_equipment_quantity(id_classroom, id_equipment):
    """
    Mettre à jour la quantité d'un équipement dans une salle de classe.

    ---
    tags:
      - Salles de classe
    parameters:
      - name: id_classroom
        in: path
        description: L'identifiant unique de la salle de classe.
        required: true
        type: integer
      - name: id_equipment
        in: path
        description: L'identifiant unique de l'équipement.
        required: true
        type: integer
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            new_quantity:
              type: integer
              description: La nouvelle quantité de l'équipement.
              example: 5
    responses:
      200:
        description: La quantité de l'équipement a été mise à jour avec succès.
      400:
        description: Requête invalide ou données manquantes.
      404:
        description: La salle de classe ou l'équipement spécifié n'existe pas.
      500:
        description: Erreur serveur lors de la mise à jour de la quantité de l'équipement.
    """
    try:
        new_quantity = request.json.get('new_quantity', None)

        if new_quantity is None:
            return jsonify({"message": "La nouvelle quantité est requise."}), 400

        Classroom_service.update_equipment_quantity(id_classroom, id_equipment, new_quantity)

        return jsonify({"message": "La quantité de l'équipement a été mise à jour avec succès."}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour de la quantité de l'équipement : {str(e)}"}), 500
    
#-------------------- supprimer un equipement d'une salle
@Classroom_bp.route('/classrooms/<int:id_classroom>/equipments/<int:id_equipment>', methods=['DELETE'])
def remove_equipment(id_classroom, id_equipment):
    """
    Supprimer un équipement d'une salle de classe.

    ---
    tags:
      - Salles de classe
    parameters:
      - name: id_classroom
        in: path
        description: L'identifiant unique de la salle de classe.
        required: true
        type: integer
      - name: id_equipment
        in: path
        description: L'identifiant unique de l'équipement à supprimer.
        required: true
        type: integer
    responses:
      200:
        description: Équipement supprimé avec succès.
      404:
        description: Salle de classe ou équipement non trouvé.
      500:
        description: Erreur serveur lors de la suppression de l'équipement.
    """
    try:
        result = Classroom_service.remove_equipment_from_classroom(id_classroom, id_equipment)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#------------------------------ supprimer une classe -----------------------#

@Classroom_bp.route('/classrooms/<int:id_classroom>', methods=['DELETE'])
def delete_classroom(id_classroom):
    """
    Supprimer une salle de classe et toutes les données associées.
    ---
    tags:
      - Salles de classe
    parameters:
      - name: id_classroom
        in: path
        description: L'identifiant unique de la salle de classe à supprimer.
        required: true
        type: integer
    responses:
      200:
        description: Salle de classe et données associées supprimées avec succès.
      404:
        description: Salle de classe non trouvée.
      500:
        description: Erreur serveur lors de la suppression de la salle de classe.
    """
    try:
        result = Classroom_service.delete_classroom(id_classroom)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

