#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import psycopg2
import requests
from contextlib import closing
from config import config
import connect_pg

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/books/get', methods=['GET','POST'])
def get_books():
    """ Return all books in JSON format """
    query = "select * from books order by id asc"
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = []
    for row in rows:
        returnStatement.append(get_book_statement(row))
    
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

@app.route('/books/get/<bookId>', methods=['GET','POST'])
def get_one_book(bookId):
    """ Return book bookId in JSON format """
    query = "select * from books where id=%(bookId)s order by id asc" % {'bookId':bookId}
    conn = connect_pg.connect()
    rows = connect_pg.get_query(conn, query)
    returnStatement = {}
    if len(rows) > 0:
        returnStatement = get_book_statement(rows[0])
    connect_pg.disconnect(conn)
    return jsonify(returnStatement)

def get_book_statement(row) :
    """ Book array statement """
    return {
        'id':row[0],
        'title':row[1],
        'author':row[2],
        'editor':row[3],
        'editPub':row[4],
        'summary':row[5],
        'cover':row[6]
    }
if __name__ == "__main__":
    # read server parameters
    params = config('config.ini', 'server')
    # Launch Flask server
    app.run(debug=params['debug'], host=params['host'], port=params['port'])