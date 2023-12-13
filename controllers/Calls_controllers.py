# controllers/calls_controllers.py
from flask import Blueprint, request, jsonify
from services.calls import CallsService
import connect_pg

calls_bp = Blueprint('calls_bp', __name__)
calls_service = CallsService()

@calls_bp.route('/calls/<int:call_id>', methods=['GET'])
def get_call_by_id(call_id):
    return calls_service.get_call_by_id(call_id)

@calls_bp.route('/calls/<int:call_id>', methods=['PUT'])
def update_call(call_id):
    data = request.get_json()
    return calls_service.update_call(call_id, data)

@calls_bp.route('/calls', methods=['POST'])
def add_call():
    data = request.get_json()
    return calls_service.add_call(data)

@calls_bp.route('/calls/<int:call_id>', methods=['DELETE'])
def delete_call(call_id):
    return calls_service.delete_call(call_id)

@calls_bp.route('/calls/students/<call_type>/<int:call_id>', methods=['GET'])
def get_students_for_call(call_type, call_id):
    return calls_service.get_students_for_call(call_type, call_id)

@calls_bp.route('/calls/status/<int:id_course>', methods=['PUT'])
def update_call_status(id_course):
    data = request.get_json()
    return calls_service.update_call_status(id_course, data)
