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
    
    try:
        material_list = materials_service.get_all_materials()
        return jsonify(material_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500



#--------------------Créer un  equipement--------------------------------------#

@materials_bp.route('/materials', methods=['POST'])
def add_material():
    try:
        
        donnees_equipement = request.json.get('datas', {})

        
        if not donnees_equipement or 'equipment' not in donnees_equipement:
            return jsonify({"message": "Données de l'équipement manquantes ou incomplètes"}), 400


        
        message = materials_service.add_material(donnees_equipement)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": "Erreur lors de l'ajout de l'équipement : " + str(e)}), 500
    
#--------------------Supprimer un  equipement--------------------------------------#

#--------------------Supprimer un  equipement--------------------------------------#

@materials_bp.route('/materials/<int:id_material>', methods=['DELETE'])
def delete_material(id_material):
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
