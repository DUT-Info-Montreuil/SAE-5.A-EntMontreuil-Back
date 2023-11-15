import psycopg2
import connect_pg
from entities.DTO.classroom import Classroom
from entities.model.classroomm import ClassroomModel
from flask import jsonify

class ClassroomService:
    def __init__(self):
        pass

    def get_all_classrooms(self, output_format="model"):
        conn = None
        cursor = None  # Initialisez cursor en dehors du bloc try
        
        try:
            conn = connect_pg.connect()  # Remplacez cela par votre fonction de connexion réelle
            cursor = conn.cursor()

            if output_format == "model":
                # Si output_format est "model", retourne une liste de ClassroomModel
                cursor.execute("""
                    SELECT c.id, c.name, c.capacity, m.id AS material_id, m.equipment, cm.quantity
                    FROM ent.Classroom c
                    LEFT JOIN ent.CONTAINS cm ON c.id = cm.id_classroom
                    LEFT JOIN ent.Materials m ON cm.id_materials = m.id
                """)
                rows = cursor.fetchall()
                
                classroom_models = {}
                for row in rows:
                    classroom_id = row[0]
                    if classroom_id not in classroom_models:
                        classroom_model = ClassroomModel(
                            id=row[0],
                            name=row[1],
                            capacity=row[2],
                            materials=[]
                        )
                        classroom_models[classroom_id] = classroom_model

                    if row[3] is not None:
                        material = {
                            "id": row[3],
                            "equipment": row[4],
                            "quantity": row[5]
                        }
                        classroom_models[classroom_id].materials.append(material)

                result = [classroom_model.jsonify() for classroom_model in classroom_models.values()]
                return jsonify(result)
            else:
                # Si output_format est "dto" (ou tout autre format par défaut), retourne une liste de Classroom
                cursor.execute("SELECT * FROM ent.Classroom")
                rows = cursor.fetchall()

                classrooms = []
                for row in rows:
                    classroom = Classroom(
                        id=row[0],
                        name=row[1],
                        capacity=row[2]
                    )
                    classrooms.append(classroom.jsonify())

                return jsonify(classrooms)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
