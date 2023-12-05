import json
import psycopg2
import connect_pg
from entities.DTO.classroom import Classroom
from entities.model.classroomm import ClassroomModel
from flask import jsonify

class ClassroomService:
    def __init__(self):
        pass
#------------------------------- récuperer toute les salles de classe -------------------#
    def get_all_classrooms(self, output_format="model",id_classroom=None,):
        conn = None
        cursor = None  # Initialisez cursor en dehors du bloc try
        
        try:
            conn = connect_pg.connect()  # Remplacez cela par votre fonction de connexion réelle
            cursor = conn.cursor()

            if output_format == "model":
                # Si output_format est "model", retourne une liste de ClassroomModel
                query="""
                    SELECT c.id, c.name, c.capacity, m.id AS material_id, m.equipment, cm.quantity
                    FROM ent.Classroom c
                    LEFT JOIN ent.CONTAINS cm ON c.id = cm.id_classroom
                    LEFT JOIN ent.Materials m ON cm.id_materials = m.id
                """
                
                if id_classroom is not None:
                        query += "WHERE c.id=%s"
                        cursor.execute(query,(id_classroom,))
                else :
                        cursor.execute(query)
                rows = cursor.fetchall()
                
                classroom_models = {}
                for row in rows:
                    classroom_id = row[0]
                    if classroom_id not in classroom_models:
                        classroom_model = ClassroomModel(
                            id=row[0],
                            name=row[1],
                            capacity=row[2],
                            materials=[]
                        )
                        classroom_models[classroom_id] = classroom_model

                    if row[3] is not None:
                        material = {
                            "id": row[3],
                            "equipment": row[4],
                            "quantity": row[5]
                        }
                        classroom_models[classroom_id].materials.append(material)

                result = [classroom_model.jsonify() for classroom_model in classroom_models.values()]
                return jsonify(result)
            else:
                
                # Si output_format est "dto" (ou tout autre format par défaut), retourne une liste de Classroom
                query ="SELECT * FROM ent.Classroom "
                
                if id_classroom is not None:
                        query += "WHERE Classroom.id=%s"
                        cursor.execute(query,(id_classroom,))
                else :
                        cursor.execute(query)
                rows = cursor.fetchall()
                classrooms = []
                for row in rows:
                    classroom = Classroom(
                        id=row[0],
                        name=row[1],
                        capacity=row[2]
                    )
                    classrooms.append(classroom.jsonify())

                return jsonify(classrooms)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

#------------------------------- chercher  une salle de classe en focntion de critère -------------------#
    def search_classrooms(self, name=None, capacity=None, id_material=None, min_quantity=None, output_format="model"):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Build the base query
            query = "SELECT c.id, c.name, c.capacity, m.id AS material_id, m.equipment, cm.quantity FROM ent.Classroom c"
            query += " LEFT JOIN ent.CONTAINS cm ON c.id = cm.id_classroom"
            query += " LEFT JOIN ent.Materials m ON cm.id_materials = m.id"

            conditions = []
            values = []

            # Helper function to add conditions
            def add_condition(condition_sql, value):
                if conditions:
                    conditions.append(f"AND {condition_sql}")
                else:
                    conditions.append(f"WHERE {condition_sql}")
                values.append(value)

            if name:
                add_condition("c.name = %s", name)
            if capacity is not None:
                add_condition("c.capacity >= %s", capacity)
            if id_material is not None:
                add_condition("m.id = %s", id_material)
            if min_quantity is not None:
                # Utilize a subquery to filter materials based on the minimum quantity
                subquery = "(SELECT id_classroom FROM ent.CONTAINS WHERE id_materials = m.id AND quantity >= %s)"
                add_condition(f"c.id IN {subquery}", min_quantity)

            if conditions:
                query += " " + " ".join(conditions)

            cursor.execute(query, tuple(values))
            rows = cursor.fetchall()

            classroom_models = {}
            for row in rows:
                classroom_id = row[0]
                if classroom_id not in classroom_models:
                    classroom_model = ClassroomModel(
                        id=row[0],
                        name=row[1],
                        capacity=row[2],
                        materials=[]
                    )
                    classroom_models[classroom_id] = classroom_model

                if row[3] is not None:
                    material = {
                        "id": row[3],
                        "equipment": row[4],
                        "quantity": row[5]
                    }
                    classroom_models[classroom_id].materials.append(material)

            result = [classroom_model.jsonify() for classroom_model in classroom_models.values()]
            return jsonify(result) if output_format == "model" else jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()


##------------------------------- ajouter un equipement dans une salle -----------------------#
    def add_equipments_to_classroom(self, id_Classroom, equipment_ids):
            try:
                conn = connect_pg.connect()  # Remplacez par votre fonction de connexion réelle
                cursor = conn.cursor()

                if not connect_pg.does_entry_exist("Classroom", id_Classroom):
                    raise Exception("La salle de classe spécifiée n'existe pas.")
                
                if not equipment_ids:
                    raise Exception("Aucun équipement spécifié à ajouter.")
                    
                # Vérifiez si les équipements existent et récupérez leurs IDs
                cursor.execute("SELECT id FROM ent.Materials WHERE id IN %s", (tuple(equipment_ids),))
                existing_equipment_ids = [row[0] for row in cursor.fetchall()]

                if len(existing_equipment_ids) != len(equipment_ids):
                    raise Exception("Certains équipements spécifiés n'existent pas.")

                # Ajoutez les équipements à la salle de classe en utilisant les IDs
                cursor.executemany("INSERT INTO ent.CONTAINS (id_classroom, id_materials, quantity) VALUES (%s, %s, %s)  ON CONFLICT (id_materials, id_classroom) DO NOTHING",
                                    [(id_Classroom, equip_id, 1) for equip_id in existing_equipment_ids])

                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()


