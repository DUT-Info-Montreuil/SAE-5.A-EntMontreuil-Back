from flask import jsonify, Blueprint
import connect_pg
import hashlib
import re
import bcrypt
import random
import string
from entities.model.usersm import UsersModel

class UsersServices :

    def __init__ (self):
        pass

    ############ GET /USERS ################
    def get_users(self):
        """ Return all users in JSON format """
        query = "select * from ent.users order by id asc"
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        users = []

        for row in rows:
            user = UsersModel(id = row[0], username = row[1], type = row[3], last_name = row[4], first_name=row[5], email=row[6])
            users.append(user)
        connect_pg.disconnect(conn)
        return users

    ############ GET /USERS/<int:id_user> ################
    def get_users_with_id(self, id_user):
        """ Return one user in JSON format """

        if not UsersFonction.field_exists('id' , id_user) :
            raise ValidationError(f"id_user : '{id_user}' not exists")
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select * from ent.users where id = %s"
        cursor.execute(query, (id_user,))
        row = cursor.fetchone()
        user = UsersModel(id = row[0], username = row[1], type = row[3], last_name = row[4], first_name=row[5], email=row[6])
        conn.commit()
        conn.close()
        return user.jsonify()

        

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
                # Verification username existe deja
                if UsersFonction.field_exists('username' , username):
                    return jsonify({"error": f"Username '{username}' already exists"}), 400
                # Verification username plus de 4 caracteres
                if len(username) < 4:
                    return jsonify({"error": "Username need to have minimum 4 characters"}), 400
            # Si email est present
            if "email" in user_data :
                email = user_data["email"]
                # Verification email
                if not UsersFonction.is_valid_email(email):
                    return jsonify({"error": "Invalid email format"}), 400
            # Si type est present
            if "type" in user_data :
                # Si type est bien = student ou admin ou teacher ou timetable_manager
                valid_type = ['student' , 'admin' , 'teacher' , 'timetable_manager']
                if user_data["type"] not in valid_type :
                    return jsonify({"error": f"Invalid type : {user_data.get('type')}, the 4 types available are [student - admin - teacher - timetable_manager]"}), 400
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
                password = data["password"]
                # Verifiez le mot de passe
                user_response, http_status = UsersFonction.is_valid_password(password) 
                if http_status != 200 :
                    return user_response, http_status 
            # Si le password n'est pas mentionner il est generer aleatoirement
            else :   
                data["password"] = UsersFonction.generate_password()
            password = data["password"]
            
            # Verifie si tous les attributs sont presents
            required_fields = ['username' , 'first_name' , 'last_name' , 'email' , 'type']
            for field in required_fields : 
                if field not in data :
                    return jsonify({"error": f"Missing '{field}' field in JSON"}), 400
            # Attribution des valeurs
            username = data["username"]
            email = data["email"] 
            first_name = data["first_name"] 
            last_name = data["last_name"]
            # Verification si id est deja utiliser
            if "id" in data :
                if UsersFonction.field_exists('id' , data["id"]) :
                    return jsonify({"error": f"Id for user '{data.get('id')}' already exist"}), 400
            # Verifiez username taille > 4
            if len(username) < 4:
                return jsonify({"error": "Username need to have minimum 4 characters"}), 400
            # Verifiez si le nom d'utilisateur est deja utilise
            if UsersFonction.field_exists('username', username):
                return jsonify({"error": f"Username '{username}' already exists"}), 400
            # Verification de la syntaxe de l'email
            if not UsersFonction.is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400
            # Verification si le type est bien un type existant (student - admin - teacher - timetable_manager)
            valid_type = ['student' , 'admin' , 'teacher' , 'timetable_manager']
            if data["type"] not in valid_type :
                    return jsonify({"error": f"Invalid type : {data.get('type')}, the 4 types available are [student - admin - teacher - timetable_manager]"}), 400
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
            return jsonify({"message": "User added", "id": row[0] , "username" : username , "password" : password}) , 200 
        except Exception as e:
            return jsonify({"message": "ERROR", "error": str(e)}) , 400

    ############  VERIFICATION FIELD EXIST ################
        # Fonction pour verifier un champ existe deja dans la base de donnees
    def field_exists(self, field,data):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.users WHERE {field} = %s"
        cursor.execute(query, (data,))
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
            return jsonify({"error": "password need to contains minimum 12 characters"}), 400
        if not re.search(r'[A-Z]', password) : # au moins 1 majuscule
            return jsonify({"error": "Password need to contains minimum 1 capital"}), 400
        if not re.search(r'[a-z]', password) : # au moins une minuscule
            return jsonify({"error": "Password need to contains minimum 1 minuscule"}), 400
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) :  # Au moins un caractere special
            return jsonify({"error": "Password need to contains minimum 1 special characters"}) , 400
        if not re.search(r'[1-9]', password) : # au moins 1 chiffre
            return jsonify({"error": "Password need to contains minimum 1 number"}) , 400
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
    

#----------------------------------ERROR-------------------------------------
class ValidationError(Exception) :
    pass