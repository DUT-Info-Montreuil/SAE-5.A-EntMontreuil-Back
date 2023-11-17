#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from config import config
from controllers.Teachers_controllers import teachers_bp
from controllers.Users_controllers import users_bp
from controllers.Roles_controllers import roles_bp
from controllers.Students_controllers import students_bp
from controllers.Absence_controller import absences_bp
from controllers.Training_controller import training_bp
from controllers.Material_controller import materials_bp
from controllers.Authentificate_controller import authentificate_bp

from flask_jwt_extended import JWTManager

# Register the main controller
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "iG98fdsVFD5fds"
jwt = JWTManager(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
swagger = Swagger(app)
#blueprint
app.register_blueprint(absences_bp)
app.register_blueprint(training_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(users_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(students_bp)
app.register_blueprint(authentificate_bp)

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