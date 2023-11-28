from flask import Blueprint, request, jsonify
from services.promotions import PromotionService

promotion_bp = Blueprint("promotion", __name__)
promotion_service = PromotionService()

@promotion_bp.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotion_info(promotion_id):
    output_format = request.args.get("format", default="DTO")
    return promotion_service.get_promotion_info(promotion_id, output_format)

@promotion_bp.route("/promotions", methods=["GET"])
def get_all_promotions():
    output_format = request.args.get("format", default="DTO")
    return promotion_service.get_all_promotions(output_format)

@promotion_bp.route("/promotions", methods=["POST"])
def add_promotion():
    data = request.json
    return promotion_service.add_promotion(data)

@promotion_bp.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotion(promotion_id):
    data = request.json
    data["id"] = promotion_id
    return promotion_service.update_promotion(data)

@promotion_bp.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotion(promotion_id):
    return promotion_service.delete_promotion(promotion_id)

@promotion_bp.route("/promotions/<int:promotion_id>/td", methods=["POST"])
def create_td_in_promotion(promotion_id):
    td_name = request.json.get("td_name")
    return promotion_service.create_td_in_promotion(promotion_id, td_name)

@promotion_bp.route("/promotions/td/<int:td_id>/tp", methods=["POST"])
def create_tp_in_td(td_id):
    tp_name = request.json.get("tp_name")
    return promotion_service.create_tp_in_td(td_id, tp_name)

@promotion_bp.route("/promotions/students/csv", methods=["POST"])
def add_students_from_csv():
    csv_path = request.json.get("csv_path")
    return promotion_service.add_students_from_csv(csv_path)

@promotion_bp.route("/promotions/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_promotion(student_ine):
    return promotion_service.remove_student_from_promotion(student_ine)

@promotion_bp.route("/promotions/td/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_td(student_ine):
    td_id = request.json.get("td_id")
    return promotion_service.remove_student_from_td(student_ine, td_id)

@promotion_bp.route("/promotions/tp/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_tp(student_ine):
    tp_id = request.json.get("tp_id")
    return promotion_service.remove_student_from_tp(student_ine, tp_id)