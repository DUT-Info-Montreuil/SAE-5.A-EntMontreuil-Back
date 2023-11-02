import unittest
import requests

class AddTrainingTestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5050'

    def test_add_training_missing_datas_key(self):
        # Send a POST request with a JSON body that doesn't include the 'datas' key
        response = requests.post(
            f'{self.BASE_URL}/trainings/add',
            json={},  # An empty dict does not have the 'datas' key
            headers={"Content-Type": "application/json"}
        )

        # The rest of the test is the same as before
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request status code")
        response_json = response.json()
        self.assertIn('message', response_json, "JSON response does not contain 'message' key")
        self.assertEqual(response_json['message'], "Données manquantes", "Expected error message 'Données manquantes' not found in the response")
   
    def test_add_training_empty_name(self):
        # Send a POST request with 'name' as an empty string
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': '', 'id_Degree': 1}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "Le nom du parcours est requis")

if __name__ == '__main__':
    unittest.main()
