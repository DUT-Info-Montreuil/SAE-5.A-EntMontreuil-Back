from flask import request, jsonify, Blueprint
from services.classroom import ClassroomService
from entities.DTO.materials import Material
import connect_pg
Classroom_bp = Blueprint('classrooms', __name__)


Classroom_service = ClassroomService()

@Classroom_bp.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    """
Récupérer toutes les salles de classe.

---
tags:
  - Salles de classe
parameters:
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "dto"
    enum: ["model", "dto"]
responses:
  200:
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        },
        {
            "id": 2,
            "name": "Salle2",
            "capacity": 40,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 8
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 12
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_classroom=None)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@Classroom_bp.route('/classrooms/<int:id_Classroom>', methods=['GET'])
def get_classroom(id_Classroom):
    """
Récupérer une salle de classe via son id
---
tags:
  - Salles de classe
parameters:
  - name: output_format
    in: query
    description: Le format de sortie des données (par défaut "model").
    required: false
    type: string
    default: "dto"
    enum: ["model", "dto"]
responses:
  200:
    description: Liste des salles de classe récupérées depuis la base de données.
    examples:
      application/json: [
        {
            "id": 1,
            "name": "Salle1",
            "capacity": 30,
            "materials": [
              {
                "id": 1,
                "equipment": "Ordinateur portable",
                "quantity": 10
              },
              {
                "id": 2,
                "equipment": "Tableau blanc",
                "quantity": 5
              }
            ]
        }
      ]
  500:
    description: Erreur serveur en cas de problème lors de la récupération des salles de classe.
"""

    try:
        output_format = request.args.get('output_format', 'model')  # Par défaut, le format de sortie est "dto"
        classrooms = Classroom_service.get_all_classrooms(output_format,id_Classroom,)

        return classrooms
    except Exception as e:
        return jsonify({"message": str(e)}), 500