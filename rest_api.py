#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from config import config

from controllers.Absence_controller import absences_bp
from controllers.Training_controller import training_bp
from controllers.Material_controller import materials_bp
from controllers.Classroom_controller import Classroom_bp

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
swagger = Swagger(app)
#register the absence
app.register_blueprint(absences_bp)
app.register_blueprint(training_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(Classroom_bp)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    # read server parameters
    params = config('config.ini', 'server')
    # Launch Flask server
    app.run(debug=params['debug'], host=params['host'], port=params['port'])