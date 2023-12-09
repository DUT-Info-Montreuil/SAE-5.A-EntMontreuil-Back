from flask import jsonify, Blueprint
import connect_pg
import hashlib
import re
import bcrypt
import random
import string
from entities.DTO.users import Users
from entities.model.usersm import UsersModel
from entities.model.remindersm import ReminderModel
from services.roles import RolesFonction

class UsersServices :

    def __init__ (self):
        pass

    ############ GET /USERS ################
    def get_users(self , output_format):
        """ Return all users in JSON format """
        query = "select u.id, password, username, last_name, first_name , email, r.id,isAdmin, isTTManager, name from ent.users u inner join ent.roles r on u.id_role = r.id  order by u.id "
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        users = []

        for row in rows:
            if output_format == 'dto' :
                user = Users(id = row[0], password=row[1] ,username = row[2], last_name = row[3], first_name=row[4], email=row[5] , id_Role=row[6] , isAdmin=row[7], isTTManager=row[8])
            elif output_format == 'model' :
                user = UsersModel(id = row[0], password=row[1], username = row[2], last_name = row[3], first_name=row[4], email=row[5] , id_Role=row[6] , isAdmin=row[7],isTTManager=row[8] ,role_name=row[9])
            else :
                raise ValueError("Invalid output_format. Should be 'dto' or 'model'.")
            users.append(user.jsonify())
        connect_pg.disconnect(conn)
        return jsonify(users)
    


    ############ GET /USERS/<int:id_user> ################
    def get_users_with_id(self, id_user, output_format):
        """ Return one user in JSON format """

        if not UsersFonction.field_exists('id' , id_user) :
            raise ValidationError(f"id_user : '{id_user}' not exists")
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select u.id, password, username, last_name, first_name , email, r.id,isAdmin, isTTManager, name from ent.users u inner join ent.roles r on u.id_role = r.id where u.id = %s"
        cursor.execute(query, (id_user,))
        row = cursor.fetchone()
        if output_format == 'dto' :
            user = Users(id = row[0], password=row[1] ,username = row[2], last_name = row[3], first_name=row[4], email=row[5] , id_Role=row[6] , isAdmin=row[7], isTTManager=row[8])
        elif output_format == 'model' :
            user = UsersModel(id = row[0], password=row[1], username = row[2], last_name = row[3], first_name=row[4], email=row[5] , id_Role=row[6] , isAdmin=row[7],isTTManager=row[8] ,role_name=row[9])
        else :
            raise ValueError("Invalid output_format. Should be 'dto' or 'model'.")
        conn.commit()
        conn.close()
        return user.jsonify()
    
    
    ############ ADD/USER ################
    def add_user(self, data):
        """ Add one user"""
        try:
            if not RolesFonction.name_exists(data["role"]) :
                return jsonify({"error": f"Le rôle '{data.get('role')}' n'existe pas, veuillez choisir un rôle présenté dans le menu déroulant."}), 400
            if data['role'] == 'enseignant' or data['role'] == 'étudiant' :
                return jsonify({"error": f"Vous ne prouvez pas ajouté d'étudiant ou d'enseignant via ce formulaire. Pour ajouter un étudiant ou un enseignant veuillez aller dans l'onglet ADMINISTRATEUR et sélectionner l'entité que vous voulez ajouter."}), 400
            return UsersFonction.add_users(data) 
        except Exception as e:
            return jsonify({"message": "ERROR", "error": str(e)}) , 400

        

 #--------------------------------------------------FONCTION--------------------------------------------------#
