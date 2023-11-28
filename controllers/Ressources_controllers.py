from flask import Blueprint, request, jsonify
from services.resources import ResourceService

resources_bp = Blueprint("resources_bp", __name__)
resource_service = ResourceService()

@resources_bp.route("/resources", methods=["POST"])
def add_resource():
    data = request.get_json()
    return resource_service.add_resource(data)

@resources_bp.route("/resources/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    return resource_service.delete_resource(resource_id)

@resources_bp.route("/resources/<int:resource_id>", methods=["PUT"])
def update_resource(resource_id):
    data = request.get_json()
    data["id"] = resource_id
    return resource_service.update_resource(data)

@resources_bp.route("/resources/<int:resource_id>", methods=["GET"])
def get_resource_by_id(resource_id):
    return resource_service.get_resource_by_id(resource_id)

@resources_bp.route("/resources", methods=["GET"])
def get_all_resources():
    return resource_service.get_all_resources()
