from flask import request, jsonify, Blueprint
from services.materials import MaterialService
from entities.DTO.materials import Material
import connect_pg

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
      - Equipements
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
    Récupérer un équipement par son id

    ---
   tags:
      - Equipements
   responses:
      200:
        description: équipement récupérer
        examples:
          application/json: [
            {
                "equipment": "projecteur",
                "id": 4
            },
          ]
      500:
        description: Erreur serveur en cas de problème lors de la récupération des équipements.
    """
    try:
        material = materials_service.get_material(id_Material)
        return jsonify(material), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#--------------------Créer un  equipement--------------------------------------#

@materials_bp.route('/materials', methods=['POST'])
def add_material():
    """
    Créer un équipement.

    ---
    tags:
      - Equipements
    parameters:
      - in: body
        name: datas
        required: true
        schema:
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
        if not isinstance(donnees_equipement['equipment'], str):
            return jsonify({"message": "Le champ 'equipment' doit être une chaîne de caractères (string)"}), 400
        
        
        if not donnees_equipement or 'equipment' not in donnees_equipement:
            return jsonify({"message": "Données de l'équipement manquantes ou incomplètes"}), 400


        
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
      - Equipements
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
def update_material(id_material):
    """
    Mettre à jour un équipement.

    ---
    tags:
      - Equipements
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

        if not donnees_equipement or 'equipment' not in donnees_equipement:
            return jsonify({"message": "Données de l'équipement manquantes ou incomplètes"}), 400
        
        equipment = donnees_equipement['equipment']
        
        if not isinstance(equipment, str):
            return jsonify({"message": "Le champ 'equipment' doit être une chaîne de caractères (string)"}), 400
        
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
