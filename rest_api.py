#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from config import config
from datetime import timedelta
from controllers.Teachers_controllers import teachers_bp
from controllers.Users_controllers import users_bp
from controllers.Roles_controllers import roles_bp
from controllers.Students_controllers import students_bp
from controllers.Absence_controllers import absences_bp
from controllers.Training_controllers import training_bp
from controllers.Material_controllers import materials_bp
from controllers.Classroom_controllers import Classroom_bp
from controllers.Authentificate_controllers import authentificate_bp
from controllers.Degree_controllers import degrees_bp
from controllers.Promotions_controllers import promotions_bp
from controllers.Td_controllers import td_bp
from controllers.Tp_controllers import tp_bp
from controllers.Courses_controllers import courses_bp
from controllers.Ressources_controllers import resources_bp
from controllers.Settings_controllers import settings_bp
from controllers.Calls_controllers import calls_bp
from flask_jwt_extended import JWTManager

# Register the main controller
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "iG98fdsVFD5fds"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
swagger = Swagger(app)
#blueprint
app.register_blueprint(absences_bp)
app.register_blueprint(training_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(Classroom_bp)
app.register_blueprint(users_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(students_bp)
app.register_blueprint(authentificate_bp)
app.register_blueprint(degrees_bp)
app.register_blueprint(promotions_bp)
app.register_blueprint(td_bp)
app.register_blueprint(tp_bp)
app.register_blueprint(resources_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(calls_bp)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response


if __name__ == "__main__":
    # Lisez les paramètres du serveur depuis config.ini
    params = config('config.ini', 'server')
    
    # Créez un contexte SSL avec les fichiers de certificat et de clé
    context = (params['cert'], params['key'])
    
    # Lancez l'application Flask avec SSL activé
    app.run(debug=params['debug'], host=params['host'], port=params['port'], ssl_context=context)
