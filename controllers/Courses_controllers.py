from flask import Blueprint, request, jsonify
from services.courses import CourseService
from datetime import datetime, timedelta
from decorators.courses_decorator import CoursesDecorators

courses_bp = Blueprint("courses_bp", __name__)
course_service = CourseService() 

##-----------------GET----------------
#get by id
@courses_bp.route("/courses/id/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    """
    Récupère un cours par son identifiant.

    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: L'identifiant unique du cours.
    responses:
      200:
        description: Cours récupéré avec succès.
        examples:
          application/json:
            {"course": {"id": 1, "name": "Math", "teacher": "John Doe", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}}
      404:
        description: Cours non trouvé.
    """
    reponse, http_status = course_service.get_course_by_id(course_id)
    return reponse, http_status

#get by day
@courses_bp.route("/courses/day/<day>", methods=["GET"])
def get_course_by_day(day):
    """
    Récupère tous les cours pour une journée spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - name: day
        in: path
        type: string
        required: true
        description: La journée pour laquelle récupérer les cours.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "teacher": "John Doe", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour la journée spécifiée.
    """
    reponse, http_status = course_service.get_course_by_day(day)
    return reponse, http_status

#get all
@courses_bp.route("/courses", methods=["GET"])
def get_all_courses():
    """
    Récupère tous les cours.

    ---
    tags:
      - Courses
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "teacher": "John Doe", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
    """
    reponse, http_status = course_service.get_all_courses()
    return reponse, http_status

#get by promotion
@courses_bp.route("/courses/promotion/<int:promotion_id>/<int:semester>", methods=["GET"])
def get_course_by_promotion(promotion_id, semester):
    """
    Récupère tous les cours pour une promotion spécifiée et un semestre donné.

    ---
    tags:
      - Courses
    parameters:
      - name: promotion_id
        in: path
        type: integer
        required: true
        description: L'identifiant de la promotion.
      - name: semester
        in: path
        type: integer
        required: true
        description: Le numéro du semestre.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "teacher": "John Doe", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour la promotion et le semestre spécifiés.
    """
    reponse, http_status = course_service.get_course_by_promotion(promotion_id, semester)
    return reponse, http_status

#get by classroom
@courses_bp.route("/courses/classroom/<string:classroom>", methods=["GET"])
def get_course_by_classroom(classroom):
    """
    Récupère tous les cours pour une salle de classe spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - name: classroom
        in: path
        type: string
        required: true
        description: Le nom de la salle de classe.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "teacher": "John Doe", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour la salle de classe spécifiée.
    """
    reponse, http_status = course_service.get_course_by_classroom(classroom)
    return reponse, http_status

#get by teacher
@courses_bp.route("/courses/teacher/<string:teacher_username>", methods=["GET"])
def get_course_by_teacher(teacher_username):
    """
    Récupère tous les cours pour un enseignant spécifié.

    ---
    tags:
      - Courses
    parameters:
      - name: teacher_username
        in: path
        type: string
        required: true
        description: Le nom d'utilisateur de l'enseignant.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour l'enseignant spécifié.
    """
    reponse, http_status = course_service.get_course_by_teacher(teacher_username)
    return reponse, http_status

#get by week
@courses_bp.route("/courses/week/<start_date>", methods=["GET"])
def get_course_by_week(start_date):
    """
    Récupère tous les cours pour une semaine spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - name: start_date
        in: path
        type: string
        required: true
        description: La date de début de la semaine.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour la semaine spécifiée.
    """
    reponse, http_status = course_service.get_course_by_week(start_date)
    return reponse, http_status

#get by training
@courses_bp.route("/courses/training/<int:trainings_id>", methods=["GET"])
def get_course_by_training(trainings_id):
    """
    Récupère tous les cours pour une formation spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - name: trainings_id
        in: path
        type: integer
        required: true
        description: L'identifiant de la formation.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour la formation spécifiée.
    """
    reponse, http_status = course_service.get_course_by_training(trainings_id)
    return reponse, http_status

#get by td
@courses_bp.route("/courses/td/<int:id_td>", methods=["GET"])
def get_course_by_td(id_td):
    """
    Récupère tous les cours pour un TD spécifié.

    ---
    tags:
      - Courses
    parameters:
      - name: id_td
        in: path
        type: integer
        required: true
        description: L'identifiant du TD.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour le TD spécifié.
    """
    reponse, http_status = course_service.get_course_by_td(id_td)
    return reponse, http_status

#get by tp
@courses_bp.route("/courses/tp/<int:id_tp>", methods=["GET"])
def get_course_by_tp(id_tp):
    """
    Récupère tous les cours pour un TP spécifié.

    ---
    tags:
      - Courses
    parameters:
      - name: id_tp
        in: path
        type: integer
        required: true
        description: L'identifiant du TP.
    responses:
      200:
        description: Cours récupérés avec succès.
        examples:
          application/json:
            [{"id": 1, "name": "Math", "start_time": "09:00", "end_time": "11:00", "classroom": "A101"}]
      404:
        description: Aucun cours trouvé pour le TP spécifié.
    """
    reponse, http_status = course_service.get_course_by_tp(id_tp)
    return reponse, http_status

##-----------------POST----------------
@courses_bp.route("/courses", methods=["POST"])
@CoursesDecorators.validate_json_add_course
def add_course():
    """
    Ajoute un nouveau cours.

    ---
    tags:
      - Courses
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: Le nom du cours.
                example: Math
              teacher:
                type: string
                description: Le nom de l'enseignant.
                example: John Doe
              start_time:
                type: string
                format: time
                description: L'heure de début du cours .
                example: 09:00
              end_time:
                type: string
                format: time
                description: L'heure de fin du cours.
                example: 11:00
              classroom:
                type: string
                description: Le nom de la salle de classe.
                example: A101
    responses:
      201:
        description: Cours ajouté avec succès.
        examples:
          application/json:
            {"message": "Cours ajouté avec succès."}
      400:
        description: Données manquantes ou invalides.
      500:
        description: Erreur interne du serveur.
    """
    data = request.get_json()
    return course_service.add_course(data)

# --------------------- Copier les cours pour une journée spécifique ---------------------
@courses_bp.route("/courses/copy-day", methods=["POST"])
def copy_day_courses():
    """
    Copie tous les cours planifiés pour une journée spécifique vers une nouvelle journée pour une promotion donnée.

    ---
    tags:
      - Courses
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            source_date:
              type: string
              description: La date source des cours à copier.
            target_date:
              type: string
              description: La nouvelle date pour la copie des cours.
            target_promotion_id:
              type: integer
              description: L'identifiant unique de la promotion cible.
    responses:
      200:
        description: Confirmation de la copie des cours pour la journée spécifiée.
      500:
        description: Erreur serveur lors de la copie des cours.
    """
    try:
        data = request.json
        source_date = data.get('source_date')
        target_date = data.get('target_date')
        target_promotion_id = data.get('target_promotion_id')

        response, status_code = course_service.copy_day_courses(source_date, target_date, target_promotion_id)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Copier les cours pour une semaine spécifique ---------------------
@courses_bp.route("/courses/copy-week", methods=["POST"])
def copy_week_courses():
    """
    Copie tous les cours planifiés pour une semaine spécifique vers une nouvelle semaine pour une promotion donnée.

    ---
    tags:
      - Courses
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            source_week_start_date:
              type: string
              description: La date de début de la semaine source des cours à copier.
            target_week_start_date:
              type: string
              description: La nouvelle date de début pour la copie des cours.
            target_promotion_id:
              type: integer
              description: L'identifiant unique de la promotion cible.
    responses:
      200:
        description: Confirmation de la copie des cours pour la semaine spécifiée.
      500:
        description: Erreur serveur lors de la copie des cours.
    """
    try:
        data = request.json
        source_week_start_date = data.get('source_week_start_date')
        target_week_start_date = data.get('target_week_start_date')
        target_promotion_id = data.get('target_promotion_id')

        response, status_code = course_service.copy_week_courses(source_week_start_date, target_week_start_date, target_promotion_id)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Mise à jour d'un cours ---------------------
@courses_bp.route("/courses/<int:course_id>", methods=["PATCH"])
def update_course(course_id):
    """
    Met à jour les informations d'un cours spécifié par son ID.

    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: L'identifiant unique du cours à mettre à jour.
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            # Ajoutez ici les propriétés que vous pouvez mettre à jour
    responses:
      200:
        description: Confirmation de la mise à jour du cours.
      400:
        description: Données JSON manquantes ou incorrectes.
      404:
        description: Le cours spécifié n'existe pas.
      500:
        description: Erreur serveur lors de la mise à jour du cours.
    """
    data = request.get_json()
    data["id"] = course_id
    return course_service.update_course(data, course_id)

# --------------------- Suppression d'un cours ---------------------
@courses_bp.route("/courses/id/<int:course_id>", methods=["DELETE"])
def delete_course_with_id(course_id):
    """
    Supprime un cours spécifié par son ID.

    ---
    tags:
      - Courses
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: L'identifiant unique du cours à supprimer.
    responses:
      200:
        description: Confirmation de la suppression du cours.
      404:
        description: Le cours spécifié n'existe pas.
      500:
        description: Erreur serveur lors de la suppression du cours.
    """
    return course_service.delete_course_with_id(course_id)
# --------------------- Suppression d'un cours par jour ---------------------
@courses_bp.route("/courses/day/<day>", methods=["DELETE"])
def delete_course_with_day(day):
    """
    Supprime tous les cours planifiés pour un jour spécifié.

    ---
    tags:
      - Courses
    parameters:
      - name: day
        in: path
        type: string
        required: true
        description: La date pour laquelle supprimer tous les cours planifiés.
    responses:
      200:
        description: Confirmation de la suppression des cours pour le jour spécifié.
      500:
        description: Erreur serveur lors de la suppression des cours.
    """
    group = request.get_json()
    return course_service.delete_course_with_day(day, group)

# --------------------- Suppression de cours sur plusieurs jours ---------------------
@courses_bp.route("/courses/days", methods=["DELETE"])
def delete_course_with_many_day():
    """
    Supprime tous les cours planifiés pour une plage de jours spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            startDay:
              type: string
              description: La date de début de la plage.
            endDay:
              type: string
              description: La date de fin de la plage.
            # Ajoutez ici d'autres propriétés nécessaires
    responses:
      200:
        description: Confirmation de la suppression des cours pour la plage de jours spécifiée.
      500:
        description: Erreur serveur lors de la suppression des cours.
    """
    data = request.get_json()
    return course_service.delete_course_with_many_day(data["startDay"], data["endDay"], data)

# --------------------- Suppression d'un cours par ressource ---------------------
@courses_bp.route("/courses/resource/<int:id_resource>", methods=["DELETE"])
def delete_course_with_resource(id_resource):
    """
    Supprime tous les cours associés à une ressource spécifiée.

    ---
    tags:
      - Courses
    parameters:
      - name: id_resource
        in: path
        type: integer
        required: true
        description: L'identifiant unique de la ressource pour laquelle supprimer les cours.
    responses:
      200:
        description: Confirmation de la suppression des cours associés à la ressource.
      500:
        description: Erreur serveur lors de la suppression des cours.
    """
    return course_service.delete_course_with_resource(id_resource)

# --------------------- Suppression d'un cours par enseignant ---------------------
@courses_bp.route("/courses/teacher/<int:id_teacher>", methods=["DELETE"])
def delete_course_with_teacher(id_teacher):
    """
    Supprime tous les cours associés à un enseignant spécifié.

    ---
    tags:
      - Courses
    parameters:
      - name: id_teacher
        in: path
        type: integer
        required: true
        description: L'identifiant unique de l'enseignant pour lequel supprimer les cours.
    responses:
      200:
        description: Confirmation de la suppression des cours associés à l'enseignant.
      500:
        description: Erreur serveur lors de la suppression des cours.
    """
    return course_service.delete_course_with_teacher(id_teacher)



"""ENT Montreuil is a Desktop Working Environnement for the students of the IUT of Montreuil
    Copyright (C) 2024  Steven CHING, Emilio CYRIAQUE-SOURISSEAU ALVARO-SEMEDO, Ismail GADA, Yanis HAMANI, Priyank SOLANKI

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""