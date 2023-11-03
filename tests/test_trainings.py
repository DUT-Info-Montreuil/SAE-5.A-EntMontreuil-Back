import unittest
import requests

class AddTrainingTestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5050'

    def test_add_training_missing_datas_key(self):
         # Envoie une requête POST avec un corps JSON qui ne comprend pas la clé 'datas'
        response = requests.post(
            f'{self.BASE_URL}/trainings/add',
            json={},  # An empty dict does not have the 'datas' key
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request status code")
        response_json = response.json()
        self.assertIn('message', response_json, "JSON response does not contain 'message' key")
        self.assertEqual(response_json['message'], "Données manquantes", "Expected error message 'Données manquantes' not found in the response")
   
    def test_add_training_empty_name(self):
        # Envoie une requête POST avec 'name' comme chaîne vide
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': '', 'id_Degree': 1}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "Le nom du parcours est requis")

    def test_add_training_missing_name(self):
        # Envoie une requête POST sans la clé 'name' dans le corps JSON
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'id_Degree': 1}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "Le nom du parcours est requis")

    def test_add_training_invalid_id_degree_type(self):
         # Envoie une requête POST sans la clé 'name' dans le corps JSON
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': 'Training Name', 'id_Degree': 'invalid'}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'), "L'identifiant du diplôme doit être un entier")

    def test_add_training_nonexistent_id_degree(self):
       # Envoie une requête POST avec un 'id_Degree' qui n'existe pas
       # Vous devez simuler ou vous assurer que la fonction does_entry_exist renverra False pour le 'id_Degree' utilisé ici
        response = requests.post(f'{self.BASE_URL}/trainings/add', json={'datas': {'name': 'Training Name', 'id_Degree': 9999999999}}, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('message'),"La formation spécifiée n'existe pas."),

class GetTrainingTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5050/trainings/get"  # Mettez à jour avec l'URL de base de votre API

    def test_get_training_success(self):
        # Teste le cas où le parcours existe
        response = requests.get(f"{self.BASE_URL}/1")  # Assurez-vous que le parcours avec l'ID 1 existe dans la base de données pour ce test
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json())

    def test_get_training_not_found(self):
        # Teste le cas où le parcours n'existe pas
        response = requests.get(f"{self.BASE_URL}/9999")  # Utilisez un ID qui n'existe pas dans la base de données
        self.assertEqual(response.status_code, 404)
        self.assertIn('Parcours non trouvé', response.json()['message'])


if __name__ == '__main__':
    unittest.main()
