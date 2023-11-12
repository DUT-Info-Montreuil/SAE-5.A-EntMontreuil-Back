import unittest
import requests
import json

class TestAbsencesRoutes(unittest.TestCase):
    BASE_URL = 'http://localhost:5050'

    def test_get_user_absences_success(self):
        # Test de récupération des absences de l'utilisateur 2 (succès)
        response = requests.get(f'{self.BASE_URL}/absences/student/2', headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        absences = response.json()
        self.assertIsInstance(absences, list)
        for absence in absences:
            self.assertIn('id_Student', absence)
            self.assertIn('id_Course', absence)
            self.assertIn('reason', absence)
            self.assertIn('justify', absence)

    def test_get_user_absences_failure(self):
        # Test de récupération des absences d'un utilisateur inexistant (échec)
        response = requests.get(f'{self.BASE_URL}/absences/student/9999', headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], "L'étudiant spécifié n'existe pas.")

    def test_update_user_course_absence_success(self):
        # Test de mise à jour d'une absence existante (succès)
        data = {
           "datas": {
                "reason": "Nouvelle raison de l'absence",
                "justify": False
            }
        }
        response = requests.put(f'{self.BASE_URL}/absences/student/1/course/1', json=data, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertTrue(response_data['message'].startswith("Absence mise à jour"))

    def test_update_user_course_absence_failure(self):
        # Test de mise à jour d'une absence inexistante (échec)
        data = {
            "datas": {
                "reason": "Nouvelle raison de l'absence",
                "justify": True
            }
        }
        response = requests.put(f'{self.BASE_URL}/absences/student/2/course/9999', json=data, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], "Absence non trouvée ou aucune modification effectuée")

    def test_add_user_course_absence_success(self):
        # Test d'ajout d'une nouvelle absence (succès)
        data = {
            "datas": {
                "reason": "Nouvelle raison de l'absence",
                "justify": True
            }
        }
        response = requests.post(f'{self.BASE_URL}/absences/student/2/course/1/add', json=data, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertTrue(response_data['message'].startswith("Absence ajoutée avec succès"))


    def test_delete_user_course_absence_failure(self):
        # Test de suppression d'une absence inexistante (échec)
        response = requests.delete(f'{self.BASE_URL}/absences/student/2/course/9999', headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], "Absence non trouvée ou déjà supprimée")

if __name__ == "__main__":
    unittest.main()
