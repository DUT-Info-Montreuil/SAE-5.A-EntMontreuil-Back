import psycopg2
import connect_pg
from entities.DTO.materials import   Material

class MaterialService:
    def __init__(self):
        pass

#-------------------- Récuperer toutes les absences --------------------------------------#
    def get_all_materials(self):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = "SELECT * FROM ent.Materials "
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                material_list = []

                for row in rows:
                        material = Material(
                            id=row[0],
                            equipment=row[1]
                        )
 
                        material_list.append(material.jsonify())

                return material_list
        except Exception as e:
            raise e
        finally:
            conn.close()

