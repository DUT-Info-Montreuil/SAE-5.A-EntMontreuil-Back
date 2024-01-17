from flask import Blueprint, jsonify, request
from services.td import TDService

td_bp = Blueprint('td_bp', __name__)
td_service = TDService()
# -------------------- Récupérer un TD par ID --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['GET'])
def get_td_by_id(td_id):
    """
    Récupérer les détails d'un TD spécifique par ID.
    ---
    tags:
      - TDs
    parameters:
      - name: td_id
        in: path
        type: integer
        required: true
        description: ID du TD à récupérer.
    responses:
      200:
        description: Détails du TD récupérés avec succès.
      404:
        description: TD non trouvé.
      500:
        description: Erreur serveur interne.
    """
    return td_service.get_td_by_id(td_id)


# -------------------- Récupérer les TD d'un Training --------------------------------------#
@td_bp.route('/td/training/<int:id_training>', methods=['GET'])
def get_tds_by_training(id_training):
    """
    Récupérer la liste des TDs pour une formation spécifique.
    ---
    tags:
      - TDs
    parameters:
      - name: id_training
        in: path
        type: integer
        required: true
        description: ID de la formation pour laquelle récupérer les TDs.
    responses:
      200:
        description: Liste des TDs récupérés avec succès.
      404:
        description: Formation non trouvée.
      500:
        description: Erreur serveur interne.
    """
    return td_service.get_tds_by_training_id(id_training)

# -------------------- Récupérer tous les TDs --------------------------------------#
@td_bp.route('/td', methods=['GET'])
def get_all_tds():
    """
    Récupérer la liste de tous les TDs.
    ---
    tags:
      - TDs
    responses:
      200:
        description: Liste de tous les TDs récupérée avec succès.
      500:
        description: Erreur serveur interne.
    """
    return td_service.get_all_tds()

# -------------------- Mettre à jour un TD --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['PUT'])
def update_td(td_id):
    """
    Mettre à jour les informations d'un TD spécifique par ID.
    ---
    tags:
      - TDs
    parameters:
      - name: td_id
        in: path
        type: integer
        required: true
        description: ID du TD à mettre à jour.
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            # ... (add properties based on your JSON structure)
    responses:
      200:
        description: Informations du TD mises à jour avec succès.
      404:
        description: TD non trouvé.
      500:
        description: Erreur serveur interne.
    """
    data = request.get_json()
    return td_service.update_td(td_id, data)

# -------------------- Supprimer un TD --------------------------------------#
@td_bp.route('/td/<int:td_id>', methods=['DELETE'])
def delete_td(td_id):
    """
    Supprimer un TD spécifique par ID.
    ---
    tags:
      - TDs
    parameters:
      - name: td_id
        in: path
        type: integer
        required: true
        description: ID du TD à supprimer.
    responses:
      200:
        description: TD supprimé avec succès.
      404:
        description: TD non trouvé.
      500:
        description: Erreur serveur interne.
    """
    return td_service.delete_td(td_id)

# -------------------- Créer un TD --------------------------------------#
@td_bp.route('/td', methods=['POST'])
def create_td():
    """
    Créer un nouveau TD.
    ---
    tags:
      - TDs
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
        description: TD créé avec succès.
      500:
        description: Erreur serveur interne.
    """
    try:
        data = request.json
        return td_service.add_td(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- get tp by TD --------------------------------------#
@td_bp.route('/td/tp/<int:id_td>', methods=['GET'])
def get_tp_by_td(id_td):
    """
    Récupérer les travaux pratiques associés à un TD spécifique par ID.
    ---
    tags:
      - TDs
    parameters:
      - name: id_td
        in: path
        type: integer
        required: true
        description: ID du TD pour lequel récupérer les TP.
    responses:
      200:
        description: Liste des TP associés au TD récupérée avec succès.
      404:
        description: TD non trouvé.
      500:
        description: Erreur serveur interne.
    """
    try:
        return td_service.get_tp_by_td(id_td)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
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