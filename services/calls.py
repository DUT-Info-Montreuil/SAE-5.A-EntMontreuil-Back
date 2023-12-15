# services/calls.py
import psycopg2
import connect_pg
from flask import jsonify

class CallsService:
    def __init__(self):
        pass

    def get_students_info_for_course(self, course_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT
                        S.id AS student_id,
                        U.last_name,
                        U.first_name,
                        CASE
                            WHEN C.id_Td IS NOT NULL THEN 'TD'
                            WHEN C.id_Tp IS NOT NULL THEN 'TP'
                            WHEN C.id_Promotion IS NOT NULL THEN 'Promotion'
                            ELSE 'Autre'
                        END AS course_type
                    FROM
                        ent.Students S
                        INNER JOIN ent.Users U ON S.id_User = U.id
                        INNER JOIN ent.Courses C ON S.id_Promotion = C.id_Promotion
                    WHERE
                        C.id = %s
                        AND (S.id_Td IS NOT NULL OR S.id_Tp IS NOT NULL OR S.id_Promotion IS NOT NULL)
                """
                cursor.execute(sql_query, (course_id,))
                rows = cursor.fetchall()

                students_info_list = []

                for row in rows:
                    student_info = {
                        "student_id": row[0],
                        "last_name": row[1],
                        "first_name": row[2],
                        "course_type": row[3]
                    }
                    students_info_list.append(student_info)

                return jsonify(students_info_list)
        except Exception as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)
    
    def get_students_with_absences_for_course(self, course_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT
                        S.id AS student_id,
                        U.username,
                        U.last_name,
                        U.first_name,
                        CASE WHEN A.id_Student IS NOT NULL THEN 'Absent' ELSE 'Présent' END AS presence_status
                    FROM
                        ent.Students S
                        INNER JOIN ent.Users U ON S.id_User = U.id
                        LEFT JOIN ent.Absences A ON S.id = A.id_Student AND A.id_Course = %s
                    WHERE
                        (S.id_Td IS NOT NULL OR S.id_Tp IS NOT NULL OR S.id_Promotion IS NOT NULL)
                """
                cursor.execute(sql_query, (course_id,))
                rows = cursor.fetchall()

                students_info_list = []

                for row in rows:
                    student_info = {
                        "student_id": row[0],
                        "username": row[1],
                        "last_name": row[2],
                        "first_name": row[3],
                        "presence_status": row[4]
                    }
                    students_info_list.append(student_info)
                return jsonify(students_info_list)
        except Exception as e:
            raise e
        finally:
            if conn:
                connect_pg.disconnect(conn)