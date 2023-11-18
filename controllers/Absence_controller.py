from flask import request, jsonify, Blueprint
from services.absences import AbsencesService
import connect_pg

# Création d'un Blueprint pour les routes liées aux absences
absences_bp = Blueprint('absences', __name__)

# Instanciation du service d'absences
absences_service = AbsencesService()


#--------------------Récuperer toutes les absences--------------------------------------#

@absences_bp.route('/absences', methods=['GET'])
def get_all_absences():
    """
    Récupère toutes les absences depuis la base de données.

    ---
    tags:
      - Absences
    parameters:
      - name: justified
        in: query
        type: integer
        required: false
        description: 1 pour les absences justifiées, 0 pour les absences non justifiées.
      - name: output_format
        in: query
        type: string
        required: false
        default: 'DTO'
        description: Format de sortie des données ('DTO' ou 'model').
    responses:
      200:
        description: Liste des absences récupérées depuis la base de données.
        examples:
          application/json: [
            {
              "id": 1,
              "student_id": 123,
              "date": "2023-01-01",
              "justified": true
              # ... autres champs
            },
            # ... autres absences
          ]
      500:
        description: Erreur serveur en cas de problème lors de la récupération des absences.
    """
    justified = request.args.get('justified', default=None, type=int)
    output_format = request.args.get('output_format', default='DTO', type=str)
    
    try:
        absences_list = absences_service.get_all_absences(justified=justified, output_format=output_format)
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#--------------------Récuperer toutes les absences d'un étudiant via son id--------------------------------------#

@absences_bp.route('/absences/student/<int:id_student>', methods=['GET'])
def get_student_absences(id_student):
    """
    Récupère toutes les absences d'un étudiant spécifié par son ID.

    ---
    tags:
      - Absences
    parameters:
      - name: id_student
        in: path
        type: integer
        required: true
        description: L'identifiant unique de l'étudiant pour lequel récupérer les absences.
      - name: justified
        in: query
        type: integer
        required: false
        description: 1 pour les absences justifiées, 0 pour les absences non justifiées. Laisser vide pour toutes les absences.
      - name: output_format
        in: query
        type: string
        required: false
        default: 'DTO'
        description: Format de sortie des données ('DTO' ou 'model').
    responses:
      200:
        description: Liste des absences de l'étudiant récupérées depuis la base de données.
        examples:
          application/json: [
            {
              "id": 1,
              "student_id": 123,
              "date": "2023-01-01",
              "justified": true,
              # ... autres champs
            },
            # ... autres absences
          ]
      404:
        description: L'étudiant spécifié n'existe pas.
      500:
        description: Erreur serveur en cas de problème lors de la récupération des absences.
    """
    justified = request.args.get('justified', default=None, type=int)
    output_format = request.args.get('output_format', default='DTO', type=str)
    
    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    try:
        absences_list = absences_service.get_student_absences(id_student, justified=justified, output_format=output_format)
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500



#--------------------Modifier une  absence--------------------------------------#

@absences_bp.route('/absences/student/<int:id_student>/course/<int:id_course>', methods=['PUT'])
def update_student_course_absence(id_student, id_course):
    """
Modifie une absence d'un étudiant pour un cours donné.

---
tags:
  - Absences
parameters:
  - name: id_student
    in: path
    type: integer
    required: true
    description: ID de l'étudiant.
  - name: id_course
    in: path
    type: integer
    required: true
    description: ID du cours.
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            reason:
              type: string
              description: Raison de l'absence.
            justify:
              type: boolean
              description: Justification de l'absence (true pour justifié, false pour non justifié).
responses:
  200:
    description: Confirmation de la mise à jour de l'absence.
  400:
    description: Données JSON manquantes ou incorrectes.
  404:
    description: L'absence ou l'étudiant spécifié n'existe pas.
  500:
    description: Erreur serveur lors de la mise à jour de l'absence.
"""

    json_data = request.json
    if not json_data or 'datas' not in json_data:
        return jsonify({"message": "Données manquantes"}), 400

    absence_data = json_data['datas']
    if 'reason' not in absence_data or 'justify' not in absence_data:
        return jsonify({"message": "Les raisons et les justifications sont requises"}), 400

    if not connect_pg.does_entry_exist("Courses", id_course):
        return jsonify({"message": "Absence non trouvée ou aucune modification effectuée"}), 404

    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    data = {
        "id_student": id_student,
        "id_course": id_course,
        "reason": absence_data["reason"],
        "justify": absence_data["justify"]
    }

    try:
        message = absences_service.update_student_course_absence(data)
        return jsonify(message)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#--------------------ajouter  une  absence--------------------------------------#
