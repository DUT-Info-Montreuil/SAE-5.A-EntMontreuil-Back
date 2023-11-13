#!/usr/bin/python
import psycopg2
from config import config

def connect(filename='config.ini', section='postgresql'):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config(filename, section) # read connection parameters
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params) # connect to the PostgreSQL server
        conn.set_client_encoding('UTF8')
        cur = conn.cursor() # create a cursor
        print('PostgreSQL database version:')
        cur.execute('SELECT version()') # execute a statement
        db_version = cur.fetchone() # display the PostgreSQL database server version
        print(db_version)
        cur.close() # close the communication with the PostgreSQL
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn

def disconnect(conn):
    conn.close() # close the connexion
    print('Database connection closed.')

def execute_commands(conn, commands):
    """ Execute a SQL command """
    cur = conn.cursor()
    # create table one by one
    for command in commands:
        if command :
            print(command)
            cur.execute(command)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()


def get_query(conn, query):
    """ query data from db """
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return rows




def does_entry_exist(table_name, entry_id):
    """
    Vérifie si une entrée existe dans la table spécifiée en fonction de son ID.

    :param table_name: Le nom de la table dans laquelle effectuer la vérification.
    :param entry_id: L'identifiant de l'entrée à vérifier.
    :return: True si l'entrée existe, False autrement.
    """
    valid_tables = ['Users', 'Admin', 'Teachers', 'Degrees', 'Trainings', 'Promotions', 'Resources',
                    'TD', 'TP', 'Materials', 'Classroom', 'Courses', 'Students', 'Absences', 'Historique']
    if table_name not in valid_tables:
        raise ValueError(f"Invalid table name: {table_name}")

    conn = None
    try:
        conn = connect()  # Utilisation de la fonction connect du module
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM ent.{} WHERE id = %s)".format(table_name), (entry_id,))
            return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Erreur lors de la vérification de l'existence de l'entrée: {e}")
        return False
    finally:
        if conn:
            disconnect(conn)


if __name__ == '__main__':
    connect()