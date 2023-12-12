from flask import request, jsonify, Blueprint
from services.degrees import DeegreeService
from entities.DTO.degrees import Degrees
import connect_pg
from decorators.degrees_decorator import DegreesDecorators

degrees_bp = Blueprint('degrees', __name__)

degree_service = DeegreeService()

@degrees_bp.route('/degrees', methods=['GET'])
def get_all_degrees():
    """
    Récupérer toutes les informations sur les Formation.

    ---
    tags:
      - Degree
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
        description: Liste des Formation récupérés depuis la base de données.
      500:
        description: Erreur serveur en cas de problème lors de la récupération des Formation.
    """
    try:
        output_format = request.args.get('output_format', 'model')
        degrees = degree_service.get_all_degrees(output_format)
        return degrees
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@degrees_bp.route('/degrees', methods=['POST'])
@DegreesDecorators.validate_json_degree
def create_degree():
    """
Créer une nouvelle Formation.

---
tags:
  - Degree
parameters:
  - in: body
    name: degree_data
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            name:
              type: string
              description: Le nom de la formation.
responses:
  201:
    description: Nouvelle formation créée avec succès.
  400:
    description: Données invalides fournies.
  500:
    description: Erreur serveur lors de la création de la formation.
"""

    try:
        data = request.json.get('datas', {})
        name = data.get('name')
        degree = Degrees(id=0, name=name)
        result = degree_service.create_degree(degree)

        if "error" in result:
            return jsonify(result), 500

        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@degrees_bp.route('/degrees/<int:degree_id>', methods=['DELETE'])
def delete_degree(degree_id):
    """
    Supprime une formation par son ID.

    Cette route permet de supprimer une formation en fournissant son ID.

    ---
    tags:
      - Degree
    parameters:
      - name: degree_id
        in: path
        description: ID de la formation à supprimer
        required: true
        type: integer
    responses:
      200:
        description: Formation supprimée avec succès
      404:
        description: Formation non trouvée
      500:
        description: Erreur interne du serveur
    """
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.delete_degree(degree_id)
    return jsonify(result)

# Route pour récupérer une formation par son ID
@degrees_bp.route('/degrees/<int:degree_id>', methods=['GET'])
def get_degree_by_id(degree_id):
    """
Récupère une formation par son ID.

Cette route permet de récupérer une formation en fournissant son ID.

---
tags:
  - Degree
parameters:
  - name: degree_id
    in: path
    description: ID de la formation à récupérer
    required: true
    type: integer
  - name: output_format
    in: query
    description: Format de sortie des données (par défaut "model")
    required: false
    type: string
    default: "model"
    enum: ["model", "dto"]
responses:
  200:
    description: Formation récupérée avec succès
  404:
    description: Formation non trouvée
  500:
    description: Erreur interne du serveur
"""

    output_format = request.args.get('output_format', 'model')
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.get_degree_by_id(degree_id, output_format)
    return result

# Route pour mettre à jour une formation
@degrees_bp.route('/degrees/<int:degree_id>', methods=['PUT'])
@DegreesDecorators.validate_json_degree
def update_degree(degree_id):
    """
Met à jour une formation par son ID.

Cette route permet de mettre à jour le nom d'une formation en fournissant son ID.

---
tags:
  - Degree
parameters:
  - name: degree_id
    in: path
    description: ID de la formation à mettre à jour
    required: true
    type: integer
  - in: body
    name: data
    required: true
    schema:
      type: object
      properties:
        datas:
          type: object
          properties:
            name:
              type: string
              description: Nouveau nom de la formation
              example: "Nouveau nom de formation"
responses:
  200:
    description: Formation mise à jour avec succès
  400:
    description: Requête invalide ou données manquantes
  404:
    description: Formation non trouvée
  500:
    description: Erreur interne du serveur
"""

    data = request.json.get('datas', {})
    new_name = data.get('name')
    if not connect_pg.does_entry_exist("Degrees", degree_id):
        return jsonify({"message": "La formation spécifiée n'existe pas."}), 404

    result = degree_service.update_degree(degree_id, new_name)
    return jsonify(result)
  
@degrees_bp.route('/degree/<int:degree_id>', methods=['GET'])
def get_degree_info(degree_id):
    try:
        # Connexion à la base de données
        conn = connect_pg.connect()
        cursor = conn.cursor()

        # Récupérer les informations du degree
        cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (degree_id,))
        degree_row = cursor.fetchone()
        if degree_row is None:
            return jsonify({"error": "Degree not found"}), 404

        degree_info = {"id": degree_row[0], "name": degree_row[1], "promotions": [], "students": []}

        # Récupérer les promotions associées au degree
        cursor.execute("SELECT * FROM ent.Promotions WHERE id_degree = %s", (degree_id,))
        promotions = cursor.fetchall()
        promotions_dict = {}
        for promotion in promotions:
            promo_info = {
                "id": promotion[0],
                "year": promotion[1],
                "level": promotion[2],
                # Ajoutez d'autres champs de la table Promotions si nécessaire
            }
            degree_info["promotions"].append(promo_info)
            promotions_dict[promotion[0]] = promo_info  # Stocker dans le dictionnaire

        # Récupérer les étudiants
        cursor.execute("""
            SELECT u.*, s.apprentice, s.id_td, s.id_tp, s.id_promotion, s.id
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            JOIN ent.Promotions p ON s.id_promotion = p.id
            WHERE p.id_degree = %s
        """, (degree_id,))
        students = cursor.fetchall()
        for student in students:
            student_info = {
                "id": student[0],
                "id_student": student[13],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[9],  # Ajustez l'indice selon l'ordre des colonnes
                "id_promotion": student[12],  # Ajustez l'indice selon l'ordre des colonnes
                "promotion": promotions_dict.get(student[12]),  # Ajouter les détails de la promotion
                "tp": [],
                "td": []
            }

            # Récupérer les informations de TP et TD associées à chaque étudiant
            if student[11] is not None:  # id_tp du student
              cursor.execute("SELECT * FROM ent.TP WHERE id = %s", (student[11],))
              tp_info = cursor.fetchone()
              if tp_info:
                student_info["tp"].append({
                  "id_tp": tp_info[0],
                  "name": tp_info[1],
                })
            
            if student[10] is not None:  # id_td du student
              cursor.execute("SELECT * FROM ent.TD WHERE id = %s", (student[10],))
              td_info = cursor.fetchone()
              if td_info:
                student_info["td"].append({
                  "id_td": td_info[0],
                  "name": td_info[1],
                })

            degree_info["students"].append(student_info)

        return jsonify(degree_info)

    except Exception as e:
        return student_info
    finally:
        cursor.close()
        conn.close()
