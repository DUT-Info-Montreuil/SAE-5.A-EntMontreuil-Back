from flask import Blueprint, request, jsonify
from services.promotions import PromotionService

promotions_bp = Blueprint("promotion", __name__)
promotion_service = PromotionService()

@promotions_bp.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotion_info(promotion_id):
    """
    Obtenez des informations sur une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: promotion_id
        in: path
        required: true
        type: integer
        description: ID de la promotion
    responses:
      200:
        description: Succès
      404:
        description: Promotion non trouvée
      500:
        description: Erreur serveur
    """
    output_format = request.args.get("format", default="DTO")
    return promotion_service.get_promotion_info(promotion_id, output_format)

@promotions_bp.route("/promotions", methods=["GET"])
def get_all_promotions():
    """
    Obtenez toutes les promotions.

    ---
    tags:
      - Promotions
    parameters:
      - name: format
        in: query
        type: string
        description: Format de sortie (DTO ou model)
    responses:
      200:
        description: Succès
      500:
        description: Erreur serveur
    """
    output_format = request.args.get("format", default="model")
    return promotion_service.get_all_promotions(output_format)

@promotions_bp.route("/promotions", methods=["POST"])
def add_promotion():
    """
    Ajoutez une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: body
        in: body
        required: true
        description: Données de la promotion à ajouter
        schema:
          type: object
          properties:
            year:
              type: integer
              description: Année de la promotion
            level:
              type: string
              description: Niveau de la promotion
            degree_id:
              type: integer
              description: ID du diplôme associé
    responses:
      200:
        description: Promotion ajoutée avec succès
      500:
        description: Erreur serveur
    """
    data = request.json
    return promotion_service.add_promotion(data)

@promotions_bp.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotion(promotion_id):
    """
    Mettez à jour une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: promotion_id
        in: path
        required: true
        type: integer
        description: ID de la promotion à mettre à jour
      - name: body
        in: body
        required: true
        description: Données de la promotion à mettre à jour
        schema:
          type: object
          properties:
            year:
              type: integer
              description: Nouvelle année de la promotion
            level:
              type: string
              description: Nouveau niveau de la promotion
            degree_id:
              type: integer
              description: Nouvel ID du diplôme associé
    responses:
      200:
        description: Promotion mise à jour avec succès
      404:
        description: Promotion non trouvée ou aucune modification effectuée
      500:
        description: Erreur serveur
    """
    data = request.json
    data["id"] = promotion_id
    return promotion_service.update_promotion(data)

@promotions_bp.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotion(promotion_id):
    """
    Supprimez une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: promotion_id
        in: path
        required: true
        type: integer
        description: ID de la promotion à supprimer
    responses:
      200:
        description: Promotion supprimée avec succès
      404:
        description: Promotion non trouvée ou déjà supprimée
      500:
        description: Erreur serveur
    """
    return promotion_service.delete_promotion(promotion_id)

@promotions_bp.route("/promotions/<int:promotion_id>/td", methods=["POST"])
def create_td_in_promotion(promotion_id):
    """
    Créez un TD dans une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: promotion_id
        in: path
        required: true
        type: integer
        description: ID de la promotion dans laquelle créer le TD
      - name: body
        in: body
        required: true
        description: Données du TD à créer
        schema:
          type: object
          properties:
            td_name:
              type: string
              description: Nom du TD
    responses:
      201:
        description: TD créé avec succès dans la promotion
      500:
        description: Erreur serveur
    """
    td_name = request.json.get("td_name")
    return promotion_service.create_td_in_promotion(promotion_id, td_name)