class UsersFonction :
   
    ############  USER UPDATE ################
    def update_users(user_data, id_user):
        try:
            # Si le password est present
            if "password" in user_data :
                password = user_data["password"]
                # Verification du password
                user_response, http_status = UsersFonction.is_valid_password(password)  
                if http_status != 200 :
                    return user_response, http_status 
                else :
                    # Hashage + salage du password 
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')  
                    user_data["password"] = hashed_password
            # Si id est présent 
            if "id" in user_data :
                return jsonify({"error": "Unable to modify user id, remove id field"}) , 400                
            # Si username est présent
            if "username" in user_data :
                username = user_data["username"]
                # Verification username existe deja,
                oldUsername = user_data["oldUsername"]
                del user_data["oldUsername"]  
                if UsersFonction.username_exist( username, oldUsername):
                    return jsonify({"error": f"Le pseudo '{username}' est déjà utilisé"}), 400
                # Verification username plus de 4 caracteres
                if len(username) < 4:
                    return jsonify({"error": "Le pseudo doit contenir minimums 4 caractères."}), 400
            # Si email est present
            if "email" in user_data :
                email = user_data["email"]
                # Verification email
                if not UsersFonction.is_valid_email(email):
                    return jsonify({"error": f"Le format de cet email '{user_data.get('email')}' est invalid, (test@test.com)."}), 400
            if "role" in user_data :
                if not RolesFonction.name_exists(user_data["role"]) :
                    return jsonify({"error": f"Le rôle '{user_data.get('role')}' n'existe pas, veuillez choisir un rôle présenté dans le menu déroulant."}), 400
                if user_data['role'] == 'student' or user_data['role'] == 'teacher' :
                    return jsonify({"error": f"Vous ne prouvez pas ajouté d'étudiant ou d'enseignant via ce formulaire. Pour ajouter un étudiant ou un enseignant veuillez aller dans l'onglet ADMINISTRATEUR et sélectionner l'entité que vous voulez ajouter."}), 400
                id_role = UsersFonction.get_role_id_by_name(user_data["role"])
                del user_data["role"]  # Supprimez le champ du nom du rôle
                user_data["id_Role"] = id_role

            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            update_clause = ", ".join([f"{key} = %s" for key in user_data.keys()])
            values = list(user_data.values())
            values.append(id_user)  # Ajoutez l'ID de l'enseignant à la fin pour identifier l'enregistrement a mettre a jour
            query = f"UPDATE ent.users SET {update_clause} WHERE id = %s"
            cursor.execute(query, values)
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
            return jsonify({"message": "User update", "id": id_user}) , 200 
        except Exception as e:
            return jsonify({"message": "ERROR", "error": str(e)}) , 400

    ############  USERS REMOVE ################
    def remove_users(id_user):
        try:
            # Verification si id_user existe bien
            if not UsersFonction.field_exists('id' , id_user) :
                return jsonify({"error": f"User '{id_user}' not exist"}) , 400
            conn = connect_pg.connect()
            cursor = conn.cursor()
            query = "DELETE FROM ent.users WHERE id = %s"
            cursor.execute(query, (id_user,))
            conn.commit()
            conn.close()
            return jsonify({"message": "User deleted", "id": id_user}) , 200 
        except Exception as e:
            return jsonify({"message": "ERROR", "error": str(e)}) , 400

    ############  USERS ADD ################
    def add_users(data):
        try:
            # Si le password est mentionner 
            if "password" in data and data["password"] :
                # Verifiez le mot de passe
                user_response, http_status = UsersFonction.is_valid_password(data["password"]) 
                if http_status != 200 :
                    return user_response, http_status 
            # Si le password n'est pas mentionner il est generer aleatoirement
            else :   
                data["password"] = UsersFonction.generate_password()
            password = data["password"]
            # isAdmin false par defaut
            if "isAdmin" not in data :
                data["isAdmin"] = False
            if "isTTManager" not in data :
                data["isTTManager"] = False
             
            id_role = UsersFonction.get_role_id_by_name(data["role"])
            del data["role"]  # Supprimez le champ du nom du rôle
            data["id_Role"] = id_role

            # Verification si id est deja utiliser
            if "id" in data :
                if UsersFonction.field_exists('id' , data["id"]) :
                    return jsonify({"error": f"Id for user '{data.get('id')}' already exist"}), 400
            # Verifiez username taille > 4
            if len(data["username"]) < 4:
                return jsonify({"error": "Le pseudo doit contenir minimums 4 caractères."}), 400
            # Verifiez si le nom d'utilisateur est deja utilise
            if UsersFonction.field_exists('username', data["username"]):
                return jsonify({"error": f"Le pseudo '{data.get('username')}' est déjà utilisé, veuillez en entrer un nouveau."}), 400
            # Verification de la syntaxe de l'email
            if not UsersFonction.is_valid_email(data["email"]):
                return jsonify({"error": f"Le format de cet email '{data.get('email')}' est invalid, (test@test.com)."}), 400
            # Hashage du password avec md5 + salt password with bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')  
            # Creez la liste de colonnes et de valeurs
            columns = list(data.keys())
            values = list(data.values())
            values[columns.index("password")] = hashed_password
            # Etablissez la connexion a la base de donnees
            conn = connect_pg.connect()
            cursor = conn.cursor()
            # Créez la requête SQL parametree
            query = f"INSERT INTO ent.users ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
            # Executez la requête SQL avec les valeurs
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Validez la transaction et fermez la connexion
            conn.commit()
            conn.close()
            return jsonify({"message": "User added", "id": row[0] , "username" : data["username"] , "password" : password}) , 200 
        except Exception as e:
            return jsonify({"message": "ERROR", "error": str(e)}) , 400

    ############  VERIFICATION FIELD EXIST ################
    # Fonction pour verifier un champ existe deja dans la base de donnees
    def field_exists( field,data):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.users WHERE {field} = %s"
        cursor.execute(query, (data,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    ############  VERIFICATION USERNAME EXIST ################
    # Fonction pour verifier un champ existe deja dans la base de donnees
    def username_exist( username, oldUsername):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.users WHERE username = '{username}' AND username != '{oldUsername}'"
        cursor.execute(query,)
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    

    ############  VERIFICATION EMAIL SYNTAXE ################
    def is_valid_email(email):
        # Utilisez une expression reguliere pour verifier la syntaxe de l'e-mail
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

    ############  VERIFICATION PASSWORD ################
    def is_valid_password(password):
        if len(password) < 12 : # plus de 12 caracteres
            return jsonify({"error": "Le mot de passe doit contenir au minimum 12 caractères"}), 400
        if not re.search(r'[A-Z]', password) : # au moins 1 majuscule
            return jsonify({"error": "Le mot de passe doit contenir au minimum 1 capitale"}), 400
        if not re.search(r'[a-z]', password) : # au moins une minuscule
            return jsonify({"error": "Le mot de passe doit contenir au minimum 1 minuscule"}), 400
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) :  # Au moins un caractere special
            return jsonify({"error": "Le mot de passe doit contenir au minimum 1 caractère special (! - @ - # - $ - % - ^ - & - *, ...)"}) , 400
        if not re.search(r'[1-9]', password) : # au moins 1 chiffre
            return jsonify({"error": "Le mot de passe doit contenir au minimum 1 chiffre"}) , 400
        return True , 200

    ############  GENERATE PASSWORD ################
    def generate_password():
        # Generate a password with at least one uppercase letter, one special character, two digits, and the rest lowercase letters
        length = 12
        uppercase_letter = random.choice(string.ascii_uppercase)
        special_character = random.choice(string.punctuation)
        digits = ''.join(random.choices(string.digits, k=2))
        lowercase_letters = ''.join(random.choices(string.ascii_lowercase, k=length-4))

        # Shuffle the characters to create the final password
        password_list = list(uppercase_letter + special_character + digits + lowercase_letters)
        random.shuffle(password_list)
        password = ''.join(password_list)
        return password


    def get_all_role_name():
        conn =connect_pg.connect()  # Établir une connexion à la base de données
        cursor = conn.cursor()
        query = "SELECT name FROM ent.roles WHERE name NOT IN ('teacher', 'student')"
        cursor.execute(query)
        role_names = [row[0] for row in cursor.fetchall()]  # Récupérer tous les noms de rôles
        conn.close()  # Fermer la connexion à la base de données
        return ", ".join(role_names)  # Retourner les noms de rôles sous forme d'une chaîne de caractères séparés par des virgules
    
    def get_role_id_by_name(role_name):
            conn = connect_pg.connect()# Établir une connexion à la base de données
            cursor = conn.cursor()

            # Exécutez une requête pour obtenir l'ID du rôle en fonction de son nom
            cursor.execute("SELECT id FROM ent.roles WHERE name = %s", (role_name,))
            role_id = cursor.fetchone()

            conn.close()  # Fermer la connexion à la base de données

            return role_id[0]  # Renvoie l'ID du rôle s'il existe

    def get_all_reminders(self, output_format='DTO'):
        query = """
            SELECT R.id, R.id_User, U.username, R.title, R.reminder_text, R.reminder_date
            FROM ent.reminders R
            INNER JOIN ent.users U ON R.id_User = U.id
            ORDER BY R.id DESC
        """
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        reminders = []

        for row in rows:
            reminder = ReminderModel(
                id=row[0],
                id_User=row[1],
                user_username=row[2],
                title=row[3],
                reminder_text=row[4],
                reminder_date=row[5],
            )
            reminders.append(reminder.jsonify())

        connect_pg.disconnect(conn)
        return reminders

    def get_reminder_by_id(reminder_id, output_format='DTO'):
        if not UsersFonction.field_exists('id', reminder_id):
            raise ValidationError(f"Reminder id: '{reminder_id}' not exists")

        query = """
            SELECT R.id, R.id_User, U.username, R.title, R.reminder_text, R.reminder_date
            FROM ent.reminders R
            INNER JOIN ent.users U ON R.id_User = U.id
            WHERE R.id = %s
        """
        conn = connect_pg.connect()
        cursor = conn.cursor()
        cursor.execute(query, (reminder_id,))
        row = cursor.fetchone()

        if not row:
            raise ValidationError(f"Reminder id: '{reminder_id}' not found")

        reminder = ReminderModel(
            id=row[0],
            id_User=row[1],
            user_username=row[2],
            title=row[3],
            reminder_text=row[4],
            reminder_date=row[5],
        )

        conn.commit()
        conn.close()
        return reminder.jsonify()

    def add_reminder(data):
        try:
            query = """
                INSERT INTO ent.reminders (id_User, title, reminder_text, reminder_date)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            values = (
                data["id_User"],
                data["title"],
                data["reminder_text"],
                data["reminder_date"],
            )

            conn = connect_pg.connect()
            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                inserted_reminder_id = cursor.fetchone()[0]

            return jsonify({
                "message": f"Reminder added successfully, ID: {inserted_reminder_id}",
                "id": inserted_reminder_id
            }), 200

        except Exception as e:
            return jsonify({"message": f"Error adding reminder: {str(e)}"}), 500
        finally:
            if conn:
                connect_pg.disconnect(conn)

    def update_reminder(data, reminder_id):
        try:
            query = """
                UPDATE ent.reminders
                SET id_User = %s, title=%s, reminder_text = %s, reminder_date = %s
                WHERE id = %s
                RETURNING id
            """
            values = (
                data["id_User"],
                data["title"],
                data["reminder_text"],
                data["reminder_date"],
                reminder_id,
            )

            conn = connect_pg.connect()
            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                updated_reminder_id = cursor.fetchone()

            conn.commit()

            if updated_reminder_id:
                return jsonify({
                    "message": f"Reminder updated successfully, ID: {updated_reminder_id[0]}"
                }), 200
            else:
                return jsonify({"message": "Reminder not found or no changes made"}), 404

        except Exception as e:
            return jsonify({"message": f"Error updating reminder: {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)

    def delete_reminder(reminder_id):
        try:

            query = "DELETE FROM ent.reminders WHERE id = %s RETURNING id"
            values = (reminder_id,)
            conn = connect_pg.connect()
            with conn, conn.cursor() as cursor:
                cursor.execute(query, values)
                deleted_reminder_id = cursor.fetchone()
            conn.commit()
            if deleted_reminder_id:
                return jsonify({
                    "message": f"Reminder deleted successfully, ID: {deleted_reminder_id[0]}"
                }), 200
            else:
                return jsonify({"message": "Reminder not found or already deleted"}), 404

        except Exception as e:
            return jsonify({"message": f"Error deleting reminder: {str(e)}"}), 500

        finally:
            if conn:
                connect_pg.disconnect(conn)
    

#----------------------------------ERROR-------------------------------------
class ValidationError(Exception) :
    pass