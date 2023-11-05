import unittest
import requests
import json

class TestAddTeachers(unittest.TestCase):
    BASE_URL = "http://localhost:5050/teachers/add"  
    
    
    def test_first(self):
        teacher_data = {
            "datas": {
                "id" : 1,
                "user": {
                    "username": "teacher1",
                    "password": "securepassworD#1",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com"
                },
                "desktop": "A1",
                "initial": "JD",
            }
        }
        data_json = json.dumps(teacher_data)
        response = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Teachers added")
        print("Test 1 : sucessful")

    def test_second(self):
        teacher_data = {
            "datas": {
                "user": {
                    "username": "teacher2",
                    "password": "securepassworD#1",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com"
                },
                "desktop": "A1",
                "initial": "JD",
            }
        }
        data_json = json.dumps(teacher_data)
        response2 = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json().get('error'), "Initial 'JD' already exists")
        print("Test 2 : initial already exist")


        
        
    def test_add_teachers_missing_initial_field(self):
        teacher_data = {
            "datas": {
                "user": {
                    "username": "teacher3",
                    "password": "securepassworD#1",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com"
                },
                "desktop": "A1",
            }
        }
        data_json = json.dumps(teacher_data)

        response3 = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(response3.json().get('error'), "Missing 'initial' field")
        print("Test 3 : missing initial field")

        
        
        
        
class TestRemoveTeachers(unittest.TestCase):
    BASE_URL = "http://localhost:5050/teachers/remove"  

    def test_remove_teachers_successful(self):
        response = requests.delete(self.BASE_URL+"/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Teacher deleted")
        
    def test_add_teachers_missing_initial_field(self):

        response = requests.delete(self.BASE_URL+"/0")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "id_teacher : '0' not exists")
        
        
   

if __name__ == '__main__':
    unittest.main()
