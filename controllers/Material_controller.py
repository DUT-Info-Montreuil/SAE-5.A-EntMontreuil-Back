from flask import request, jsonify, Blueprint
from services.materials import MaterialService
import connect_pg

# Création d'un Blueprint pour les routes liées aux absences
materials_bp = Blueprint('materials', __name__)

# Instanciation du service d'absences
materials_service = MaterialService()


#--------------------Récuperer toutes les equipements--------------------------------------#

@materials_bp.route('/materials', methods=['GET'])
def get_all_absences():
    
    try:
        material_list = materials_service.get_all_materials()
        return jsonify(material_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
