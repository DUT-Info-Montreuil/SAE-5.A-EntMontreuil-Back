import unittest
from flask import Flask, Response
from unittest.mock import patch
from users import users_bp
from users import *

class UsersGetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(users_bp)
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        # Vous pouvez ajouter davantage d'assertions pour vérifier la réponse, par exemple,
        # vérifier la structure des données renvoyées.

class TestUpdateUsers(unittest.TestCase):
    def setUp(self):
        # Créez un objet d'application Flask minimal pour les tests
        self.app = Flask(__name__)

    def test_update_users_successful(self):
        # Test a successful update
        user_data = {
            "password": "NewPassword123#",
            "email": "newemail@example.com",
        }
        id_user = 91  # Replace with a valid user ID
        with self.app.app_context():
            with patch('users.connect_pg') as mock_connect_pg:
                response, http_status = update_users(user_data, id_user)
                self.assertEqual(http_status, 200)  # Vérifiez le code d'état
                self.assertIn("User update", response.get_data(as_text=True))  # Obtenez le contenu de la réponse

    def test_update_users_invalid_password(self):
        # Test update with an invalid password
        user_data = {
            "password": "NewPa#",
            "email": "newemail@example.com",
        }
        id_user = 91  # Replace with a valid user ID
        with self.app.app_context():
            with patch('users.connect_pg') as mock_connect_pg:
                response, http_status = update_users(user_data, id_user)
                self.assertEqual(http_status, 400)  # Vérifiez le code d'état
                self.assertIn("password need to contains minimum 12 characters", response.get_data("error")) 



if __name__ == '__main__':
    unittest.main()
