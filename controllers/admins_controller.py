from flask import request, jsonify, Blueprint
from services.admins import AdminsService , ValidationError 
import json

# Création d'un Blueprint pour les routes liées 
admins_bp = Blueprint('admins', __name__)

# Instanciation du service
admins_service = AdminsService()

#-----------get all admins--------------
@admins_bp.route('/admins', methods=['GET'])
def get_all_admins():
    try:
        output_format = request.args.get('output_format' , default='dto' , type=str)
        valid_format = ['dto' , 'model']
        if output_format not in valid_format :
            return jsonify({'error': "Invalid output_format (valid output_format is model & dto)"}), 400
        all_admins = admins_service.get_all_admins(output_format).json
        return jsonify(all_admins)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
#-----------get one admin--------------
@admins_bp.route('/admins/<int:id>', methods=['GET'])
def get_one_admin(id):
    try:
        output_format = request.args.get('output_format' , default='dto' , type=str)
        valid_format = ['dto' , 'model']
        if output_format not in valid_format :
            return jsonify({'error': "Invalid output_format (valid output_format is model & dto)"}), 400
        admin = admins_service.get_admin(id,output_format)
        return jsonify(admin)
    except ValidationError as e :
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
#----------------add admins------------
@admins_bp.route('/admins/add', methods=['POST'])
def add_admin() :   
    try :
        json_data = request.json
        message, status_code = admins_service.add_admins(json_data)
        return message, status_code
    except ValidationError as e :
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#-------------delete admins--------------------
@admins_bp.route('/admins/remove/<int:id_admin>', methods=['DELETE'])
def delete_admin(id_admin):
    try:
        message, status_code = admins_service.delete_admin(id_admin)
        return message, status_code
    except ValidationError as e :
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#-------------update admins -----------------------
@admins_bp.route('/admins/update/<int:id_admin>', methods=['PATCH'])
def update_admin(id_admin):
    try:
        json_data = request.json
        message, status_code = admins_service.update_admins(id_admin, json_data)
        return message, status_code
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        