#----------------- modifer la quantité d'un equipement dans une salle  ----------------------#

    def update_equipment_quantity(self, id_classroom, id_equipment, new_quantity):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()  # Utilisez votre fonction de connexion
            cursor = conn.cursor()

            # Vérifiez si la salle de classe spécifiée existe
            if not connect_pg.does_entry_exist("Classroom", id_classroom):
                raise Exception("La salle de classe spécifiée n'existe pas.")

            # Vérifiez si l'équipement spécifié existe dans la salle
            cursor.execute("SELECT * FROM ent.CONTAINS WHERE id_classroom = %s AND id_materials = %s", (id_classroom, id_equipment))
            if cursor.fetchone() is None:
                raise Exception("L'équipement spécifié n'existe pas dans la salle de classe.")

            # Mettez à jour la quantité de l'équipement
            cursor.execute("UPDATE ent.CONTAINS SET quantity = %s WHERE id_classroom = %s AND id_materials = %s", (new_quantity, id_classroom, id_equipment))

            conn.commit()
            return jsonify({"message": "Quantité mise à jour avec succès"}), 200

        except Exception as e:
            if conn:
                conn.rollback()
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                    conn.close()
    #----------- enlever un equipement d'une classe  ---------------#
    def remove_equipment_from_classroom(self, id_classroom, id_equipment):
            try:
                conn = connect_pg.connect()
                cursor = conn.cursor()

                # Vérifiez si la salle de classe et l'équipement existent
                if not connect_pg.does_entry_exist("Classroom", id_classroom):
                    raise Exception("La salle de classe spécifiée n'existe pas.")

                if not connect_pg.does_entry_exist("Materials", id_equipment):
                    raise Exception("L'équipement spécifié n'existe pas.")

                # Supprimez l'équipement de la salle de classe
                cursor.execute("DELETE FROM ent.CONTAINS WHERE id_classroom = %s AND id_materials = %s", (id_classroom, id_equipment))
                conn.commit()

                return {"message": "Équipement supprimé avec succès."}
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

#--------------------- supprimer une classe --------------------#
    def delete_classroom(self, id_classroom):
            conn = None
            cursor = None
            try:
                conn = connect_pg.connect()
                cursor = conn.cursor()

                # Supprimez d'abord les tuples associés dans les tables liées
                delete_related_query = "DELETE FROM ent.CONTAINS WHERE id_classroom = %s"
                cursor.execute(delete_related_query, (id_classroom,))

                # Ensuite, supprimez la salle de classe
                delete_classroom_query = "DELETE FROM ent.Classroom WHERE id = %s"
                cursor.execute(delete_classroom_query, (id_classroom,))

                conn.commit()
                return {
                    "message": "Salle de classe et données associées supprimées avec succès."
                }

            except Exception as e:
                conn.rollback()
                return {"error": str(e)}
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()


    def create_classroom(self,classroom):
            conn = None
            cursor = None
            try:
                conn = connect_pg.connect()
                cursor = conn.cursor()

                insert_query = "INSERT INTO ent.Classroom (name, capacity) VALUES (%s, %s) RETURNING id"
                cursor.execute(insert_query, (classroom.name, classroom.capacity))
                classroom_id = cursor.fetchone()[0]

                conn.commit()
                return {
                    "message": "Salle de classe créée avec succès.",
                    "id": classroom_id
                }
            except psycopg2.errors.UniqueViolation as e:
                if conn:
                    conn.rollback()  # Annulez la transaction en cours pour éviter un état incohérent
                return {"message": "Une salle de classe avec ce nom existe déjà."}, 409

            except Exception as e:
                conn.rollback()
                return {"error": str(e)}
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    # Dans la classe ClassroomService
    def update_classroom(self, id_classroom, new_name=None, new_capacity=None):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()  # Utilisez votre fonction de connexion
            cursor = conn.cursor()

            # Vérifiez si la salle de classe spécifiée existe
            if not connect_pg.does_entry_exist("Classroom", id_classroom):
                raise Exception("La salle de classe spécifiée n'existe pas.")

            # Mettez à jour le nom et/ou la capacité de la salle de classe
            update_query = "UPDATE ent.Classroom SET"
            update_fields = []

            if new_name is not None:
                update_fields.append(f" name = %s")
            if new_capacity is not None:
                update_fields.append(f" capacity = %s")

            update_query += ", ".join(update_fields)
            update_query += " WHERE id = %s"

            if new_name is not None and new_capacity is not None:
                cursor.execute(update_query, (new_name, new_capacity, id_classroom))
            elif new_name is not None:
                cursor.execute(update_query, (new_name, id_classroom))
            elif new_capacity is not None:
                cursor.execute(update_query, (new_capacity, id_classroom))

            conn.commit()

            return {"message": "Salle de classe mise à jour avec succès."}, 200

        except psycopg2.errors.UniqueViolation as e:  # Gestion spécifique de l'erreur de violation de contrainte unique
            if conn:
                conn.rollback()
            return {"message": "Une salle de classe avec ce nom existe déjà."}, 409  # Code 409 pour Conflit

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}, 500  # Code 500 pour Erreur Interne du Serveur

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

