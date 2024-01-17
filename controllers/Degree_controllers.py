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
        cursor.execute("SELECT id, year, level FROM ent.Promotions WHERE id_degree = %s", (degree_id,))
        promotions = cursor.fetchall()
        promotions_dict = {promotion[0]: {"id": promotion[0], "year": promotion[1], "level": promotion[2]} for promotion in promotions}
        degree_info["promotions"].extend(promotions_dict.values())

        # Récupérer les étudiants
        cursor.execute("""
            SELECT u.*, s.apprentice, s.id_td, s.id_tp, s.id_promotion, s.id
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            WHERE s.id_promotion IN (SELECT id FROM ent.Promotions WHERE id_degree = %s)
        """, (degree_id,))
        students = cursor.fetchall()

        for student in students:
            student_info = {
                "id": student[0],
                "id_student": student[13],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[9],
                "id_promotion": student[12],
                "promotion": promotions_dict.get(student[12]),
                "tp": [],
                "td": []
            }

            # Récupérer les informations de TP et TD associées à chaque étudiant
            if student[11] is not None:
                cursor.execute("SELECT * FROM ent.TP WHERE id = %s", (student[11],))
                tp_info = cursor.fetchone()
                if tp_info:
                    student_info["tp"].append({
                        "id_tp": tp_info[0],
                        "name": tp_info[1]
                    })

            if student[10] is not None:
                cursor.execute("""
                    SELECT td.*, t.id, t.name, t.semester 
                    FROM ent.TD td
                    JOIN ent.Trainings t ON td.id_training = t.id
                    WHERE td.id = %s
                """, (student[10],))
                td_info = cursor.fetchone()
                if td_info:
                    training_info = {
                        "id": td_info[4],
                        "name": td_info[5],
                        "semester": td_info[6]
                    }
                    student_info["td"].append({
                        "id_td": td_info[0],
                        "name": td_info[1],
                        "training": training_info
                    })

            degree_info["students"].append(student_info)

        return jsonify(degree_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@degrees_bp.route('/cohort', methods=['GET'])
def get_cohort_tree():
    try:
        conn = connect_pg.connect()
        cursor = conn.cursor()

        # Récupérer tous les degrees
        cursor.execute("SELECT id, name FROM ent.Degrees")
        degrees = cursor.fetchall()

        cohort_tree = []

        for degree in degrees:
            degree_id, degree_name = degree

            # Récupérer les promotions pour chaque degree
            cursor.execute("SELECT id, year, level FROM ent.Promotions WHERE id_degree = %s", (degree_id,))
            promotions = cursor.fetchall()

            promotion_children = []

            for promo in promotions:
                promo_id, promo_year, promo_level = promo

                # Récupérer les formations pour chaque promotion
                cursor.execute("SELECT id, name FROM ent.Trainings WHERE id_promotion = %s", (promo_id,))
                trainings = cursor.fetchall()

                training_children = []

                for training in trainings:
                    training_id, training_name = training

                    # Récupérer les TDs pour chaque formation
                    cursor.execute("SELECT id, name FROM ent.TD WHERE id_training = %s", (training_id,))
                    tds = cursor.fetchall()

                    td_children = []

                    for td in tds:
                        td_id, td_name = td

                        # Récupérer les TPs pour chaque TD
                        cursor.execute("SELECT id, name FROM ent.TP WHERE id_td = %s", (td_id,))
                        tps = cursor.fetchall()

                        tp_children = [{"tp_id": tp[0], "label": tp[1], "url": f"/resp/cohort/tp/{tp[0]}", "data": "TP"} for tp in tps]

                        td_children.append({
                            "td_id": td_id,
                            "label": td_name,
                            "url": f"/resp/cohort/td/{td_id}",
                            "data": "TD",
                            "children": tp_children
                        })

                    training_children.append({
                        "label": training_name,
                        "data": "Parcours",
                        "url": f"/resp/cohort/training/{training_id}",
                        "children": td_children
                    })

                # Modifier le label ici
                promo_label = f"BUT {promo_level} {degree_name} {promo_year}"

                promotion_children.append({
                    "label": promo_label,
                    "data": "Promotion",
                    "url": f"/resp/cohort/promotion/{promo_id}",
                    "children": training_children
                })

            cohort_tree.append({
                "label": degree_name,
                "icon": "pi pi-fw pi-compass",
                "data": "Formation",
                "url": f"/resp/cohort/degree/{degree_id}",
                "children": promotion_children
            })

        return jsonify(cohort_tree)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@degrees_bp.route('/promotion/<int:promotion_id>', methods=['GET'])
def get_promotion_info(promotion_id):
    try:
        conn = connect_pg.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, year, level, id_degree FROM ent.Promotions WHERE id = %s", (promotion_id,))
        promotion_row = cursor.fetchone()
        if promotion_row is None:
            return jsonify({"error": "Promotion not found"}), 404

        promotion_info = {
            "id": promotion_row[0],
            "year": promotion_row[1],
            "level": promotion_row[2],
            "degree": {},
            "students": [],
            "trainings": []
        }

        cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (promotion_row[3],))
        degree_row = cursor.fetchone()
        if degree_row:
            promotion_info["degree"] = {"id": degree_row[0], "name": degree_row[1]}

        cursor.execute("""
            SELECT u.*, s.apprentice, s.id_td, s.id_tp, s.id_promotion, s.id
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            WHERE s.id_promotion = %s
        """, (promotion_id,))
        students = cursor.fetchall()

        for student in students:
            student_info = {
                "id": student[0],
                "id_student": student[13],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[9],
                "id_promotion": student[12],
                "tp": [],
                "td": [],
                "training": {}
            }

            if student[11] is not None:
                cursor.execute("SELECT * FROM ent.TP WHERE id = %s", (student[11],))
                tp_info = cursor.fetchone()
                if tp_info:
                    student_info["tp"].append({"id_tp": tp_info[0], "name": tp_info[1]})
            
            if student[10] is not None:
                cursor.execute("SELECT * FROM ent.TD WHERE id = %s", (student[10],))
                td_info = cursor.fetchone()
                if td_info:
                    student_info["td"].append({"id_td": td_info[0], "name": td_info[1]})

                    cursor.execute("SELECT t.id, t.name, t.semester FROM ent.Trainings t JOIN ent.TD td ON t.id = td.id_training WHERE td.id = %s", (td_info[0],))
                    training_info = cursor.fetchone()
                    if training_info:
                        student_info["training"] = {"id": training_info[0], "name": training_info[1], "semester": training_info[2]}

            promotion_info["students"].append(student_info)

        cursor.execute("SELECT t.id, t.name, t.semester FROM ent.Trainings t WHERE t.id_promotion = %s", (promotion_id,))
        trainings = cursor.fetchall()

        for training in trainings:
            cursor.execute("""
                SELECT COUNT(DISTINCT s.id)
                FROM ent.Students s
                JOIN ent.TD td ON s.id_td = td.id
                WHERE td.id_training = %s
            """, (training[0],))
            student_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM ent.TD WHERE id_training = %s", (training[0],))
            td_count = cursor.fetchone()[0]

            training_info = {
                "id": training[0],
                "name": training[1],
                "semester": training[2],
                "student_count": student_count,
                "td_count": td_count
            }
            promotion_info["trainings"].append(training_info)

        return jsonify(promotion_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@degrees_bp.route('/training/<int:training_id>', methods=['GET'])
def get_training_info(training_id):
    try:
        # Connexion à la base de données
        conn = connect_pg.connect()
        cursor = conn.cursor()

        # Récupérer les informations du training
        cursor.execute("SELECT id, name, semester, id_promotion FROM ent.Trainings WHERE id = %s", (training_id,))
        training_row = cursor.fetchone()
        if training_row is None:
            return jsonify({"error": "Training not found"}), 404

        training_info = {
            "id": training_row[0],
            "name": training_row[1],
            "semester": training_row[2],
            "degree": {},
            "promotion": {},
            "tds": [],
            "students": []
        }
        
        # Récupérer les informations du degree associé
        cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (training_row[3],))
        degree_row = cursor.fetchone()
        if degree_row:
            training_info["degree"] = {
                "id": degree_row[0],
                "name": degree_row[1]
            }
            
      # Récupérer les informations de la promotion associée
        cursor.execute("SELECT id, year, level FROM ent.Promotions WHERE id = %s", (training_row[3],))
        promotion_row = cursor.fetchone()
        if promotion_row:
            training_info["promotion"] = {
                "id": promotion_row[0],
                "year": promotion_row[1],
                "level": promotion_row[2]
            }

        # Récupérer les TDs associés au training
        cursor.execute("SELECT id, name FROM ent.TD WHERE id_training = %s", (training_id,))
        tds = cursor.fetchall()

        for td in tds:
            cursor.execute("SELECT COUNT(*) FROM ent.TP WHERE id_td = %s", (td[0],))
            tp_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT s.id)
                FROM ent.Students s
                WHERE s.id_td = %s
            """, (td[0],))
            student_count = cursor.fetchone()[0]

            td_info = {
                "id_td": td[0],
                "name": td[1],
                "tp_count": tp_count,
                "student_count": student_count
            }
            training_info["tds"].append(td_info)

        # Récupérer la liste des étudiants faisant partie du training
        cursor.execute("""
            SELECT DISTINCT u.*, s.id AS id_student, s.apprentice, s.id_td, s.id_tp
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            JOIN ent.TD td ON s.id_td = td.id
            WHERE td.id_training = %s
        """, (training_id,))
        students = cursor.fetchall()

        for student in students:
            student_info = {
                "id": student[0],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[10],
                "id_student": student[9],
                "tp": [],
                "td": []
            }

            # Ajouter les informations de TP spécifique pour l'étudiant
            if student[11] is not None:
                cursor.execute("SELECT * FROM ent.TP WHERE id = %s", (student[11],))
                tp_info = cursor.fetchone()
                if tp_info:
                    student_info["tp"].append({
                        "id_tp": tp_info[0],
                        "name": tp_info[1]
                    })

            # Ajouter les informations de TD
            if student[10]:
                td_info = next((td for td in training_info["tds"] if td["id_td"] == student[10]), None)
                if td_info:
                    student_info["td"].append(td_info)

            training_info["students"].append(student_info)

        return jsonify(training_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@degrees_bp.route('/td/<int:td_id>', methods=['GET'])
def get_td_info(td_id):
    try:
        conn = connect_pg.connect()
        cursor = conn.cursor()

        # Récupérer les informations du TD
        cursor.execute("SELECT id, name, id_training FROM ent.TD WHERE id = %s", (td_id,))
        td_row = cursor.fetchone()
        if td_row is None:
            return jsonify({"error": "TD not found"}), 404

        td_info = {
            "id": td_row[0],
            "name": td_row[1],
            "training": {},
            "promotion": {},
            "degree": {},
            "tps": [],
            "students": []
        }

        # Récupérer les informations du training associé
        cursor.execute("SELECT id, name, semester, id_promotion FROM ent.Trainings WHERE id = %s", (td_row[2],))
        training_row = cursor.fetchone()
        if training_row:
            td_info["training"] = {
                "id": training_row[0],
                "name": training_row[1],
                "semester": training_row[2]
            }

            # Récupérer les informations de la promotion et du degree associés
            cursor.execute("SELECT id, year, level, id_degree FROM ent.Promotions WHERE id = %s", (training_row[3],))
            promotion_row = cursor.fetchone()
            if promotion_row:
                td_info["promotion"] = {
                    "id": promotion_row[0],
                    "year": promotion_row[1],
                    "level": promotion_row[2]
                }

                cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (promotion_row[3],))
                degree_row = cursor.fetchone()
                if degree_row:
                    td_info["degree"] = {
                        "id": degree_row[0],
                        "name": degree_row[1]
                    }

        # Récupérer les TP associés au TD
        cursor.execute("SELECT id, name FROM ent.TP WHERE id_td = %s", (td_id,))
        tps = cursor.fetchall()

        for tp in tps:
            cursor.execute("""
                SELECT COUNT(DISTINCT s.id)
                FROM ent.Students s
                WHERE s.id_tp = %s
            """, (tp[0],))
            student_count = cursor.fetchone()[0]

            tp_info = {
                "id_tp": tp[0],
                "name": tp[1],
                "student_count": student_count
            }
            td_info["tps"].append(tp_info)

        # Récupérer la liste des étudiants faisant partie du TD
        cursor.execute("""
            SELECT DISTINCT u.*, s.id AS id_student, s.apprentice, s.id_tp
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            WHERE s.id_td = %s
        """, (td_id,))
        students = cursor.fetchall()

        for student in students:
            student_info = {
                "id": student[0],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[10],
                "id_student": student[9],
                "tp": []
            }

            # Ajouter les informations de TP spécifique pour l'étudiant
            if student[11] is not None:
                cursor.execute("SELECT * FROM ent.TP WHERE id = %s", (student[11],))
                tp_info = cursor.fetchone()
                if tp_info:
                    student_info["tp"].append({
                        "id_tp": tp_info[0],
                        "name": tp_info[1]
                    })

            td_info["students"].append(student_info)

        return jsonify(td_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@degrees_bp.route('/tp/<int:tp_id>', methods=['GET'])
def get_tp_info(tp_id):
    try:
        conn = connect_pg.connect()
        cursor = conn.cursor()

        # Récupérer les informations du TP
        cursor.execute("SELECT id, name, id_td FROM ent.TP WHERE id = %s", (tp_id,))
        tp_row = cursor.fetchone()
        if tp_row is None:
            return jsonify({"error": "TP not found"}), 404

        tp_info = {
            "id": tp_row[0],
            "name": tp_row[1],
            "td": {},
            "training": {},
            "promotion": {},
            "degree": {},
            "students": []
        }

        # Récupérer les informations du TD associé
        cursor.execute("SELECT id, name, id_training FROM ent.TD WHERE id = %s", (tp_row[2],))
        td_row = cursor.fetchone()
        if td_row:
            tp_info["td"] = {
                "id": td_row[0],
                "name": td_row[1]
            }

            # Récupérer les informations du training, promotion, et degree associés
            cursor.execute("SELECT id, name, semester, id_promotion FROM ent.Trainings WHERE id = %s", (td_row[2],))
            training_row = cursor.fetchone()
            if training_row:
                tp_info["training"] = {
                    "id": training_row[0],
                    "name": training_row[1],
                    "semester": training_row[2]
                }

                cursor.execute("SELECT id, year, level, id_degree FROM ent.Promotions WHERE id = %s", (training_row[3],))
                promotion_row = cursor.fetchone()
                if promotion_row:
                    tp_info["promotion"] = {
                        "id": promotion_row[0],
                        "year": promotion_row[1],
                        "level": promotion_row[2]
                    }

                    cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (promotion_row[3],))
                    degree_row = cursor.fetchone()
                    if degree_row:
                        tp_info["degree"] = {
                            "id": degree_row[0],
                            "name": degree_row[1]
                        }

        # Récupérer la liste des étudiants faisant partie du TP
        cursor.execute("""
            SELECT DISTINCT u.*, s.id AS id_student, s.apprentice
            FROM ent.Users u
            JOIN ent.Students s ON u.id = s.id_user
            WHERE s.id_tp = %s
        """, (tp_id,))
        students = cursor.fetchall()

        for student in students:
            student_info = {
                "id": student[0],
                "username": student[1],
                "last_name": student[3],
                "first_name": student[4],
                "isApprentice": student[10],
                "id_student": student[9]
            }
            tp_info["students"].append(student_info)

        return jsonify(tp_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

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