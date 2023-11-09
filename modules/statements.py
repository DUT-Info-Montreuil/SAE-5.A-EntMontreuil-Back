from flask import Blueprint
import connect_pg


statement_bp = Blueprint('statement', __name__)


############  ADMIN STATEMENT ################
def get_admin_statement(row):
    """ Admin array statement """
    admin_statement = {
        'id': row[0]
    }
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ent.users WHERE id = %s", (row[1],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    user_statement = get_user_statement(user)  
    admin_statement['user'] = user_statement
    return admin_statement