@promotions_bp.route("/promotions/td/<int:td_id>/tp", methods=["POST"])
def create_tp_in_td(td_id):
    """
    Créez un TP dans un TD.

    ---
    tags:
      - Promotions
    parameters:
      - name: td_id
        in: path
        required: true
        type: integer
        description: ID du TD dans lequel créer le TP
      - name: body
        in: body
        required: true
        description: Données du TP à créer
        schema:
          type: object
          properties:
            tp_name:
              type: string
              description: Nom du TP
    responses:
      201:
        description: TP créé avec succès dans le TD
      500:
        description: Erreur serveur
    """
    tp_name = request.json.get("tp_name")
    return promotion_service.create_tp_in_td(td_id, tp_name)

@promotions_bp.route("/promotions/students/csv", methods=["POST"])
def add_students_from_csv():
    """
    Ajoutez des étudiants à une promotion, TD et TP à partir d'un fichier CSV.

    ---
    tags:
      - Promotions
    parameters:
      - name: body
        in: body
        required: true
        description: Chemin du fichier CSV contenant les données des étudiants
        schema:
          type: object
          properties:
            csv_path:
              type: string
              description: Chemin du fichier CSV
    responses:
      200:
        description: Étudiants ajoutés avec succès à la promotion, TD et TP
      404:
        description: Fichier CSV non trouvé ou données incorrectes
      500:
        description: Erreur serveur
    """
    csv_path = request.json.get("csv_path")
    return promotion_service.add_students_tp_td_promotion_from_csv(csv_path)

@promotions_bp.route("/promotions/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_promotion(student_ine):
    """
    Retirez un étudiant d'une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: student_ine
        in: path
        required: true
        type: string
        description: INE de l'étudiant à retirer
    responses:
      200:
        description: Étudiant retiré avec succès de la promotion, TD et TP
      404:
        description: Étudiant non trouvé
      500:
        description: Erreur serveur
    """
    return promotion_service.remove_student_from_promotion(student_ine)

@promotions_bp.route("/promotions/td/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_td(student_ine):
    """
    Retirez un étudiant d'un TD.

    ---
    tags:
      - Promotions
    parameters:
      - name: student_ine
        in: path
        required: true
        type: string
        description: INE de l'étudiant à retirer du TD
      - name: body
        in: body
        required: true
        description: Données supplémentaires pour le retrait de l'étudiant du TD
        schema:
          type: object
          properties:
            td_id:
              type: integer
              description: ID du TD
    responses:
      200:
        description: Étudiant retiré avec succès du TD
      400:
        description: Étudiant non présent dans le TD spécifié
      404:
        description: Étudiant non trouvé ou TD non trouvé
      500:
        description: Erreur serveur
    """
    td_id = request.json.get("td_id")
    return promotion_service.remove_student_from_td(student_ine, td_id)

@promotions_bp.route("/promotions/tp/students/<string:student_ine>", methods=["DELETE"])
def remove_student_from_tp(student_ine):
    """
    Retirez un étudiant d'un TP.

    ---
    tags:
      - Promotions
    parameters:
      - name: student_ine
        in: path
        required: true
        type: string
        description: INE de l'étudiant à retirer du TP
      - name: body
        in: body
        required: true
        description: Données supplémentaires pour le retrait de l'étudiant du TP
        schema:
          type: object
          properties:
            tp_id:
              type: integer
              description: ID du TP
    responses:
      200:
        description: Étudiant retiré avec succès du TP
      400:
        description: Étudiant non présent dans le TP spécifié
      404:
        description: Étudiant non trouvé ou TP non trouvé
      500:
        description: Erreur serveur
    """
    tp_id = request.json.get("tp_id")
    return promotion_service.remove_student_from_tp(student_ine, tp_id)

@promotions_bp.route("/promotions/trainings/<int:id_promo>", methods=["GET"])
def get_training_of_promo(id_promo):
    """
    Obtenez les parcours d'une promotion.

    ---
    tags:
      - Promotions
    parameters:
      - name: id_promo
        in: path
        required: true
        type: integer
        description: ID de la promotion
    responses:
      200:
        description: Succès
      500:
        description: Erreur serveur
    """
    return promotion_service.get_training_of_promo(id_promo)
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