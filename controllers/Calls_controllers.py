from flask import Blueprint, request, jsonify
from services.calls import CallsService
import connect_pg

calls_bp = Blueprint('calls_bp', __name__)
calls_service = CallsService()

@calls_bp.route('/calls/students/info/<int:course_id>', methods=['GET'])
def get_students_info_for_course(course_id):
    return calls_service.get_students_info_for_course(course_id)

@calls_bp.route('/calls/students/absences/<int:course_id>', methods=['GET'])
def get_students_with_absences_for_course(course_id):
    return calls_service.get_students_with_absences_for_course(course_id)