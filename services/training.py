from flask import request, jsonify
import psycopg2
import connect_pg
from entities.DTO.trainings import Training
from entities.model.trainingsm import TrainingModel

class TrainingService:
    def __init__(self):
        pass

#------------------ Récuperer tous les parcours --------------------------------#
    def get_all_trainings(self, output_format="DTO"):
            try:
                conn = connect_pg.connect()
                with conn.cursor() as cursor:
                    sql_query = "SELECT T.id, T.name, T.id_Degree, D.name FROM ent.Trainings T INNER JOIN ent.Degrees D ON T.id_Degree = D.id"
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    trainings_list = []

                    for row in rows:
                        if output_format == "DTO":
                            training = Training(
                                id=row[0],
                                name=row[1],
                                id_Degree=row[2]
                            )
                            trainings_list.append(training.jsonify())
                        else :
                            training = TrainingModel(
                                id=row[0],
                                name=row[1],
                                id_Degree=row[2],
                                degree_name=row[3]
                            )
                            trainings_list.append(training.jsonify())

                    return trainings_list
            except Exception as e:
                raise e
            finally:
                conn.close()

#------------------ Ajouter un parcours --------------------------------#
    def add_training(self, training_data):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Trainings (name, id_Degree) VALUES (%s, %s) RETURNING id"
            data = (training_data["name"], training_data["id_Degree"])

            with conn, conn.cursor() as cursor:
                cursor.execute(query, data)
                new_training_id = cursor.fetchone()[0]

            success_message = {
                "message": f"Le parcours '{training_data['name']}' a été ajouté avec succès.",
                "id": new_training_id
            }
            return success_message

        except psycopg2.IntegrityError as e:
            if 'trainings_id_degree_name_key' in str(e):
                return {"message": "Un parcours avec le même nom existe déjà pour ce diplôme."}

        except Exception as e:
            return {"message": f"Erreur lors de l'ajout du parcours : {str(e)}"}

        finally:
            connect_pg.disconnect(conn)


    def get_training(self, id_training):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ent.Trainings WHERE id = %s", (id_training,))
                row = cursor.fetchone()
                if row:
                    parcours = {
                        "id": row[0],
                        "name": row[1],
                        "id_Degree": row[2]
                    }
                    return parcours

        except Exception as e:
            return None  

        finally:
            connect_pg.disconnect(conn)

    def update_training(self, id_training, training_data):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.Trainings SET name = %s, id_Degree = %s WHERE id = %s RETURNING id",
                    (training_data["name"], training_data["id_Degree"], id_training)
                )
                updated_row = cursor.fetchone()
                if updated_row:
                    return updated_row[0]

        except Exception as e:
            return None  # Indicates an error during update

        finally:
            connect_pg.disconnect(conn)

    def delete_training(self, id_training):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ent.Trainings WHERE id = %s RETURNING id", (id_training,))
                deleted_row = cursor.fetchone()

            if deleted_row:
                return True
            else:
                return False

        except Exception as e:
            return False  # Indicates an error during deletion

        finally:
            connect_pg.disconnect(conn)
