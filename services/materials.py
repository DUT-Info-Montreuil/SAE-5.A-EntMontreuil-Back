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

#-------------------- Ajouter un équipement--------------------------------------#

    def add_material(self, data):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Materials (equipment) VALUES (%s) RETURNING equipment"
            values = (data["equipment"],)  
            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_equipment = cursor.fetchone()

            return {"message": f"Équipement ajouté avec succès : {inserted_equipment}"}

        except psycopg2.Error as e:
            return {"message": f"Erreur lors de l'ajout de l'équipement : {str(e)}"}

        finally:
            if conn:
                connect_pg.disconnect(conn)

#-------------------- Supprimer un équipement--------------------------------------#

    def delete_material(self, id_material):
        try:
            conn = connect_pg.connect()
            query = "DELETE FROM ent.Materials WHERE id = %s RETURNING id, equipment"
            values = (id_material,)

            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                deleted_row = cursor.fetchone()
                conn.commit()

            if deleted_row:
                deleted_id, deleted_equipment = deleted_row
                return {"message": f"Équipement avec l'ID {deleted_id} ({deleted_equipment}) supprimé avec succès."}, 200
            else:
                return {"message": f"Équipement avec l'ID {id_material} introuvable."}, 404

        except psycopg2.Error as e:
            return {"message": f"Erreur lors de la suppression de l'équipement : {str(e)}"}, 500

        finally:
            if conn:
                connect_pg.disconnect(conn)
