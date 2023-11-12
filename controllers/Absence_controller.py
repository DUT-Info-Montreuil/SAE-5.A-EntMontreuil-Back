from flask import request, jsonify, Blueprint
import psycopg2
from services.absences import AbsencesService
import connect_pg

# Création d'un Blueprint pour les routes liées aux absences
absences_bp = Blueprint('absences', __name__)

# Instanciation du service d'absences
absences_service = AbsencesService()


#--------------------Récuperer toutes les absences--------------------------------------#

@absences_bp.route('/absences/dto', methods=['GET'])
def get_all_absences_dto():
    justified = request.args.get('justified', default=None, type=int)
    
    try:
        absences_list = absences_service.get_all_absences(justified=justified, output_format="DTO")
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@absences_bp.route('/absences/model', methods=['GET'])
def get_all_absences_model():
    justified = request.args.get('justified', default=None, type=int)
    
    try:
        absences_list = absences_service.get_all_absences(justified=justified, output_format="model")
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
#--------------------Récuperer toutes les absences d'un étudiant via son id--------------------------------------#

@absences_bp.route('/absences/student/<int:id_student>/dto', methods=['GET'])
def get_student_absences_dto(id_student):
    justified = request.args.get('justified', default=None, type=int)
    
    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    try:
        absences_list = absences_service.get_student_absences(id_student, justified=justified, output_format="DTO")
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@absences_bp.route('/absences/student/<int:id_student>/model', methods=['GET'])
def get_student_absences_model(id_student):

    justified = request.args.get('justified', default=None, type=int)
    
    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    try:
        absences_list = absences_service.get_student_absences(id_student, justified=justified, output_format="model")
        return jsonify(absences_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


#--------------------Modifier une  absence--------------------------------------#

@absences_bp.route('/absences/student/<int:id_student>/course/<int:id_course>', methods=['PUT'])
def update_student_course_absence(id_student, id_course):
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
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#--------------------ajouter  une  absence--------------------------------------#
@absences_bp.route('/absences/student/<int:id_student>/course/<int:id_course>/add', methods=['POST'])
def add_student_course_absence(id_student, id_course):
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
    data = {
        "id_student": id_student,
        "id_course": id_course
    }

    # Vérification que l'étudiant existe
    if not connect_pg.does_entry_exist("Students", id_student):
        return jsonify({"message": "L'étudiant spécifié n'existe pas."}), 404

    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM ent.Absences WHERE id_Student = %s AND id_Course = %s RETURNING id_Student, id_Course", (data["id_student"], data["id_course"]))
            deleted_row = cursor.fetchone()
            conn.commit()

            if deleted_row:
                return jsonify({"message": f"Absence supprimée pour l'étudiant {deleted_row[0]} et le cours {deleted_row[1]}"})
            else:
                return jsonify({"message": "Absence non trouvée ou déjà supprimée"}), 404
    except psycopg2.Error as e:
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            connect_pg.disconnect(conn)

