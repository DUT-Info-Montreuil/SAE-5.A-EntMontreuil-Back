#FROM
from flask import Flask
from flask_cors import CORS
from config import config
from controllers.teachers_controllers import teachers_bp
from controllers.users_controllers import users_bp

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.register_blueprint(users_bp)
app.register_blueprint(teachers_bp)

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