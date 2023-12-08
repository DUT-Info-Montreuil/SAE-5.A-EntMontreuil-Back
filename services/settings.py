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

        return jsonify({"message": "Paramètres mis à jour avec succès", "user_id": user_id}), 200

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


