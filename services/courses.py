import psycopg2
import connect_pg
from flask import jsonify
from entities.model.coursesm import CourseModel
from datetime import datetime, timedelta

class CourseService:
    #------------------get by id-----------------------
    def get_course_by_id(self, course_id):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Courses", 'id', course_id) :
                return {"error": f"l'id : {course_id} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.id = %s
                """

                cursor.execute(sql_query, (course_id,))
                row = cursor.fetchone()

                if row:
                    
                    
                    teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(course_id)
                    if status_code == 200:
                        teachers = teachers_result["teachers"]
                    else:
                        teachers = [] 
                        
                    classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(course_id)
                    if status_code == 200:
                        classrooms = classrooms_result["classrooms"]
                    else:
                        classrooms = [] 
                        
                    course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                    
                    return  {"courses": course_info.jsonify()}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #------------------get by day-----------------------
    def get_course_by_day(self, day):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.dateCourse = %s
                """

                cursor.execute(sql_query, (day,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []},200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()

    #------------------get by classroom!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-----------------------
    def get_course_by_classroom(self, classroom_name):
        try:
            
            if not CoursesFonction.field_exist("Classroom", 'name', classroom_name) :
                return {"error": f"la nom : {classroom_name} n'existe pas"}, 400
            response, status = CoursesFonction.get_all_id_courses_with_classroom_name(classroom_name)
            if status == 200 : 
                all_id_courses = response["courses"]
            else : 
                return {"courses": []}, 200
            courses_info = []
            for id_course in all_id_courses:
                course_details, status_code = self.get_course_by_id(id_course)
                if status_code == 200:
                    courses_info.append(course_details["courses"])
            return {"courses": courses_info}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
    #------------------get by promotion-----------------------
    def get_course_by_promotion(self, promotion_year):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Promotions", 'year', promotion_year) :
                return {"error": f"la promotion de : {promotion_year} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                   SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE P.year = %s
                """

                cursor.execute(sql_query, (promotion_year,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
    #------------------get by week-----------------------
    def get_course_by_week(self,start_date):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Supposons que la date soit au format 'YYYY-MM-DD'
                sql_query = '''
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.dateCourse >= %s AND C.dateCourse <= %s
                '''
            
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                end_date = start_date + timedelta(days=4)
                
                cursor.execute(sql_query, (start_date, end_date))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
            
     #------------------get by training-----------------------
    def get_course_by_training(self,training_id):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Trainings", 'id', training_id) :
                return {"error": f"l'id : {training_id} n'existe pas"}, 400
            with conn.cursor() as cursor:
                # Supposons que la date soit au format 'YYYY-MM-DD'
                sql_query = '''
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE tr.id = %s
                '''
                
                cursor.execute(sql_query, (training_id,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    #------------------get by teacher!!!!!!!!!!!!!!!-----------------------
    def get_course_by_teacher(self, teacher_username):
        try:
            if not CoursesFonction.teacher_username_exist(teacher_username) :
                return {"error": f"l'identifiant : {teacher_username} n'existe pas"}, 400
            response, status = CoursesFonction.get_all_id_courses_with_teacher_username(teacher_username)
            if status == 200 : 
                all_id_courses = response["courses"]
            else : 
                return {"courses": []}, 200
            courses_info = []
            for id_course in all_id_courses:
                course_details, status_code = self.get_course_by_id(id_course)
                if status_code == 200:
                    courses_info.append(course_details["courses"])
            return {"courses": courses_info}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500

           
    #------------------get by td----------------------- 
    def get_course_by_td(self, id_td):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("TD", 'id', id_td) :
                return {"error": f"l'id' : {id_td} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.id_Td = %s
                """

                cursor.execute(sql_query, (id_td,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #------------------get by tp-----------------------
    def get_course_by_tp(self, id_tp):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("TP", 'id', id_tp) :
                return {"error": f"l'id' : {id_tp} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.id_Tp = %s
                """

                cursor.execute(sql_query, (id_tp,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []

                    for row in rows:
                        teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                        if status_code == 200:
                            teachers = teachers_result["teachers"]
                        else:
                            teachers = [] 
                            
                        classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                        if status_code == 200:
                            classrooms = classrooms_result["classrooms"]
                        else:
                            classrooms = [] 
                            
                        course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #------------------get all-----------------------
    def get_all_courses(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training, tr.name, tr.semester, R.name, TP.name, TD.name, P.year, P.level, R.color
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    order by C.id
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                courses_list = []

                for row in rows:
                    teachers_result, status_code = CoursesFonction.get_all_teacher_courses_with_id_courses(row[0])
                    if status_code == 200:
                        teachers = teachers_result["teachers"]
                    else:
                        teachers = [] 
                        
                    classrooms_result, status_code = CoursesFonction.get_all_classroom_courses_with_id_courses(row[0])
                    if status_code == 200:
                        classrooms = classrooms_result["classrooms"]
                    else:
                        classrooms = [] 
                        
                    course_info = CourseModel(*row, teacher = teachers, classroom= classrooms)
                    courses_list.append(course_info.jsonify())
                return {"courses" : courses_list}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération des cours : {str(e)}"}, 500
        finally:
            conn.close()

    #----------------------add courses----------------------------------
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



class CoursesFonction : 
    #---------------recupere les information du teacher d'un cour
    def get_all_teacher_courses_with_id_courses (id_courses) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT t.id, u.username, u.first_name, u.last_name, t.initial  FROM ent.Courses_Teachers ct 
                    LEFT JOIN ent.Teachers t ON ct.id_Teacher = t.id
                    LEFT JOIN ent.Users u ON t.id_User = u.id
                    WHERE ct.id_Course = %s
                """

                cursor.execute(sql_query, (id_courses,))
                rows = cursor.fetchall()

                if rows :
                    teacher_list = []

                    for row in rows:
                        teacher_info = {
                            "id" : row[0],
                            "first_name" : row[2],
                            "last_name" : row[3],
                            "username" : row[1],
                            "initial" : row[4]
                        }
                        teacher_list.append(teacher_info)
                    return {"teachers": teacher_list}, 200
                else:
                    return {"message": "aucun prof"},400
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #---------------recupere les information d'une classe selon un cour
    def get_all_classroom_courses_with_id_courses (id_courses) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT c.id, c.name, c.capacity
                    FROM ent.Courses_Classrooms ct 
                    LEFT JOIN ent.Classroom c ON ct.id_Classroom = c.id
                    WHERE ct.id_Course = %s
                """

                cursor.execute(sql_query, (id_courses,))
                rows = cursor.fetchall()

                if rows :
                    classroom_list = []

                    for row in rows:
                        classroom_info = {
                            "id" : row[0],
                            "name" : row[1],
                            "capacity" : row[2]
                        }
                        classroom_list.append(classroom_info)
                    return {"classrooms": classroom_list}, 200
                else:
                    return {"message": "aucune salle"},400
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #---------------recupere les id_courses d'un teacher selon son username
    def get_all_id_courses_with_teacher_username (teacher_username) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT ct.id_course
                    FROM ent.Courses_Teachers ct 
                    LEFT JOIN ent.Teachers t ON ct.id_Teacher = t.id
                    INNER JOIN ent.Users u ON t.id_User = u.id
                    WHERE u.username = %s
                """

                cursor.execute(sql_query, (teacher_username,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []
                    for row in rows:
                        courses_list.append(row[0])
                    return {"courses": courses_list}, 200
                else:
                    return {"message": f"Aucune cour n'est attribuée à l'enseignant {teacher_username}"},400
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #---------------recupere les id_courses d'une salle selon son nom 
    def get_all_id_courses_with_classroom_name (classroom_name) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT ct.id_course
                    FROM ent.Courses_Classrooms ct 
                    LEFT JOIN ent.Classroom c ON ct.id_Classroom = c.id
                    WHERE c.name = %s
                """

                cursor.execute(sql_query, (classroom_name,))
                rows = cursor.fetchall()

                if rows :
                    courses_list = []
                    for row in rows:
                        courses_list.append(row[0])
                    return {"courses": courses_list}, 200
                else:
                    return {"message": f"Aucune cour n'est attribuée dans la salle {classroom_name}"},400
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
        
    #---------------permet de savoir si un champ existe dans une table        
    def field_exist (table, field, value) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = f"""
                    SELECT COUNT(*)
                    FROM ent.{table} 
                    WHERE {field} = %s
                """

                cursor.execute(sql_query, (value,))
                row = cursor.fetchone()
                return row[0]>0


        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()
            
    #---------------permet de savoir si le username d'un teaccher existe        
    def teacher_username_exist (teacher_username) : 
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT COUNT(*)
                    FROM ent.Teachers t INNER JOIN ent.Users u on u.id = t.id_User
                    WHERE u.username = %s
                """

                cursor.execute(sql_query, (teacher_username,))
                row = cursor.fetchone()
                return row[0]>0


        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()