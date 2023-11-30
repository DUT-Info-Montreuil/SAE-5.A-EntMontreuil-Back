import psycopg2
import connect_pg
from entities.model.absencesm import AbsencesModel
from entities.DTO.absences import   Absences
from flask import jsonify
class AbsencesService:
    def __init__(self):
        pass

#-------------------- récuperer les abences d'un étudiant --------------------------------------#
    def get_student_absences(self, student_identifier, justified=None, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Modification de la requête pour supporter la recherche par id_student ou username
                sql_query = """
         SELECT A.id_Student, A.id_Course, A.reason, A.document, A.justify, C.dateCourse, 
                       C.startTime, C.endTime, U.last_name, U.first_name, R.name, C.datecourse
                FROM ent.Absences A 
                INNER JOIN ent.Courses C ON A.id_Course = C.id 
                INNER JOIN ent.Students S ON A.id_Student = S.id 
                INNER JOIN ent.Users U ON S.id_User = U.id
                INNER JOIN ent.Resources R ON C.id_Resource = R.id
                WHERE """

                # Déterminer si student_identifier est un ID ou un username
                if isinstance(student_identifier, int):
                    sql_query += "A.id_Student = %s"
                else:
                    sql_query += "U.username = %s"

                if justified is not None:
                    if justified:
                        sql_query += " AND A.justify = true"
                    else:
                        sql_query += " AND A.justify = FALSE"
                sql_query += "order by A.id"
                cursor.execute(sql_query, (student_identifier,))
                rows = cursor.fetchall()
                absences_list = []
                
                for row in rows:
                    if output_format == "DTO":
                        absence = Absences(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            document=row[3],
                            justify=row[4]
                        )
                        absences_list.append(absence.jsonify())
                    elif output_format == "model":
                        absence = AbsencesModel(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            document=row[3],
                            justify=row[4],
                            student_last_name=row[8],
                            student_first_name=row[9],
                            course_start_time=row[6],
                            course_end_time=row[7],
                            resource_name=row[10],
                            course_date=row[5]
                        )
                        absences_list.append(absence.jsonify())

                return absences_list
        except Exception as e:
            raise e
        finally:
            conn.close()


#-------------------- Récuperer toutes les absences --------------------------------------#
    def get_all_absences(self, justified=None, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Construisez la requête SQL en fonction de la justification
                sql_query = """
                            SELECT A.id_Student, A.id_Course, A.reason, A.document, A.justify, C.dateCourse, C.startTime, C.endTime, 
                                U.last_name, U.first_name, R.name
                            FROM ent.Absences A 
                            INNER JOIN ent.Courses C ON A.id_Course = C.id 
                            INNER JOIN ent.Students S ON A.id_Student = S.id 
                            INNER JOIN ent.Users U ON S.id_User = U.id
                            INNER JOIN ent.Resources R ON C.id_Resource = R.id
                            """

                if justified is not None:
                    if justified == 1:
                        sql_query += " WHERE A.justify = true"
                    elif justified == 0:
                        sql_query += " WHERE A.justify = false"

                cursor.execute(sql_query)
                rows = cursor.fetchall()

                absences_list = []

                for row in rows:
                    if output_format == "DTO":
                        absence = Absences(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            document=row[3],
                            justify=row[4]
                        )
                        absences_list.append(absence.jsonify())
                    else:
                        absence = AbsencesModel(
                            id_Student=row[0],
                            id_Course=row[1],
                            reason=row[2],
                            document=row[3],
                            justify=row[4],
                            student_last_name=row[8],
                            student_first_name=row[9],
                            course_start_time=row[6],
                            course_end_time=row[7],
                            resource_name=row[10],
                            course_date=row[5]
                        )
                        absences_list.append(absence.jsonify())

                return absences_list
        except Exception as e:
            raise e
        finally:
            conn.close()

#-------------------- Mettre à jour  une  absence--------------------------------------#

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

#-------------------- Ajouter une Absence--------------------------------------#

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
#-------------------- Supprimer une  absence--------------------------------------#
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

#-------------------- Envoyer un justificatif--------------------------------------#

    def submit_justification_document(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ent.Absences (id_Student, id_Course, document) VALUES (%s, %s, %s) RETURNING id_Student, id_Course",
                    (data["student_id"], data["id_course"], data["document"].read())
                )
                inserted_student_id, inserted_course_id = cursor.fetchone()
                conn.commit()

                return f"Justificatif envoyé avec succès pour l'étudiant {inserted_student_id} pour le cours de {inserted_course_id}"
        except psycopg2.Error as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)