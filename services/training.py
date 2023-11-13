from flask import request, jsonify
import psycopg2
import connect_pg
from entities.DTO.trainings import Training
from entities.model.trainingsm import TrainingModel

class TrainingService:
    def __init__(self):
        pass

#------------------ Récuperer tous les parcours --------------------------------#
    def get_all_trainings(self, output_format="DTO", id_Degree=None):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                sql_query = "SELECT T.id, T.name, T.id_Degree, D.name FROM ent.Trainings T INNER JOIN ent.Degrees D ON T.id_Degree = D.id"
                
                # Si id_Degree est passé en paramètre, ajoute une clause WHERE pour filtrer par ID de diplôme
                if id_Degree is not None:
                    sql_query += " WHERE T.id_Degree = %s"
                    cursor.execute(sql_query, (id_Degree,))
                else:
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
                    else:
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


#---------------------- Ajouter un parcours --------------------------------#
    def add_training(self, training):
        try:
            conn = connect_pg.connect()
            query = "INSERT INTO ent.Trainings (name, id_Degree) VALUES (%s, %s) RETURNING id"
            data = (training.name, training.id_Degree)

            with conn, conn.cursor() as cursor:
                cursor.execute(query, data)
                new_training_id = cursor.fetchone()[0]

            success_message = {
                "message": f"Le parcours '{training.name}' a été ajouté avec succès.",
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

#---------------------- Récuperer un parcours par son id --------------------------------#
    def get_training(self, id_training,output_format="model"):
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM ent.Trainings T INNER JOIN ent.Degrees D ON T.id_Degree = D.id WHERE T.id = %s", (id_training,))
                row = cursor.fetchone()
                if row:
                      if output_format == "DTO":
                            
                            training = Training(
                                id=row[0],
                                name=row[1],
                                id_Degree=row[2]
                            )
                          
                      else :
                             training = TrainingModel(
                                id=row[0],
                                name=row[1],
                                id_Degree=row[2],
                                degree_name=row[3]
                            )
                
                return training.jsonify()

        except Exception as e:
            return None  

        finally:
            connect_pg.disconnect(conn)
#---------------------- Modifier un parcours par son id --------------------------------#
    def update_training(self, training):
        """
        Met à jour un parcours existant dans la base de données par son ID.

        Cette méthode effectue une mise à jour des informations d'un parcours existant dans la base de données.
        Elle utilise une transaction pour garantir la cohérence des données en cas de succès ou d'échec de la mise à jour.

        Args:
            training (Training): Un objet Training DTO contenant les nouvelles informations du parcours.

        Returns:
            dict: Un dictionnaire contenant un message de résultat et un code d'état HTTP (200 en cas de succès).

        Raises:
            Exception: En cas d'erreur lors de la mise à jour du parcours.
        """       
        try:
            conn = connect_pg.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE ent.Trainings SET name = %s, id_Degree = %s WHERE id = %s RETURNING ID",
                    (training.name, training.id_Degree, training.id)
                )
                updated_row = cursor.fetchone()
                if updated_row:
                    conn.commit()  # Valide la transaction si la mise à jour réussit
                    return {"message": f"Le parcours avec l'ID {training.id} a été mis à jour avec succès."},200
                else:
                    return {"message": f"Le parcours avec l'ID {training.id} n'a pas pu être mis à jour."}, 404
        except Exception as e:
            conn.rollback()  # Annule la transaction en cas d'erreur
            return {"message": f"Erreur lors de la mise à jour du parcours : {str(e)}"}, 500
        finally:
            connect_pg.disconnect(conn)



    def delete_training(self, id_training):
        """
            Supprime un parcours existant de la base de données par son ID.

            Args:
                id_training (int): L'identifiant unique du parcours à supprimer.

            Returns:
                dict: Un dictionnaire contenant un message de résultat et un code d'état HTTP.

            Raises:
                Exception: En cas d'erreur lors de la suppression du parcours.

            Example:
                Pour supprimer un parcours avec l'ID 1, envoyez une requête DELETE à l'URL correspondante.
        """
        conn = connect_pg.connect()
        try:
            with conn:
                with conn.cursor() as cursor:

                    cursor.execute(
                        "DELETE FROM ent.Trainings WHERE id = %s RETURNING id", (id_training,))
                    deleted_row = cursor.fetchone()

                    # Si la suppression a réussi, valide la transaction
                    if deleted_row:
                        conn.commit()
                        return {"message": f"Le parcours avec l'ID {id_training} a été supprimé avec succès."}, 200
                    else:
                        # Si la suppression a échoué, annule la transaction
                        conn.rollback()
                        return {"message": f"Le parcours avec l'ID {id_training} n'a pas pu être trouvé."}, 404

        except Exception as e:
            # En cas d'erreur, annule la transaction
            conn.rollback()
            return {"message": f"Erreur lors de la suppression du parcours : {str(e)}"}, 500

        finally:
            connect_pg.disconnect(conn)
