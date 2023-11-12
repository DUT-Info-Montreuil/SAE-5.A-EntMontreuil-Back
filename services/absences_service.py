import psycopg2
import connect_pg
from entities.model.absencesm import AbsencesModel
from entities.DTO.absences import   Absences
class AbsencesService:
    def __init__(self):
        pass

    def get_student_absences(self, id_student, justified=None, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Construisez la requête SQL en fonction de la justification
                sql_query = "SELECT A.id_Student, A.id_Course, A.reason, A.justify, C.dateCourse, C.startTime, C.endTime, U.last_name, U.first_name FROM ent.Absences A INNER JOIN ent.Courses C ON A.id_Course = C.id INNER JOIN ent.Students S ON A.id_Student = S.id INNER JOIN ent.Users U ON S.id_User = U.id WHERE A.id_Student = %s"
                if justified is not None:
                    if justified == 1:
                        sql_query += " AND A.justify = true"
                    elif justified == 0:
                        sql_query += " AND A.justify = FALSE"
             
                cursor.execute(sql_query, (id_student,))
                rows = cursor.fetchall()
                absences_list = []

                for row in rows:
                    if output_format == "DTO":
                        absence = Absences(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            justify=row[3]
                        )
                        absences_list.append(absence.jsonify())
                    elif output_format == "model":
                        absence = AbsencesModel(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            justify=row[3],
                            student_last_name=row[7],
                            student_first_name=row[8],
                            course_start_time=row[5],
                            course_end_time=row[6]
                        )
                        absences_list.append(absence.jsonify())

                return absences_list
        except Exception as e:
            raise e
        finally:
            conn.close()


    def get_all_absences(self, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT A.id_Student, A.id_Course, A.reason, A.justify, C.dateCourse, C.startTime, C.endTime, U.last_name, U.first_name FROM ent.Absences A INNER JOIN ent.Courses C ON A.id_Course = C.id INNER JOIN ent.Students S ON A.id_Student = S.id INNER JOIN ent.Users U ON S.id_User = U.id")
                rows = cursor.fetchall()
                absences_list = []

                for row in rows:
                    if output_format == "DTO":
                        absence = Absences(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            justify=row[3]
                        )
                        absences_list.append(absence.jsonify())
                    elif output_format == "model":
                        absence = AbsencesModel(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            justify=row[3],
                            student_last_name=row[7],
                            student_first_name=row[8],
                            course_start_time=row[5],
                            course_end_time=row[6]
                        )
                        absences_list.append(absence.jsonify())

                return absences_list
        except Exception as e:
            raise e
        finally:
            conn.close()

    def update_student_course_absence(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.Absences SET reason = %s, justify = %s WHERE id_Student = %s AND id_Course = %s RETURNING id_Student, id_Course",
                    (data["reason"], data["justify"], data["id_student"], data["id_course"])
                )
                updated_row = cursor.fetchone()
                conn.commit()

                if updated_row:
                    return f"Absence mise à jour pour l'étudiant {updated_row[0]} et le cours {updated_row[1]}"
                else:
                    return "Absence non trouvée ou aucune modification effectuée"
        except psycopg2.Error as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def add_student_course_absence(self, data):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Absences (id_Student, id_Course, reason, justify) VALUES (%s, %s, %s, %s) RETURNING id_Student, id_Course"
            values = (data["id_student"], data["id_course"], data["reason"], data["justify"])

            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_student_id, inserted_course_id = cursor.fetchone()

            return f"Absence ajoutée avec succès pour l'étudiant {inserted_student_id} lors du cours {inserted_course_id}"

        except psycopg2.Error as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def delete_student_course_absence(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Absences WHERE id_Student = %s AND id_Course = %s RETURNING id_Student, id_Course", (data["id_student"], data["id_course"]))
                deleted_row = cursor.fetchone()
                conn.commit()

                if deleted_row:
                    return f"Absence supprimée pour l'étudiant {deleted_row[0]} et le cours {deleted_row[1]}"
                else:
                    return "Absence non trouvée ou déjà supprimée"
        except psycopg2.Error as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)
