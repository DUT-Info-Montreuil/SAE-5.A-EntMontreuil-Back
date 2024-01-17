from flask import jsonify, request
import connect_pg
from entities.DTO.settings import Settings

# Route pour créer ou mettre à jour les paramètres utilisateur
class SettingsService:
    
    def update_settings(self, user_id, data):
        conn = connect_pg.connect()  # Établir une connexion à la base de données
        cursor = conn.cursor()

        # Récupérer les données des paramètres depuis la requête JSON
        notification_mail = data.get('notification_mail')
        notification_website = data.get('notification_website')

        # Vérifier si l'utilisateur a déjà des paramètres
        if not self.user_has_settings(user_id):
            # Si l'utilisateur n'a pas encore de paramètres, créez-en un
            cursor.execute("INSERT INTO ent.settings (id_user, notification_mail, notification_website) VALUES (%s, %s, %s) RETURNING id_user",
                           (user_id, notification_mail, notification_website))
        else:
            # Si l'utilisateur a déjà des paramètres, mettez-les à jour
            cursor.execute("UPDATE ent.settings SET notification_mail = %s, notification_website = %s WHERE id_user = %s",
                           (notification_mail, notification_website, user_id))

        conn.commit()  # Valider la transaction
        conn.close()   # Fermer la connexion à la base de données

        status_code = 200 if cursor.rowcount > 0 else 400


        return jsonify({"message": "Paramètres mis à jour avec succès", "user_id": user_id, "status_code": status_code}), 200

    def get_settings(self, user_id):
        conn = connect_pg.connect()  # Établir une connexion à la base de données
        cursor = conn.cursor()

        # Récupérer les paramètres de l'utilisateur
        cursor.execute("SELECT * FROM ent.settings WHERE id_user = %s", (user_id,))
        row = cursor.fetchone()

        # Si l'utilisateur n'a pas de paramètres, renvoyer une erreur
        if not row:
            return jsonify({"error": f"Paramètres introuvables pour l'utilisateur avec l'ID {user_id}"}), 404

        # Créer un objet Settings à partir des données de la base de données
        settings = Settings(id_user=row[0], notification_mail=row[1], notification_website=row[2])

        conn.close()  # Fermer la connexion à la base de données
        return jsonify(settings.jsonify())

# --------------------Fonctions------------------------#

    def user_has_settings(self, user_id):
        conn = connect_pg.connect()  # Établir une connexion à la base de données
        cursor = conn.cursor()

        # Vérifier si l'utilisateur a des paramètres dans la base de données
        cursor.execute("SELECT COUNT(*) FROM ent.settings WHERE id_user = %s", (user_id,))
        count = cursor.fetchone()[0]

        conn.close()  # Fermer la connexion à la base de données
        return count > 0


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