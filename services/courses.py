import psycopg2
import connect_pg
from flask import jsonify
from entities.model.coursesm import CourseModel
from datetime import datetime, timedelta

class CourseService:
    ####################### GETTER ######################
    #------------------get by id-----------------------
    def get_course_by_id(self, course_id):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Courses", 'id', course_id) :
                return {"error": f"l'id : {course_id} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                    SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                    if row[8] :
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                    if row[9] :
                        response, status = CoursesFonction.get_group_of_td(row[9])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = [row[9]],id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                    if row[10] :
                        response, status = CoursesFonction.get_group_of_promotion(row[10])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = response["td"],id_Promotion = [row[10]],id_Training = response["training"], teacher = teachers, classroom= classrooms)
                    if row[11] :
                        response, status = CoursesFonction.get_group_of_training(row[11])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = response["td"],id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
                        
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                        if row[8] :
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                            
                        if row[9] :
                            response, status = CoursesFonction.get_group_of_td(row[9])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = [row[9]],id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        if row[10] :
                            response, status = CoursesFonction.get_group_of_promotion(row[10])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = response["td"],id_Promotion = [row[10]],id_Training = response["training"], teacher = teachers, classroom= classrooms)
                        if row[11] :
                            response, status = CoursesFonction.get_group_of_training(row[11])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = response["td"],id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
                        
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []},200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()

    #------------------get by classroom-----------------------
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
    def get_course_by_promotion(self, promotion_id,semester):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Promotions", 'id', promotion_id) :
                return {"error": f"la promotion de : {promotion_id} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                 SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training ,trr.semester
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.Trainings trr ON R.id_Training = trr.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE P.id = %s AND trr.semester = %s
                """
                cursor.execute(sql_query, (promotion_id,semester))
                rows = cursor.fetchall()
       
                courses_promotion = []
                courses_training = []
                courses_td = []
                courses_tp = []
                response, status = CoursesFonction.get_group_of_promotion(promotion_id)
                tp = response["tp"]
                td = response["td"]
                training = response["training"]
                if rows :
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
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = response["td"],id_Promotion = [row[10]],id_Training = response["training"], teacher = teachers, classroom= classrooms)
                        courses_promotion.append(course_info.jsonify())
                        
                if training : 
                    for id in training :
                        if CoursesFonction.verifie_id_in_courses('id_training' , id) :
                            response, status = CoursesFonction.get_course_by_training_fonction(id)
                            for course in response["courses"] :
                                courses_training.append(course)
                if td :
                    for id in td :
                        if CoursesFonction.verifie_id_in_courses('id_td' , id) :
                            response, status = CoursesFonction.get_course_by_td_fonction(id)
                            for course in response["courses"] :
                                courses_td.append(course)
                if tp :
                    for id in tp :
                        if CoursesFonction.verifie_id_in_courses('id_tp' , id) :
                            response, status = CoursesFonction.get_course_by_tp_fonction(id)
                            for course in response["courses"] :
                                courses_tp.append(course)
                    
                courses_list = {
                    "courses_promotion" : courses_promotion,
                    "courses_training" : courses_training,
                    "courses_td" : courses_td,
                    "courses_tp" : courses_tp
                }                  
                        
                return {"courses": courses_list}, 200
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
                    FROM ent.Courses C
                    LEFT JOIN ent.Resources R ON C.id_Resource = R.id
                    LEFT JOIN ent.TP TP ON C.id_Tp = TP.id
                    LEFT JOIN ent.TD TD ON C.id_Td = TD.id
                    LEFT JOIN ent.Promotions P ON C.id_Promotion = P.id
                    LEFT JOIN ent.Trainings tr ON C.id_Training = tr.id
                    WHERE C.dateCourse >= %s AND C.dateCourse <= %s
                '''
            
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
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
                            
                        if row[8] :
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        if row[9] :
                            response, status = CoursesFonction.get_group_of_td(row[9])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = [row[9]],id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        if row[10] :
                            response, status = CoursesFonction.get_group_of_promotion(row[10])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = response["td"],id_Promotion = [row[10]],id_Training = response["training"], teacher = teachers, classroom= classrooms)
                        if row[11] :
                            response, status = CoursesFonction.get_group_of_training(row[11])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = response["td"],id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                courses_training = []
                courses_td = []
                courses_tp = []
                response, status = CoursesFonction.get_group_of_training(training_id)
                tp = response["tp"]
                td = response["td"]
                if rows :
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
                            
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = tp,id_Td = td ,id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
                        courses_training.append(course_info.jsonify())
                
                if td :
                    for id in td :
                        if CoursesFonction.verifie_id_in_courses('id_td' , id) :
                            response, status = CoursesFonction.get_course_by_td_fonction(id)
                            for course in response["courses"] : 
                                courses_td.append(course)
                if tp :
                    for id in tp :
                        if CoursesFonction.verifie_id_in_courses('id_tp' , id) :
                            response, status = CoursesFonction.get_course_by_tp_fonction(id)
                            for course in response["courses"] :
                                courses_tp.append(course)
                
                courses_list = {
                    "courses_training" : courses_training,
                    "courses_td" : courses_td,
                    "courses_tp" : courses_tp
                }                  
            return {"courses": courses_list}, 200
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                courses_td = []
                courses_tp = []
                response, status = CoursesFonction.get_group_of_td(id_td)
                tp = response["tp"]
                if rows :
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
                        
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = tp,id_Td = [row[9]] ,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        courses_td.append(course_info.jsonify())
                    
                if tp :
                    for id in tp :
                        if CoursesFonction.verifie_id_in_courses('id_tp' , id) :
                            response, status = CoursesFonction.get_course_by_tp_fonction(id)
                            for course in response["courses"] :
                                courses_tp.append(course)
            
                courses_list = {
                    "courses_td" : courses_td,
                    "courses_tp" : courses_tp
                }                  
                
            return {"courses": courses_list}, 200
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                    courses_tp = []

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
                            
                        if row[8] :
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        courses_tp.append(course_info.jsonify())
                    courses_list = {
                        "courses_tp" : courses_tp
                    }     
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
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                        
                    if row[8] :
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                    if row[9] :
                        response, status = CoursesFonction.get_group_of_td(row[9])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = [row[9]],id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                    if row[10] :
                        response, status = CoursesFonction.get_group_of_promotion(row[10])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = response["td"],id_Promotion = [row[10]],id_Training = response["training"], teacher = teachers, classroom= classrooms)
                    if row[11] :
                        response, status = CoursesFonction.get_group_of_training(row[11])
                        course_info = CourseModel(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                        id_Tp = response["tp"],id_Td = response["td"],id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
                    courses_list.append(course_info.jsonify())
                return {"courses" : courses_list}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération des cours : {str(e)}"}, 500
        finally:
            conn.close()

    ########################### POST ###################################
    #----------------------add courses----------------------------------
    def add_course(self, data):
        try:
            conn = connect_pg.connect()
            
            fields_present = ["id_tp", "id_td", "id_promotion", "id_training"]
            present_count = sum(1 for field in fields_present if field in data)
            
            if present_count != 1:
                return {"error": "Un seul champ parmi [ id_tp - id_td - id_promotion - id_training ] doit être présent"}, 400
        
            if 'id_tp' in data :
                if not CoursesFonction.field_exist('TP', 'id' , data["id_tp"]) :
                    return {"error": f"l'id_tp {data.get('id_tp')} n'existe pas"}, 400
            if 'id_td' in data :
                if not CoursesFonction.field_exist('TD', 'id' , data["id_td"]) :
                    return {"error": f"l'id_td {data.get('id_td')} n'existe pas"}, 400
            if 'id_promotion' in data :
                if not CoursesFonction.field_exist('Promotions', 'id' , data["id_promotion"]) :
                    return {"error": f"l'id_promotion {data.get('id_promotion')} n'existe pas"}, 400
            if 'id_training' in data :
                if not CoursesFonction.field_exist('Trainings', 'id' , data["id_training"]) :
                    return {"error": f"l'id_training {data.get('id_training')} n'existe pas"}, 400
            if not CoursesFonction.field_exist('Resources', 'id' , data["id_resource"]) :
                    return {"error": f"l'id_resource {data.get('id_resource')} n'existe pas"}, 400
                
            time_format = '%H:%M'  # Format HH-MM
            data["startTime"] = datetime.strptime(data.get('startTime'), '%H:%M').strftime(time_format)
            
            data['endTime'] = datetime.strptime(data.get('endTime'), '%H:%M').strftime(time_format)
            data['dateCourse'] = datetime.strptime(data.get('dateCourse'), '%Y-%m-%d').strftime('%Y-%m-%d')
            
            response, status =  CoursesFonction.check_course_overlap(data) 
            if status != 200 :
                return response, status
            
            # Vérification des teachers id
            if data["teachers_id"] :
                for id in data["teachers_id"] :
                    if not CoursesFonction.field_exist('Teachers', 'id' , id) :
                        return {"error": f"l'id de l'enseignant : {id} n'existe pas"}, 400
            
            if data["classrooms_id"] :
                for id in data["classrooms_id"] :
                    if not CoursesFonction.field_exist('Classroom', 'id' , id) :
                        return {"error": f"l'id de la classe : {id} n'existe pas"}, 400
            
            # Vérification des champs présents et validation réussie, procédez à l'insertion
            query = """
                INSERT INTO ent.Courses (startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Training)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            
            id_Tp = data.get('id_tp') if 'id_tp' in data else None
            id_Td = data.get('id_td') if 'id_td' in data else None
            id_Promotion = data.get('id_promotion') if 'id_promotion' in data else None
            id_Training = data.get('id_training') if 'id_training' in data else None
            cursor = conn.cursor()
            cursor.execute(query, (data.get('startTime'), data.get('endTime'), data.get('dateCourse'), data.get('control'), data.get('id_resource'), id_Tp, id_Td, id_Promotion, id_Training))
            new_course_id = cursor.fetchone()[0] 
            conn.commit()

            if new_course_id :
                if data["teachers_id"] :
                    query_sql = """
                                    INSERT INTO ent.Courses_Teachers (id_Course, id_Teacher)
                                    VALUES (%s, %s)
                                """
                    for id in data["teachers_id"] :
                        cursor.execute(query_sql, (new_course_id, id))
                        conn.commit()
                if data["classrooms_id"] :
                    query_sql = """
                                    INSERT INTO ent.Courses_Classrooms (id_Course, id_Classroom)
                                    VALUES (%s, %s)
                                """
                    for id in data["classrooms_id"] :
                        cursor.execute(query_sql, (new_course_id, id))
                        conn.commit()
                new_course=self.get_course_by_id(new_course_id)

                return {"message": "Cours ajouté avec succès" , "id" : new_course_id,"course":new_course}, 200
            else :
                return {"error": "Une erreur est survenue lors de l'ajout du cours"}, 400

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de l'ajout du cours : {str(e)}"}), 500

        finally:
            conn.close()
            
    ############################## DELETE ##################################
    
    #--------with id -------------
    def delete_course_with_id(self, course_id):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist('Courses', 'id', course_id) :
                return jsonify({"error": f"L'id du cour : {course_id} n'existe pas"}), 400
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ent.Courses WHERE id = %s", (course_id,))
                conn.commit()
                return jsonify({"message": f"Cours supprimé avec succès, ID : {course_id}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du cours : {str(e)}"}), 500

        finally:
            conn.close()
    #--------with day -------------    
    def delete_course_with_day(self, day, group):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist('Courses', 'dateCourse', day) :
                return jsonify({"error": f"Aucun cours trouvé pour ce jour : {day} "}), 400
            
            if "id_tp" in group :
                group_name = "id_tp"
            if "id_td" in group : 
                group_name = "id_td"
            if "id_training" in group : 
                group_name = "id_training"
            if "id_promotion" in group : 
                group_name = "id_promotion"

            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM ent.Courses WHERE dateCourse = %s AND {group_name} = %s", (day,group.get(group_name)))
                conn.commit()
                return jsonify({"message": f"Cours supprimé avec succès, jour : {day}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression du cours : {str(e)}"}), 500

        finally:
            conn.close()
            
    #--------with with start day and end day -------------    
    def delete_course_with_many_day(self, start_day, end_day, group):
        try:
            conn = connect_pg.connect()
            # Vérification des formats de date
            try:
                start_date = datetime.strptime(start_day, '%Y-%m-%d')
                end_date = datetime.strptime(end_day, '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Le format de date est incorrect. Utilisez le format YYYY-MM-DD."}), 400

            # Vérification si start_day est inférieur ou égal à end_day
            if start_date >= end_date:
                return jsonify({"error": "La date de début doit être antérieure à la date de fin."}), 400
            
            if "id_tp" in group :
                group_name = "id_tp"
            if "id_td" in group : 
                group_name = "id_td"
            if "id_training" in group : 
                group_name = "id_training"
            if "id_promotion" in group : 
                group_name = "id_promotion"

            # Vérification si des cours existent entre les dates spécifiées
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM ent.Courses WHERE dateCourse BETWEEN %s AND %s AND {group_name} = %s", (start_day, end_day, data.get(group_name)))
                count = cursor.fetchone()[0]

                if count == 0:
                    return jsonify({"message": "Aucun cours trouvé entre les dates spécifiées pour le groupe."}), 400

                # Suppression des cours entre les deux dates
                cursor.execute(f"DELETE FROM ent.Courses WHERE dateCourse BETWEEN %s AND %s AND {group_name} = %s", (start_day, end_day, data.get(group_name)))
                conn.commit()
                return jsonify({"message": f"Cours supprimés avec succès entre {start_day} et {end_day}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression des cours : {str(e)}"}), 500

        finally:
            conn.close()
        
    #------------------delete by resource---------------------    
    def delete_course_with_resource(self, id_resource):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM ent.Courses WHERE id_resource  = %s", (id_resource,))
                conn.commit()
                return jsonify({"message": f"Cours supprimés avec succès pour l'id resource {id_resource}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression des cours : {str(e)}"}), 500

        finally:
            conn.close()
            
    #------------------delete by teacher---------------------    
    def delete_course_with_teacher(self, id_teacher):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_course from ent.Courses_Teachers where id_teacher = %s", (id_teacher,))
                rows = cursor.fetchall()
                all_courses = []
                for row in rows :
                    cursor.execute(f"DELETE FROM ent.Courses WHERE id  = %s", (row[0],))
                conn.commit()
                return jsonify({"message": f"Cours supprimés avec succès pour l'id teacher {id_teacher}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la suppression des cours : {str(e)}"}), 500

        finally:
            conn.close()
        
    
    ############################ PATCH ###############################

    def update_course(self, data,course_id):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ent.Courses
                    SET startTime = %s, endTime = %s, dateCourse = %s, control = %s,
                        id_Resource = %s, id_Tp = %s, id_Td = %s, id_Promotion = %s, id_Training = %s
                    WHERE id = %s
                    """,
                    (
                        data["startTime"],
                        data["endTime"],
                        data["dateCourse"],
                        data["control"],
                        data["id_resource"],
                        data["id_tp"],
                        data["id_td"],
                        data["id_promotion"],
                        data["id_training"],
                        course_id
                    )
                )
                
                cursor.execute(
                    """
                    DELETE from ent.Courses_Classrooms
                    WHERE id_Course = %s
                    """,
                    (course_id,)
                )
                
                for id in data["classrooms"] :
                    cursor.execute(
                        """
                        INSERT INTO ent.Courses_Classrooms (id_course, id_classroom) VALUES (%s, %s)
                        """,
                        (course_id,id)
                    )
                    
                cursor.execute(
                    """
                    DELETE from ent.Courses_Teachers
                    WHERE id_Course = %s
                    """,
                    (course_id,)
                )
                
                for id in data["teachers"] :
                    cursor.execute(
                        """
                        INSERT INTO ent.Courses_Teachers (id_course, id_teacher) VALUES (%s, %s)
                        """,
                        (course_id,id)
                    )
                
                conn.commit()

                return jsonify({"message": f"Cours mis à jour avec succès, ID : {course_id}"}), 200

        except psycopg2.Error as e:
            return jsonify({"message": f"Erreur lors de la mise à jour du cours : {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def copy_day_courses(self, source_date, target_date):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                # Supprimer les cours existants pour le jour cible
                delete_query = """
                    DELETE FROM ent.Courses
                    WHERE dateCourse = %s
                """
                cursor.execute(delete_query, (target_date,))
    
                # Copier les cours pour le jour cible
                insert_query = """
                    INSERT INTO ent.Courses (
                        startTime, endTime, dateCourse, control, id_Resource,
                        id_Tp, id_Td, id_Promotion, id_Training
                    )
                    SELECT
                        startTime, endTime, %s, control, id_Resource,
                        id_Tp, id_Td, id_Promotion, id_Training
                    FROM ent.Courses
                    WHERE dateCourse = %s
                """
                cursor.execute(insert_query, (target_date, source_date))
    
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
                # Supprimer les cours existants pour la semaine cible
                delete_query = """
                    DELETE FROM ent.Courses
                    WHERE dateCourse >= %s AND dateCourse < %s
                """
                cursor.execute(delete_query, (target_week_start_date, target_week_start_date + 5))
    
                # Copier les cours pour la semaine cible
                insert_query = """
                    INSERT INTO ent.Courses (
                        startTime, endTime, dateCourse, control, id_Resource,
                        id_Tp, id_Td, id_Promotion, id_Training
                    )
                    SELECT
                        startTime, endTime, %s + (dateCourse - %s), control, id_Resource,
                        id_Tp, id_Td, id_Promotion, id_Training
                    FROM ent.Courses
                    WHERE dateCourse >= %s AND dateCourse < %s
                """
                cursor.execute(insert_query, (target_week_start_date, source_week_start_date,
                                              source_week_start_date, source_week_start_date + 5))
    
                conn.commit()
    
                return jsonify({"message": "Cours copiés avec succès vers la nouvelle semaine"}), 200
        except Exception as e:
            return jsonify({"message": f"Erreur lors de la copie des cours : {str(e)}"}), 500
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
            
    # check si il y a deja un cours présent
    def check_course_overlap( data):
        try:
            response, status =  CoursesFonction.check_course_overlap(data) 
            if status != 200 :
                return response, status
            conn = connect_pg.connect()
            cursor = conn.cursor()
            
            # Convertir les dates et heures en objets datetime pour la comparaison
            start_time = datetime.strptime(data['startTime'], '%H:%M').time()
            end_time = datetime.strptime(data['endTime'], '%H:%M').time()
            date_course = datetime.strptime(data['dateCourse'], '%Y-%m-%d').date()
            
            where_clause = ""
            group = ""
        
            if "id_tp" in data and data["id_tp"] is not None:
                group = f"le tp {data.get('id_tp')}"
                response , status = CoursesFonction.get_group_of_tp(data["id_tp"])
                if status != 200 :
                    return response , status
                where_clause = f"AND (id_Tp = {data.get('id_tp')} OR id_Training = {response.get('training')} OR id_Promotion = {response.get('promotion')} OR id_Td = {response.get('td')})"
                
            if "id_td" in data and data["id_td"] is not None:
                group = f"le td {data.get('id_td')}"
                response , status = CoursesFonction.get_group_of_td(data["id_td"])
                if status != 200 :
                    return response , status
                tp_list = response["tp"]
                where_clause = f"AND (id_Td = {data.get('id_td')} OR id_Training = {response.get('training')} OR id_Promotion = {response.get('promotion')}"
                if tp_list :
                    where_clause += f" OR id_Tp IN ({', '.join(map(str, tp_list))})"
                where_clause += ")"   
                
            if "id_training" in data and data["id_training"] is not None:
                group = f"le parcour {data.get('id_training')}"
                response , status = CoursesFonction.get_group_of_training(data["id_training"])
                if status != 200 :
                    return response , status
                td_list = response["td"]
                tp_list = response["tp"]
                where_clause = f"AND (id_Training = {data.get('id_training')} OR id_Promotion = {response.get('promotion')}"
                if td_list :
                    where_clause += f" OR id_Td IN ({', '.join(map(str, td_list))})"
                if tp_list :
                    where_clause += f" OR id_Tp IN ({', '.join(map(str, tp_list))})"
                where_clause += ")"
         
                
            if "id_promotion" in data and data["id_promotion"] is not None:
                where_clause = f"AND id_Promotion = {data.get('id_promotion')}"
                group = f"la promotion {data.get('id_promotion')}"
                response , status = CoursesFonction.get_group_of_promotion(data["id_promotion"])
                if status != 200 :
                    return response , status
                td_list = response["td"]
                tp_list = response["tp"]
                training_list = response["training"]
                
                where_clause = f"AND (id_Promotion = {data.get('id_promotion')}"
                if td_list :
                    where_clause += f" OR id_Td IN ({', '.join(map(str, td_list))})" 
                if training_list :
                    where_clause += f" OR id_Training IN ({', '.join(map(str, training_list))})"
                if tp_list :
                    where_clause += f" OR id_Tp IN ({', '.join(map(str, tp_list))})" 
                where_clause += ")"
                
                

            query = """
                SELECT * FROM ent.Courses
                WHERE dateCourse = %s
                AND (
                    (startTime < %s AND endTime > %s)
                    OR (startTime < %s AND endTime > %s)
                    OR (startTime = %s AND endTime = %s)
                ) 
            """ + where_clause 

            cursor.execute(query, (date_course, start_time, start_time, end_time, end_time, start_time, end_time))
            overlapping_courses = cursor.fetchall()
            if not overlapping_courses :
                return {"message": f"Validation , le cour peut etre ajouté"}, 200
            return {"error": f"Un cours est déjà présent"}, 400

        except Exception as e:
            return {"message": f"Erreur dans check_course_overlap : {str(e)}"}, 500

    # recuperation des groupes liés au tp
    def get_group_of_tp(id_tp) :
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()   
            TD = None
            Training = None         
            Promotion = None
            query = """
                SELECT td.id, td.id_training, td.id_promotion FROM ent.TP tp
                INNER JOIN ent.TD td on tp.id_Td = td.id
                WHERE tp.id = %s
            """
            cursor.execute(query, (id_tp,))
            row = cursor.fetchone()
            if row:
                TD = row[0]
                Training = row[1]
                Promotion = row[2]
            else:
                return {"message": "Aucun TP trouvé avec cet ID"}, 400
            return {"td": TD, "training" : Training, "promotion" : Promotion}, 200

        except Exception as e:
            return {"message": f"Erreur dans get_group_of_tp : {str(e)}"}, 500
     
    # recuperation des groupes liés au td   
    def get_group_of_td(id_td) :
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()            
            training = None
            promotion = None
            tps = None
            query = """
                SELECT id_training,id_promotion FROM ent.TD 
                Where id = %s

            """
            cursor.execute(query, (id_td,))
            row = cursor.fetchone()
            if row:
                training, promotion = row
            else:
                return {"message": "Aucun TD trouvé avec cet ID"}, 400
            
            query2 = """
                SELECT tp.id FROM ent.TP tp
                INNER JOIN ent.TD td on tp.id_Td = td.id
                Where td.id = %s

            """
            cursor.execute(query2, (id_td,))
            rows = cursor.fetchall()
            if rows :
                tps = []
                for row in rows :
                    tps.append(row[0])
            conn.close()
            return {"tp": tps, "training" : training, "promotion" : promotion}, 200

        except Exception as e:
            return {"message": f"Erreur dans get_group_of_td : {str(e)}"}, 500
        
        
    # recuperation des groupes liés au training   
    def get_group_of_training(id_training) :
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()            
            promotion = None
            tds = None
            tps = None
            
            query = """
                SELECT id,id_promotion FROM ent.TD 
                Where id_training = %s
            """
            cursor.execute(query, (id_training,))
            rows = cursor.fetchall()
            if rows :
                tds = []
                for row in rows :
                    tds.append(row[0])
                promotion = rows[0][1]
            
            query_2 = """
                SELECT tp.id FROM ent.TD td
                INNER JOIN ent.TP tp on tp.id_Td = td.id
                Where td.id = %s

            """
            if tds :
                tps = []
                for td in tds :
                    cursor.execute(query_2, (td,))
                    rows = cursor.fetchall()
                    if rows :
                        for row in rows :
                            tps.append(row[0])
            
            return {"tp": tps, "td" : tds, "promotion" : promotion}, 200

        except Exception as e:
            return {"message": f"Erreur get_group_of_training : {str(e)}"}, 500
        
    # recuperation des groupes liés a une promotion  
    def get_group_of_promotion(id_promotion):
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()
            
            query = """
                SELECT tr.id AS training_id, td.id AS td_id, tp.id AS tp_id 
                FROM ent.Trainings tr
                LEFT JOIN ent.TD td ON tr.id = td.id_training
                LEFT JOIN ent.TP tp ON td.id = tp.id_td
                WHERE tr.id_promotion = %s
            """
            cursor.execute(query, (id_promotion,))
            rows = cursor.fetchall()
            
            trainings = list(set([row[0] for row in rows if row[0] is not None]))
            tds = list(set([row[1] for row in rows if row[1] is not None]))
            tps = list(set([row[2] for row in rows if row[2] is not None]))
            
            conn.close()
            
            return {"tp": tps, "td": tds, "training": trainings}, 200

        except Exception as e:
            return {"message": f"Erreur get_group_of_promotion : {str(e)}"}, 500
        
    # verifie si id trainings est present dans la table courses  
    def verifie_id_in_courses(field, value):
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()
            
            query = f"""
                SELECT COUNT(*) FROM ent.Courses
                WHERE {field} = %s
            """
            cursor.execute(query, (value,))
            row = cursor.fetchone()[0]
            
            return row > 0
            
            conn.close()

        except Exception as e:
            return {"message": f"Erreur get_group_of_promotion : {str(e)}"}, 500
        
        
    #------------------ GET COURSES BY TD ------------------
    def get_course_by_td_fonction( id_td):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("TD", 'id', id_td) :
                return {"error": f"l'id' : {id_td} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                        if row[9] :
                            response, status = CoursesFonction.get_group_of_td(row[9])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = [row[9]],id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()

    # ---------------------------- GET COURSES BY TRAINING --------------------------
    def get_course_by_training_fonction(training_id):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("Trainings", 'id', training_id) :
                return {"error": f"l'id : {training_id} n'existe pas"}, 400
            with conn.cursor() as cursor:
                # Supposons que la date soit au format 'YYYY-MM-DD'
                sql_query = '''
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                            
                        if row[11] :
                            response, status = CoursesFonction.get_group_of_training(row[11])
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = response["tp"],id_Td = response["td"],id_Promotion = None,id_Training = [row[11]], teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
            
    # ----------------- GET COURSES BY TP -----------------------
    def get_course_by_tp_fonction( id_tp):
        try:
            conn = connect_pg.connect()
            if not CoursesFonction.field_exist("TP", 'id', id_tp) :
                return {"error": f"l'id' : {id_tp} n'existe pas"}, 400
            with conn.cursor() as cursor:
                sql_query = """
                     SELECT C.id, C.startTime, C.endTime, C.dateCourse, C.control, C.id_Resource, R.name, R.color, C.id_Tp, C.id_Td, C.id_Promotion, C.id_Training
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
                            
                        if row[8] :
                            course_info = CourseModel(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                            id_Tp = [row[8]],id_Td = None,id_Promotion = None,id_Training = None, teacher = teachers, classroom= classrooms)
                        courses_list.append(course_info.jsonify())
                    return {"courses": courses_list}, 200
                else:
                    return {"courses": []}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération du cours : {str(e)}"}, 500
        finally:
            conn.close()