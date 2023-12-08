import psycopg2
import connect_pg
from flask import jsonify

class CourseService:
    
    def get_course_by_id(self, course_id, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, R.id AS resource_id,
                           TP.id AS tp_id, TD.id AS td_id, P.id AS promotion_id, T.id AS teacher_id,
                           CL.id AS classroom_id
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Teachers T ON C.id_Teacher = T.id
                    LEFT JOIN ent.Classroom CL ON C.id_classroom = CL.id
                    WHERE C.id = %s
                """

                cursor.execute(sql_query, (course_id,))
                row = cursor.fetchone()

                if row:
                    course_info = {
                        "id": row[0],
                        "startTime": str(row[1]),
                        "endTime": str(row[2]),
                        "dateCourse": str(row[3]),
                        "control": row[4],
                        "resource_id": row[5],
                        "tp_id": row[6],
                        "td_id": row[7],
                        "promotion_id": row[8],
                        "teacher_id": row[9],
                        "classroom_id": row[10]
                    }

                    return course_info, 200
                else:
                    return {"message": "Cours non trouvé"}, 404
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()

    def get_all_courses(self, output_format="DTO"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, R.id AS resource_id,
                           TP.id AS tp_id, TD.id AS td_id, P.id AS promotion_id, T.id AS teacher_id,
                           CL.id AS classroom_id
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Teachers T ON C.id_Teacher = T.id
                    LEFT JOIN ent.Classroom CL ON C.id_classroom = CL.id
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                courses_list = []

                for row in rows:
                    course = {
                        "id": row[0],
                        "startTime": str(row[1]),
                        "endTime": str(row[2]),
                        "dateCourse": str(row[3]),
                        "control": row[4],
                        "resource_id": row[5],
                        "tp_id": row[6],
                        "td_id": row[7],
                        "promotion_id": row[8],
                        "teacher_id": row[9],
                        "classroom_id": row[10]
                    }

                    courses_list.append(course)

                return courses_list, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération des cours : {str(e)}"}, 500
        finally:
            conn.close()

    def add_course(self, data):
        try:
            conn = connect_pg.connect()
            query = """
                INSERT INTO ent.Courses (startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            values = (
                data["startTime"],
                data["endTime"],
                data["dateCourse"],
                data["control"],
                data["resource_id"],
                data["tp_id"],
                data["td_id"],
                data["promotion_id"],
                data["teacher_id"],
                data["classroom_id"]
            )

            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_course_id = cursor.fetchone()[0]

            return jsonify({
                "message": f"Cours ajouté avec succès, ID : {inserted_course_id}"
            }), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de l'ajout du cours : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def update_course(self, data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ent.Courses
                    SET startTime = %s, endTime = %s, dateCourse = %s, control = %s,
                        id_Resource = %s, id_Tp = %s, id_Td = %s, id_Promotion = %s,
                        id_Teacher = %s, id_classroom = %s
                    WHERE id = %s
                    RETURNING id
                    """,
                    (
                        data["startTime"],
                        data["endTime"],
                        data["dateCourse"],
                        data["control"],
                        data["resource_id"],
                        data["tp_id"],
                        data["td_id"],
                        data["promotion_id"],
                        data["teacher_id"],
                        data["classroom_id"],
                        data["id"]
                    )
                )
                updated_course_id = cursor.fetchone()

                conn.commit()

                if updated_course_id:
                    return jsonify({
                        "message": f"Cours mis à jour avec succès, ID : {updated_course_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Cours non trouvé ou aucune modification effectuée"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour du cours : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def delete_course(self, course_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ent.Courses WHERE id = %s RETURNING id", (course_id,)
                )
                deleted_course_id = cursor.fetchone()

                conn.commit()

                if deleted_course_id:
                    return jsonify({
                        "message": f"Cours supprimé avec succès, ID : {deleted_course_id[0]}"
                    }), 200
                else:
                    return jsonify({"message": "Cours non trouvé ou déjà supprimé"}), 404

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du cours : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def copy_day_courses(self, source_date, target_date):
            try:
                conn = connect_pg.connect()
                with conn.cursor() as cursor:
                    sql_query = """
                        INSERT INTO ent.Courses (startTime, endTime, dateCourse, control, id_Resource,
                                                id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom)
                        SELECT startTime, endTime, %s, control, id_Resource,
                            id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom
                        FROM ent.Courses
                        WHERE dateCourse = %s
                    """

                    cursor.execute(sql_query, (target_date, source_date))
                    conn.commit()

                    return jsonify({"message": "Cours copiés avec succès vers la nouvelle journée"}), 200
            except Exception as e:
                return jsonify({"message": f"Erreur lors de la copie des cours : {str(e)}"}), 500
            finally:
                conn.close()

    def copy_week_courses(self, source_week_start_date, target_week_start_date):
            try:
                conn = connect_pg.connect()
                with conn.cursor() as cursor:
                    sql_query = """
                        INSERT INTO ent.Courses (startTime, endTime, dateCourse, control, id_Resource,
                                                id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom)
                        SELECT startTime, endTime, %s + (dateCourse - %s), control, id_Resource,
                            id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom
                        FROM ent.Courses
                        WHERE dateCourse >= %s AND dateCourse < %s
                    """

                    cursor.execute(sql_query, (target_week_start_date, source_week_start_date,
                                            source_week_start_date, source_week_start_date + 7))
                    conn.commit()

                    return jsonify({"message": "Cours copiés avec succès vers la nouvelle semaine"}), 200
            except Exception as e:
                return jsonify({"message": f"Erreur lors de la copie des cours : {str(e)}"}), 500
            finally:
                conn.close()

def get_courses_by_day(self, target_date):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT * FROM ent.Courses
                    WHERE dateCourse = %s
                """
                cursor.execute(sql_query, (target_date,))
                rows = cursor.fetchall()
                courses_list = self._format_courses(rows)
                return courses_list, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération des cours pour la journée : {str(e)}"}, 500
        finally:
            conn.close()

def get_courses_by_week(self, target_week_start_date):
    try:
        conn = connect_pg.connect()
        with conn.cursor() as cursor:
            sql_query = """
                SELECT * FROM ent.Courses
                WHERE dateCourse >= %s AND dateCourse < %s
            """
            cursor.execute(sql_query, (target_week_start_date, target_week_start_date + 7))
            rows = cursor.fetchall()
            courses_list = self._format_courses(rows)
            return courses_list, 200
    except Exception as e:
        return {"message": f"Erreur lors de la récupération des cours pour la semaine : {str(e)}"}, 500
    finally:
        conn.close()

def _format_courses(self, rows):
    courses_list = []
    for row in rows:
        course = {
            "id": row[0],
            "startTime": str(row[1]),
            "endTime": str(row[2]),
            "dateCourse": str(row[3]),
            "control": row[4],
            "resource_id": row[5],
            "tp_id": row[6],
            "td_id": row[7],
            "promotion_id": row[8],
            "teacher_id": row[9],
            "classroom_id": row[10]
        }
        courses_list.append(course)
    return courses_list            