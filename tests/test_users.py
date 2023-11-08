import unittest
import requests
from ENT_BACK.modules.users import *



class UsersGetTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5050/users" 

    def test_get_users(self):
        response = requests.get(f'{self.BASE_URL}')
        self.assertEqual(response.status_code, 200)
        print("Test 1 : Get all users succesful")
        
        

if __name__ == '__main__':
    unittest.main()
