import unittest
import requests
import json


####################################### TEST ADD STUDENTS #######################################
class TestAddStudents(unittest.TestCase):
    BASE_URL = "http://localhost:5050/students/add"  

    def test_add_students_successful(self):
        student_data = {
                "datas" : {
                    "id" : 1,
                    "user": {
                        "username": "tesdet",
                        "password": "testSqd9559995##ord",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com"
                    },
                    "apprentice": True
                }
            }
        data_json = json.dumps(student_data)
        response = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Student added, save the password for this user it will not be recoverable")
        print("Test 1 : Succesful student add")

    def test_add_students_missing_datas_field(self):
        student_data = {
                        "id" : 1,
                        "user": {
                            "username": "tesdet",
                            "password": "testSqd9559995##ord",
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "john.doe@example.com"
                        },
                        "apprentice": True
                    
                }
        data_json = json.dumps(student_data)
        response = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "Missing 'datas' field in JSON")
        print("Test 2 : Error student add missing 'datas' field")

    def test_add_students_missing_user_field(self):
        student_data = {
                "datas" : {
                    "id" : 1,
                    "apprentice": True
                }
            }
        data_json = json.dumps(student_data)
        response = requests.post(f'{self.BASE_URL}', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "Missing 'user' field in JSON")
        print("Test 3 : Error student add missing 'user' field")    



####################################### TEST REMOVE STUDENTS #######################################
class TestRemoveStudents(unittest.TestCase):
    BASE_URL = "http://localhost:5050/students/remove"  

    def test_remove_students_successful(self):
        student_data = {
                "datas" : {
                    "id" : 1,
                    "user": {
                        "username": "tesdet",
                        "password": "testSqd9559995##ord",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com"
                    },
                    "apprentice": True
                }
            }
        data_json = json.dumps(student_data)

        response = requests.delete(f'{self.BASE_URL+"/1"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Student deleted")
        print("Test 4 : Succesful remove student")

    def test_remove_students_id_not_exist(self):
        response = requests.delete(f'{self.BASE_URL+"/0"}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "id_student : '0' not exists")
        print("Test 5 : Error remove student id not exist")
          

####################################### TEST UPDATE STUDENTS #######################################
class TestUpdateStudents(unittest.TestCase):

    def setUp(self):
        # Ce code sera exécuté avant chaque cas de test
        student_data = {
                "datas" : {
                    "id" : 1,
                    "user": {
                        "username": "test",
                        "password": "testSqd9559995##ord",
                        "first_name": "Priyank",
                        "last_name": "Solanki",
                        "email": "priyank@example.com"
                    },
                }
            }
        data_json = json.dumps(student_data)
        requests.post("http://localhost:5050/students/add", data=data_json, headers={"Content-Type": "application/json"})
        pass

    def tearDown(self):
        # Ce code sera exécuté après chaque cas de test
        requests.delete("http://localhost:5050/students/remove/1")
        pass

    BASE_URL = "http://localhost:5050/students/update" 

    def test_update_students_successful(self):
        student_data = {
            "datas": {
                "user": {
                    "username": "newusername",
                    "password": "newpassworD123#",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com"
                }
            }
        }
        data_json = json.dumps(student_data)
        response = requests.patch(f'{self.BASE_URL}/1', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Student update")
        print("Test 6 : Succesful student update")

    def test_update_students_missing_datas_field(self):
        student_data = {
            "user": {
                "username": "newusername",
                "password": "newpassword",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        }
        data_json = json.dumps(student_data)
        response = requests.patch(f'{self.BASE_URL}/1', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "Missing 'datas' field in JSON")
        print("Test 7 : Error student update missing 'datas' field")

    def test_update_students_empty_user_field(self):
        student_data = {
            "datas": {
                "user": {}
            }
        }
        data_json = json.dumps(student_data)
        response = requests.patch(f'{self.BASE_URL}/1', data=data_json, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), "Empty 'user' field in JSON")
        print("Test 8 : Error student update empty 'user' field")


####################################### TEST ADD STUDENTS CSV #######################################
class TestCSVAddStudents(unittest.TestCase):
    BASE_URL = "http://localhost:5050/students/add"


    def test_csv_add_students_invalid_csv(self):
        csv_path = "invalid_path.pdf"
        response = requests.post(f'{self.BASE_URL}/{csv_path}')
        self.assertEqual(response.status_code, 400)
        print("Test 9 : Error student add with csv incorrect path")

if __name__ == '__main__':
    unittest.main()
