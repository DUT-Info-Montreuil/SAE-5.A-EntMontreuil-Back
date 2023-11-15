from flask import request, jsonify, Blueprint
from services.materials import MaterialService
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
        # Récupérez les données de l'équipement depuis le JSON de la requête
        donnees_equipement = request.json.get('datas', {})

        # Vérifiez la présence des données de l'équipement
        if not donnees_equipement or 'equipment' not in donnees_equipement:
            return jsonify({"message": "Données de l'équipement manquantes ou incomplètes"}), 400

        # Appelez le service MaterialService pour ajouter l'équipement
        message = materials_service.add_material(donnees_equipement)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": "Erreur lors de l'ajout de l'équipement : " + str(e)}), 500
    


@materials_bp.route('/materials/<int:id_material>', methods=['DELETE'])
def delete_material(id_material):
    try:
        result, status_code = materials_service.delete_material(id_material)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression de l'équipement : {str(e)}"}), 500
