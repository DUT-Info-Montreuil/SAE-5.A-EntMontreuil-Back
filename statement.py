from imports import *

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
    if user :
        user_statement = get_user_statement(user)  
        teacher_statement['user'] = user_statement
    else :
        teacher_statement['user'] = None  # L'utilisateur n'existe pas
    return teacher_statement

