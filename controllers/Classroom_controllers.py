from flask import request, jsonify, Blueprint
from services.classroom import ClassroomService
from entities.DTO.classroom import Classroom
import connect_pg
from decorators.classrooms_decorator import ClassroomsDecorators
Classroom_bp = Blueprint('classrooms', __name__)


Classroom_service = ClassroomService()
#------------------------------- récuperer toute les salles de classe -------------------#
@Classroom_bp.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    """
Récupérer toutes les salles de classe.

---
tags:
  - Classrooms
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
  - Classrooms
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
        if not connect_pg.does_entry_exist("Classroom", id_Classroom):
          return jsonify({"message": "La salle de classe spécifiée n'existe pas."}), 404

        output_format = request.args.get('output_format', 'model')  
        classrooms = Classroom_service.get_all_classrooms(output_format,id_Classroom,)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@Classroom_bp.route('/classrooms/search', methods=['GET'])
def search_classrooms():
    """
    Rechercher des salles de classe en fonction de critères spécifiés.
    ---
    tags:
      - Classrooms
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
        description: L'ID de l'équipement présent dans la salle de classe à rechercher (optionnel).
        required: false
        type: integer
      - name: min_quantity
        in: query
        description: La quantité minimale de l'équipement à rechercher (optionnel).
        required: false
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
        min_quantity = request.args.get('min_quantity', None)
        output_format = request.args.get('output_format', 'model')

        # Call the search function in your ClassroomService
        classrooms = Classroom_service.search_classrooms(name, capacity, equipment, min_quantity, output_format)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    
 ##------------------------------- ajouter un equipement dans une salle -----------------------#   
@Classroom_bp.route('/classrooms/<int:id_Classroom>/equipments', methods=['POST'])
@ClassroomsDecorators.validate_json_add_equipement_classroom
def add_equipments_to_classroom(id_Classroom ):
    """
Ajouter des équipements à une salle de classe.

---
tags:
  - Classrooms
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
        datas:
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
        
        data = request.json.get('datas', {})
        equipment_ids = data.get('equipment_ids', [])
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
@ClassroomsDecorators.validate_json_update_equipment_classroom
def update_classroom_equipment_quantity(id_classroom, id_equipment):
    """
Mettre à jour la quantité d'un équipement dans une salle de classe.

---
tags:
  - Classrooms
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
    name: datas
    required: true
    schema:
      type: object
      properties:
        datas:
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
        data = request.json.get('datas', {})
        new_quantity = data.get('new_quantity')

        Classroom_service.update_equipment_quantity(id_classroom, id_equipment, new_quantity)

        return jsonify({"message": "La quantité de l'équipement a été mise à jour avec succès."}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour de la quantité de l'équipement : {str(e)}"}), 500
    
#-------------------- supprimer un equipement d'une salle
@Classroom_bp.route('/classrooms/<int:id_classroom>/equipments/<int:id_equipment>', methods=['DELETE'])
def remove_equipment_classroom(id_classroom, id_equipment):
    """
    Supprimer un équipement d'une salle de classe.

    ---
    tags:
      - Classrooms
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
      - Classrooms
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
        if not connect_pg.does_entry_exist("Students", id_classroom):
          return jsonify({"message": "La salle de classe spécifiée n'existe pas."}), 404
        result = Classroom_service.delete_classroom(id_classroom)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@Classroom_bp.route('/classrooms', methods=['POST'])
@ClassroomsDecorators.validate_json_add_classroom
def create_classroom():
    """
Créer une nouvelle salle de classe.

---
tags:
  - Classrooms
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
            name:
              type: string
              description: Le nom de la salle de classe.
            capacity:
              type: integer
              description: La capacité de la salle de classe.
responses:
  201:
    description: Nouvelle salle de classe créée avec succès.
  400:
    description: Données invalides fournies.
  500:
    description: Erreur serveur lors de la création de la salle de classe.
"""

    try:
        data = request.json.get('datas', {})
        name = data.get('name')
        capacity = data.get('capacity')       
        classroom=Classroom(
                            id=0,
                            name=name,
                            capacity=capacity
        )
        result = Classroom_service.create_classroom(classroom)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@Classroom_bp.route('/classrooms/<int:id_classroom>', methods=['PUT'])
def update_classroom(id_classroom):
    """
    Modifier une salle de classe.

    ---
    tags:
      - Classrooms
    parameters:
      - name: id_classroom
        in: path
        description: L'identifiant unique de la salle de classe à modifier.
        required: true
        type: integer
      - in: body
        name: datas
        required: true
        schema:
          type: object
          properties:
            datas:
              type: object
              properties:
                name:
                  type: string
                  description: Le nouveau nom de la salle de classe (optionnel).
                capacity:
                  type: integer
                  description: La nouvelle capacité de la salle de classe (optionnel).
    responses:
      200:
        description: Salle de classe modifiée avec succès.
      400:
        description: Données invalides fournies.
      404:
        description: Salle de classe non trouvée.
      500:
        description: Erreur serveur lors de la modification de la salle de classe.
    """
    try:
        data = request.json.get('datas', {})
        name = data.get('name', None)
        capacity = data.get('capacity', None)

        # Validation : Vérifiez si le nom est un chiffre ou si la capacité est une chaîne de caractères
        if name is not None and not isinstance(name, str):
            return jsonify({"error": "Le nom doit être une chaîne de caractères."}), 400
        if capacity is not None and not isinstance(capacity, int):
            return jsonify({"error": "La capacité doit être un nombre entier."}), 400

        result = Classroom_service.update_classroom(id_classroom, name, capacity)

        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
