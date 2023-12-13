# services/calls.py
import psycopg2
import connect_pg
from entities.model.callsm import CallsModel
from entities.DTO.calls import Calls
from flask import jsonify

class CallsService:
    def __init__(self):
        pass

    def get_call_by_id(self, call_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ent.Calls WHERE id = %s", (call_id,))
                row = cursor.fetchone()
                if row:
                    call = CallsModel(*row)
                    return jsonify(call.jsonify())
                else:
                    return jsonify({"message": "Call not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Error retrieving call: {str(e)}"}), 500
        finally:
            conn.close()

    def update_call(self, call_id, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE ent.Calls
                    SET is_present = %s
                    WHERE id = %s
                    RETURNING id_Course, id_Student
                """, (data["is_present"], call_id))
                updated_row = cursor.fetchone()
                conn.commit()

                if updated_row:
                    return jsonify({"message": f"Call updated for course {updated_row[0]} and student {updated_row[1]}"})
                else:
                    return jsonify({"message": "Call not found or no changes made"}), 404
        except Exception as e:
            return jsonify({"error": f"Error updating call: {str(e)}"}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def add_call(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ent.Calls (id_Course, id_Student, is_present)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (data["id_Course"], data["id_Student"], data["is_present"]))
                inserted_call_id = cursor.fetchone()[0]
                conn.commit()

                return jsonify({"message": f"Call added successfully, ID: {inserted_call_id}"}), 200
        except Exception as e:
            return jsonify({"error": f"Error adding call: {str(e)}"}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def delete_call(self, call_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Calls WHERE id = %s RETURNING id_Course, id_Student", (call_id,))
                deleted_row = cursor.fetchone()
                conn.commit()

                if deleted_row:
                    return jsonify({"message": f"Call deleted successfully for course {deleted_row[0]} and student {deleted_row[1]}"})
                else:
                    return jsonify({"message": "Call not found or already deleted"}), 404
        except Exception as e:
            return jsonify({"error": f"Error deleting call: {str(e)}"}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def get_students_for_call(self, call_type, call_id):
        """
        Get the list of students for a specific call (promo, TD, TP).

        :param call_type: Type of call ("promo", "TD", or "TP").
        :param call_id: ID of the call (promo ID, TD ID, or TP ID).
        :return: List of students for the specified call.
        """
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                if call_type == "promo":
                    # Retrieve all students for the promotion
                    cursor.execute("""
                        SELECT S.id, S.id_User, U.last_name, U.first_name
                        FROM ent.Students S
                        INNER JOIN ent.Users U ON S.id_User = U.id
                        INNER JOIN ent.Promotions P ON S.id_Promotion = P.id
                        WHERE P.id = %s
                    """, (call_id,))
                elif call_type == "TD":
                    # Retrieve all students for the TD
                    cursor.execute("""
                        SELECT S.id, S.id_User, U.last_name, U.first_name
                        FROM ent.Students S
                        INNER JOIN ent.Users U ON S.id_User = U.id
                        WHERE S.id_Td = %s
                    """, (call_id,))
                elif call_type == "TP":
                    # Retrieve all students for the TP
                    cursor.execute("""
                        SELECT S.id, S.id_User, U.last_name, U.first_name
                        FROM ent.Students S
                        INNER JOIN ent.Users U ON S.id_User = U.id
                        INNER JOIN ent.TP T ON S.id_Tp = T.id
                        WHERE T.id = %s
                    """, (call_id,))
                else:
                    return jsonify({"error": "Invalid call type"}), 400

                rows = cursor.fetchall()
                students_list = []

                for row in rows:
                    student_info = {
                        "id": row[0],
                        "id_User": row[1],
                        "last_name": row[2],
                        "first_name": row[3],
                    }
                    students_list.append(student_info)

                return jsonify(students_list), 200

        except Exception as e:
            return jsonify({"error": f"Error getting students for call: {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def update_call_status(self, id_course, student_statuses):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Calls WHERE id_Course = %s", (id_course,))

                for student_status in student_statuses:
                    cursor.execute(
                        "INSERT INTO ent.Calls (id_Course, id_Student, is_present) VALUES (%s, %s, %s)",
                        (id_course, student_status["id_Student"], student_status["is_present"])
                    )

                    if not student_status["is_present"]:
                        absence_data = {
                            "id_student": student_status["id_Student"],
                            "id_course": id_course,
                            "reason": "Absent",  
                            "justify": False  
                        }
                        self.absences_service.add_student_course_absence(absence_data)

                conn.commit()

                return "Statut de l'appel mis à jour avec succès"
        except psycopg2.Error as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)