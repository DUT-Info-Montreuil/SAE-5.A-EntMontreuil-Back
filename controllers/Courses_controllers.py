from flask import Blueprint, request, jsonify
from services.courses import CourseService

courses_bp = Blueprint("courses_bp", __name__)
course_service = CourseService() 

@courses_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    return course_service.get_course_by_id(course_id)

@courses_bp.route("/courses", methods=["GET"])
def get_all_courses():
    return course_service.get_all_courses()

@courses_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    return course_service.add_course(data)

@courses_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.get_json()
    data["id"] = course_id
    return course_service.update_course(data)

@courses_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    return course_service.delete_course(course_id)

@courses_bp.route("/courses/copy-day", methods=["POST"])
def copy_day_courses():
    data = request.get_json()
    source_date = data.get("source_date")
    target_date = data.get("target_date")
    return course_service.copy_day_courses(source_date, target_date)

@courses_bp.route("/courses/copy-week", methods=["POST"])
def copy_week_courses():
    data = request.get_json()
    source_week_start_date = data.get("source_week_start_date")
    target_week_start_date = data.get("target_week_start_date")
    return course_service.copy_week_courses(source_week_start_date, target_week_start_date)

@courses_bp.route("/courses/day", methods=["GET"])
def get_courses_by_day():
    target_date = request.args.get("target_date")
    return course_service.get_courses_by_day(target_date)

@courses_bp.route("/courses/week", methods=["GET"])
def get_courses_by_week():
    target_week_start_date = request.args.get("target_week_start_date")
    return course_service.get_courses_by_week(target_week_start_date)