@absences_bp.route('/absences/student/<int:id_student>/course/<int:id_course>/add', methods=['POST'])
def add_student_course_absence(id_student, id_course):
    """
Ajoute une absence d'un étudiant pour un cours donné.

---
tags:
  - Absences
parameters:
  - name: id_student
    in: path
    type: integer
    required: true
    description: ID de l'étudiant.
  - name: id_course
    in: path
    type: integer
    required: true
    description: ID du cours.
  - in: body
    name: datas
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            reason:
              type: string
              description: Raison de l'absence.
            justify:
              type: boolean
              description: Justification de l'absence (true pour justifié, false pour non justifié).
responses:
  201:
    description: Confirmation de l'ajout de l'absence.
  400:
    description: Données JSON manquantes ou incorrectes.
  404:
    description: Le cours ou l'étudiant spécifié n'existe pas.
  500:
    description: Erreur serveur lors de l'ajout de l'absence.
"""

    try:
        json_data = request.json

        # Vérifie la présence des données JSON et de la clé 'datas'
        if not json_data or 'datas' not in json_data:
            return jsonify({"message": "Données manquantes"}), 400

        absence_data = json_data['datas']

        # Valide la présence des champs obligatoires dans les données JSON
        required_fields = ['reason', 'justify']
        for field in required_fields:
            if field not in absence_data:
                return jsonify({"message": f"Le champ '{field}' est requis"}), 400

        if not connect_pg.does_entry_exist("Courses", id_course):
            return jsonify({"message": "Le cours spécifié n'existe pas."}), 404

        if not connect_pg.does_entry_exist("Students", id_student):
            return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

        data = {
            "id_student": id_student,
            "id_course": id_course,
            "reason": absence_data["reason"],
            "justify": absence_data["justify"]
        }

        message = absences_service.add_student_course_absence(data)
        return jsonify({"message": message}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

#-------------------- Supprimer une  absence--------------------------------------#
@absences_bp.route('/absences/student/<int:id_student>/course/<int:id_course>/delete', methods=['DELETE'])
def delete_student_course_absence(id_student, id_course):
    """
    Supprime une absence spécifique d'un étudiant pour un cours donné.

    ---
    tags:
      - Absences
    parameters:
      - name: id_student
        in: path
        type: integer
        required: true
        description: L'identifiant unique de l'étudiant concerné.
      - name: id_course
        in: path
        type: integer
        required: true
        description: L'identifiant unique du cours concerné.
    responses:
      200:
        description: Confirmation de la suppression de l'absence.
        examples:
          application/json: 
            {"message": "Absence supprimée avec succès."}
      404:
        description: L'étudiant ou le cours spécifié n'existe pas, ou l'absence n'a pas été trouvée.
      500:
        description: Erreur serveur en cas de problème lors de la suppression de l'absence.
    """
    # Instanciation du service d'absences
    absences_service = AbsencesService()

    # Vérification de l'existence de l'étudiant et du cours
    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    if not connect_pg.does_entry_exist("Courses", id_course):
        return jsonify({"message": "Le cours spécifié n'existe pas."}), 404

    # Tentative de suppression de l'absence
    try:
        message = absences_service.delete_student_course_absence({"id_student": id_student, "id_course": id_course})
        return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
