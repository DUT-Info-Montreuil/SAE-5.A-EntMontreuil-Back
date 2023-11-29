from flask import jsonify, request
import connect_pg
from entities.DTO.roles import Roles

# Route pour créer un nouveau rôle
class RolesServices :
    def create_role(self,data):
        conn = connect_pg.connect()  # Établir une connexion à la base de données
        cursor = conn.cursor()

        # Récupérer les données du rôle depuis la requête JSON
        role_name = data.get('name')

        if RolesFonction.name_exists(role_name) :
            return jsonify({"error": "Role name already exist"}), 400

        # Insérer le nouveau rôle dans la base de données
        cursor.execute("INSERT INTO ent.roles (name) VALUES (%s) RETURNING id", (role_name,))
        role_id = cursor.fetchone()[0]

        conn.commit()  # Valider la transaction
        conn.close()   # Fermer la connexion à la base de données

        return jsonify({"message": "Role created", "role_id": role_id}), 201

    # Route pour mettre à jour un rôle existant
    def update_role(self, role_id, data):
        
        if not RolesFonction.id_exists(role_id) :
            raise ValidationError(f"id role '{role_id}' not exist")
        
        # Récupérer le nouveau nom du rôle depuis la requête JSON
        updated_role_name = data.get('name')        
        if RolesFonction.name_exists(updated_role_name) :
            return jsonify({"error": f"Role name {updated_role_name} already exist"}), 400
        conn = connect_pg.connect()   # Établir une connexion à la base de données
        cursor = conn.cursor()
        # Mettre à jour le nom du rôle dans la base de données
        cursor.execute("UPDATE ent.roles SET name = %s WHERE id = %s", (updated_role_name, role_id))

        conn.commit()  # Valider la transaction
        conn.close()   # Fermer la connexion à la base de données

        return jsonify({"message": "Role updated", "role_id": role_id}), 200

    # Route pour supprimer un rôle existant
    def delete_role(self,role_id):
        conn = connect_pg.connect()   # Établir une connexion à la base de données
        cursor = conn.cursor()
        if not RolesFonction.id_exists(role_id) :
            return jsonify({"error": f"id role '{role_id}' not exist"}), 400
        # Supprimer le rôle de la base de données
        cursor.execute("DELETE FROM ent.roles WHERE id = %s", (role_id,))

        conn.commit()  # Valider la transaction
        conn.close()   # Fermer la connexion à la base de données

        return jsonify({"message": "Role deleted", "role_id": role_id}), 200

    # Route pour obtenir tous les rôles
    def get_roles(self):
        query = "select * from ent.roles order by id"
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        roles = []

        for row in rows:
            role = Roles(id = row[0], name = row[1])
            roles.append(role.jsonify())
        connect_pg.disconnect(conn)
        return jsonify(roles)

    # Route pour obtenir un rôle spécifique par ID
    def get_role_by_id(self,role_id):
        
        if not RolesFonction.id_exists(role_id) :
            raise ValidationError(f"id role '{role_id}' not exist")
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = "select * from ent.roles where id = %s"
        cursor.execute(query, (role_id,))
        row = cursor.fetchone()
        role = Roles(id = row[0], name = row[1])

        conn.commit()
        conn.close()
        return role.jsonify()
    
        # Route pour obtenir tous les rôles
    def get_roles_not_student_teacher(self):
        query = "select * from ent.roles where name not in ('teacher', 'student') order by id "
        conn = connect_pg.connect()
        rows = connect_pg.get_query(conn, query)
        roles = []

        for row in rows:
            role = Roles(id = row[0], name = row[1])
            roles.append(role.jsonify())
        connect_pg.disconnect(conn)
        return jsonify(roles)

#--------------------Role Fonction----------------------------#
class RolesFonction :

    def name_exists( name):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.roles WHERE name = %s"
        cursor.execute(query, (name,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def id_exists( id):
        conn = connect_pg.connect()
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM ent.roles WHERE id = %s"
        cursor.execute(query, (id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
#--------------------ERROR----------------------------------#
class ValidationError(Exception) :
    pass