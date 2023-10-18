#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import psycopg2
from contextlib import closing
from config import config
import connect_pg
import hashlib
import re

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/users/get', methods=['GET','POST'])
def get_users():
    """ Return all user in JSON format """
    query = "select * from ent.users order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_user_statement(row))

    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

@app.route('/users/add', methods=['POST'])
def add_users():
    try:
        jsonObject = request.json
        # Assurez-vous que "datas" est présent dans l'objet JSON
        if "datas" not in jsonObject:
            return jsonify({"message": "Missing 'datas' field in JSON"})
        data = jsonObject["datas"]
        password = data.get("password") 
        username = data.get("username")
        if not username:
            return jsonify({"message": "Missing 'username' field in JSON"})
        # Vérifiez si le nom d'utilisateur est déjà utilisé
        if username_exists(username):
            return jsonify({"message": "Username already in use"})

        # Vérifiez le mot de passe
        if len(password) < 12 : # plus de 12 caracteres
            return jsonify({"message": "password need to contains minimum 12 characters"})
        if not re.search(r'[A-Z]', password) : # au moins 1 majuscule
            return jsonify({"message": "Password need to contains minimum 1 capital"})
        if not re.search(r'[a-z]', password) : # au moins une minuscule
            return jsonify({"message": "Password need to contains minimum 1 minuscule"})
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) :  # Au moins un caractère spécial
            return jsonify({"message": "Password need to contains minimum 1 special characters"})
        if not re.search(r'[1-9]', password) : # au moins 1 chiffre
            return jsonify({"message": "Password need to contains minimum 1 number"})


        hashed_password = hashlib.md5(password.encode()).hexdigest()
        # Créez la liste de colonnes et de valeurs
        columns = list(data.keys())
        values = list(data.values())
        values[columns.index("password")] = hashed_password
        # Établissez la connexion à la base de données
        conn = connect_pg.connect()
        cursor = conn.cursor()
        # Créez la requête SQL paramétrée
        query = f"INSERT INTO ent.users ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])}) RETURNING id"
        # Exécutez la requête SQL avec les valeurs
        cursor.execute(query, values)
        # Récupérez l'identifiant de l'utilisateur inséré
        row = cursor.fetchone()
        # Validez la transaction et fermez la connexion
        conn.commit()
        conn.close()
        return jsonify({"message": "User added", "id": row[0]})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)})

def username_exists(username):
    # Fonction pour vérifier si le nom d'utilisateur existe déjà dans la base de données
    conn = connect_pg.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ent.users WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_user_statement(row) :
    """ User array statement """
    return {
        'id':row[0],
        'username':row[1],
        'password':row[2],
        'type':row[3],
        'last_name':row[4],
        'first_name':row[5],
        'email':row[6]
    }



if __name__ == "__main__":
    # read server parameters
    params = config('config.ini', 'server')
    # Launch Flask server
    app.run(debug=params['debug'], host=params['host'], port=params['port'])