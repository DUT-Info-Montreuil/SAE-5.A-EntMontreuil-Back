from flask import Blueprint, request, jsonify
from services.courses import CourseService
from datetime import datetime, timedelta

courses_bp = Blueprint("courses_bp", __name__)
course_service = CourseService() 

##-----------------GET----------------
#get by id
@courses_bp.route("/courses/id/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    reponse, http_status =course_service.get_course_by_id(course_id)
    return reponse, http_status

#get by day
@courses_bp.route("/courses/day/<day>", methods=["GET"])
def get_course_by_day(day):
    reponse, http_status = course_service.get_course_by_day(day)
    return reponse, http_status

#get all
@courses_bp.route("/courses", methods=["GET"])
def get_all_courses():
    reponse, http_status =course_service.get_all_courses()
    return reponse, http_status

#get by promotion
@courses_bp.route("/courses/promotion/<int:promotion_year>", methods=["GET"])
def get_course_by_promotion(promotion_year):
    reponse, http_status = course_service.get_course_by_promotion(promotion_year)
    return reponse, http_status

#get by classroom
@courses_bp.route("/courses/classroom/<string:classroom>", methods=["GET"])
def get_course_by_classroom(classroom):
    reponse, http_status = course_service.get_course_by_classroom(classroom)
    return reponse, http_status

#get by teacher
@courses_bp.route("/courses/teacher/<string:teacher_username>", methods=["GET"])
def get_course_by_teacher(teacher_username):
    reponse, http_status =course_service.get_course_by_teacher(teacher_username)
    return reponse, http_status

#get by week
@courses_bp.route("/courses/week/<start_date>", methods=["GET"])
def get_course_by_week(start_date):
    reponse, http_status = course_service.get_course_by_week(start_date)
    return reponse, http_status

#get by training
@courses_bp.route("/courses/trainings/<int:trainings_id>", methods=["GET"])
def get_course_by_training(trainings_id):
    reponse, http_status = course_service.get_course_by_training(trainings_id)
    return reponse, http_status

#get by td
@courses_bp.route("/courses/td/<int:id_td>", methods=["GET"])
def get_course_by_td(id_td):
    reponse, http_status = course_service.get_course_by_td(id_td)
    return reponse, http_status

#get by tp
@courses_bp.route("/courses/tp/<int:id_tp>", methods=["GET"])
def get_course_by_tp(id_tp):
    reponse, http_status = course_service.get_course_by_tp(id_tp)
    return reponse, http_status

##-----------------POST----------------
@courses_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    return course_service.add_course(data)

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

##-----------------PATCH----------------
@courses_bp.route("/courses/<int:course_id>", methods=["PATCH"])
def update_course(course_id):
    data = request.get_json()
    data["id"] = course_id
    return course_service.update_course(data)

##-----------------DELETE----------------
@courses_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    return course_service.delete_course(course_id)



