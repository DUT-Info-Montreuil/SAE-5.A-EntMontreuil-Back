import psycopg2
import connect_pg
from flask import jsonify
from entities.model.degreesm import DegreesModel

class DeegreeService:
    def __init__(self):
        pass

    def get_all_degrees(self, output_format="model"):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            if output_format == "model":
                # Si output_format est "model", retournez une liste de DegreeModel
                query = "SELECT id, name FROM ent.Degrees"
                cursor.execute(query)
                rows = cursor.fetchall()
                degrees = [DegreesModel(id=row[0], name=row[1]) for row in rows]
                return jsonify([degree.jsonify() for degree in degrees])
            else:
                # Si output_format est "dto" (ou tout autre format par défaut), retournez une liste de Degree
                query = "SELECT id, name FROM ent.Degrees"
                cursor.execute(query)
                rows = cursor.fetchall()
                degrees = [{"id": row[0], "name": row[1]} for row in rows]
                return jsonify(degrees)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()



    def create_degree(self, degree):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            insert_query = "INSERT INTO ent.Degrees (name) VALUES (%s) RETURNING id"
            cursor.execute(insert_query, (degree.name,))
            degree_id = cursor.fetchone()[0]

            conn.commit()
            return {
                "message": "Formation créée avec succès.",
                "id": degree_id
            }, 200

        except psycopg2.errors.UniqueViolation as unique_err:
            if "degrees_name_unique" in str(unique_err):
                conn.rollback()
                return {
                    "error": "Unique constraint violation",
                    "message": "Une formation avec ce nom existe déjà.",
                }, 409  # HTTP status code 409 Conflict for unique constraint violation
            else:
                conn.rollback()
                return {
                    "error": "Unique constraint violation",
                    "message": str(unique_err)
                }, 409  # HTTP status code 409 Conflict for unique constraint violation
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 401
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()


    # Méthode pour supprimer une formation par son ID
    def delete_degree(self, degree_id):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Vérifiez d'abord si la formation existe
            cursor.execute("SELECT id FROM ent.Degrees WHERE id = %s", (degree_id,))
            if cursor.fetchone() is None:
                raise Exception("La formation spécifiée n'existe pas.")

            # Supprimez la formation
            cursor.execute("DELETE FROM ent.Degrees WHERE id = %s", (degree_id,))
            conn.commit()

            return {"message": "Formation supprimée avec succès."},200

        except Exception as e:
            conn.rollback()
            return {"message": str(e)},401
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    # Méthode pour récupérer une formation par son ID
    def get_degree_by_id(self, degree_id, output_format="model"):
        conn = None
        cursor = None
        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            if output_format == "model":
          
                # Si output_format est "model", retournez une instance de DegreeModel
                cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (degree_id,))
                row = cursor.fetchone()
                if row is None:
                    raise Exception("La formation spécifiée n'existe pas.")
                degree = DegreesModel(id=row[0], name=row[1]) 
                return jsonify(degree.jsonify())
            else:
                # Si output_format est "dto" (ou tout autre format par défaut), retournez un dictionnaire
                cursor.execute("SELECT id, name FROM ent.Degrees WHERE id = %s", (degree_id,))
                row = cursor.fetchone()
                if row is None:
                    raise Exception("La formation spécifiée n'existe pas.")
                degree = {"id": row[0], "name": row[1]}
                return jsonify(degree)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()


    # Méthode pour modifier une formation
    def update_degree(self, degree_id, new_name):
        conn = None
        cursor = None

        try:
            conn = connect_pg.connect()
            cursor = conn.cursor()

            # Mettez à jour le nom de la formation
            cursor.execute("UPDATE ent.Degrees SET name = %s WHERE id = %s", (new_name, degree_id))
            conn.commit()

            return {"message": "Formation mise à jour avec succès."}, 200

        except psycopg2.errors.UniqueViolation as unique_error:
            conn.rollback()
            # Gérez l'erreur de clé unique ici, en retournant un message personnalisé
            error_message = f"Erreur de duplication : Le nom '{new_name}' existe déjà."
            return {"message": error_message}, 409  # Utilisez le code 409 Conflict pour indiquer la duplication

        except Exception as e:
            conn.rollback()
            return {"message": str(e)}

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
"""ENT Montreuil is a Desktop Working Environnement for the students of the IUT of Montreuil
    Copyright (C) 2024  Steven CHING, Emilio CYRIAQUE-SOURISSEAU ALVARO-SEMEDO, Ismail GADA, Yanis HAMANI, Priyank SOLANKI

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""