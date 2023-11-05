from flask import Blueprint
import connect_pg


statement_bp = Blueprint('statement', __name__)

############  USER STATEMENT ################
def get_user_statement(row) :
    """ User array statement """
    return {
        'id':row[0],
        'username':row[1],
        'password':row[2],
        'type':row[3],
        'last_name':row[4],
        'first_name':row[5],
        'email':row[6]
    }

############  TEACHER STATEMENT ################
def get_teacher_statement(row):
    """ Teacher array statement """
    teacher_statement = {
        'id': row[0],
        'initial': row[1],
        'desktop': row[2],
        'timetable_manager': row[3],
    }
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ent.users WHERE id = %s", (row[4],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    user_statement = get_user_statement(user)  
    teacher_statement['user'] = user_statement
    return teacher_statement


############  STUDENT STATEMENT ################
def get_student_statement(row):
    """ Student array statement """
    student_statement = {
        'id': row[0],
        'appprentice': row[1],
    }
    conn = connect_pg.connect()
    cursor = conn.cursor()
    #get user
    cursor.execute("SELECT * FROM ent.users WHERE id = %s", (row[2],))
    user = cursor.fetchone()
    user_statement = get_user_statement(user)
    student_statement['user'] = user_statement
    #get td
    if row[4] :
        cursor.execute("SELECT name FROM ent.td WHERE id = %s", (row[4],))
        td = cursor.fetchone()
        student_statement['TD'] = td[0]
    # get tp
    if row[3] :
        cursor.execute("SELECT name FROM ent.tp WHERE id = %s", (row[3],))
        tp = cursor.fetchone()
        student_statement['TP'] = tp[0]
    #get promotion
    if row[5] :
        cursor.execute("SELECT * FROM ent.promotions WHERE id = %s", (row[5],))
        promotion = cursor.fetchone()
        cursor.execute("SELECT name FROM ent.degrees WHERE id = %s", (promotion[2],))
        degree = cursor.fetchone()
        student_statement['Promotion'] = f"{degree[0]} BUT {promotion[1]}"

    cursor.close()
    conn.close()
    return student_statement

