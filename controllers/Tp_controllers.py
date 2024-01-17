from flask import Blueprint, jsonify, request
from services.tp import TPService

tp_bp = Blueprint('tp_bp', __name__)
tp_service = TPService()
# -------------------- Récupérer un TP par ID --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['GET'])
def get_tp_by_id(tp_id):
    """
    Récupérer les détails d'un TP spécifique par ID.
    ---
    tags:
      - TPs
    parameters:
      - name: tp_id
        in: path
        type: integer
        required: true
        description: ID du TP à récupérer.
    responses:
      200:
        description: Détails du TP récupérés avec succès.
      404:
        description: TP non trouvé.
      500:
        description: Erreur serveur interne.
    """
    return tp_service.get_tp_by_id(tp_id)

# -------------------- Récupérer tous les TPs --------------------------------------#
@tp_bp.route('/tp', methods=['GET'])
def get_all_tps():
    """
    Récupérer la liste de tous les TPs.
    ---
    tags:
      - TPs
    responses:
      200:
        description: Liste de tous les TPs récupérée avec succès.
      500:
        description: Erreur serveur interne.
    """
    return tp_service.get_all_tps()

# -------------------- Mettre à jour un TP --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['PUT'])
def update_tp(tp_id):
    """
    Mettre à jour les informations d'un TP spécifique par ID.
    ---
    tags:
      - TPs
    parameters:
      - name: tp_id
        in: path
        type: integer
        required: true
        description: ID du TP à mettre à jour.
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Informations du TP mises à jour avec succès.
      404:
        description: TP non trouvé.
      500:
        description: Erreur serveur interne.
    """
    data = request.get_json()
    return tp_service.update_tp(tp_id, data)

# -------------------- Supprimer un TP --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>', methods=['DELETE'])
def delete_tp(tp_id):
    """
    Supprimer un TP spécifique par ID.
    ---
    tags:
      - TPs
    parameters:
      - name: tp_id
        in: path
        type: integer
        required: true
        description: ID du TP à supprimer.
    responses:
      200:
        description: TP supprimé avec succès.
      404:
        description: TP non trouvé.
      500:
        description: Erreur serveur interne.
    """
    return tp_service.delete_tp(tp_id)

# -------------------- Ajouter un TP --------------------------------------#
@tp_bp.route('/tp', methods=['POST'])
def add_tp():
    """
    Ajouter un nouveau TP.
    ---
    tags:
      - TPs
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: TP ajouté avec succès.
      500:
        description: Erreur serveur interne.
    """
    try:
        data = request.json
        return tp_service.add_tp(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- Ajouter des étudiants à un TP --------------------------------------#
@tp_bp.route('/tp/<int:tp_id>/add-students', methods=['POST'])
def add_students_to_tp(tp_id):
    """
    Ajouter des étudiants à un TP spécifique par ID.
    ---
    tags:
      - TPs
    parameters:
      - name: tp_id
        in: path
        type: integer
        required: true
        description: ID du TP auquel ajouter les étudiants.
      - name: student_ids
        in: body
        required: true
        schema:
          type: object
          properties:
            student_ids:
              type: array
              items:
                type: integer
        description: Liste des IDs des étudiants à ajouter.
    responses:
      200:
        description: Étudiants ajoutés au TP avec succès.
      400:
        description: Mauvaise requête ou erreur de validation.
      500:
        description: Erreur serveur interne.
    """
    student_ids = request.json.get('student_ids')
    if not student_ids:
        return jsonify({"error": "Aucun identifiant d'étudiant fourni"}), 400
    return tp_service.add_students_to_tp(tp_id, student_ids)

# -------------------- Supprimer un étudiant d'un TP --------------------------------------#
@tp_bp.route('/tp/remove_student/<int:student_id>', methods=['GET'])
def remove_student(student_id):
    """
    Supprimer un étudiant d'un TP, TD ou promotion.
    ---
    tags:
      - TPs
    parameters:
      - name: student_id
        in: path
        type: integer
        required: true
        description: ID de l'étudiant à supprimer.
    responses:
      200:
        description: Étudiant supprimé du TP avec succès.
      500:
        description: Erreur serveur interne.
    """
    return tp_service.remove_student_from_tp_td_promotion(student_id)
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