import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password

from performance.serializers import *

class UserModelViewTest(APITestCase):
    def setUp(self):
        user1_data = {
            "first_name": "Flaunta",
            "last_name": "Goddess",
            "email": "iflaunta@gmail.com",
            "password": make_password("1234")
        }
        user1 = User.objects.create(**user1_data)

        # Authorizing user1 for login
        self.client.force_authenticate(user1)
    
    def test_get_user_valid(self):
        # Getting a valid authorized user
        response = self.client.get(reverse("performance:get_user"))
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["user_id"], 1)
        self.assertEqual(data["first_name"], "Flaunta")
        self.assertEqual(data["last_name"], "Goddess")
        self.assertEqual(data["email"], "iflaunta@gmail.com")
    
    def test_get_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)
        # Getting an unauthorized user
        response = self.client.get(reverse("performance:get_user"))
        self.assertEqual(response.status_code, 401)
    
    def test_add_user_valid(self):
        # Adding a new valid user
        user_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        response = self.client.post(reverse("performance:add_user"), json.dumps(user_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        data = response.data
        self.assertEqual(data["user_id"], 2)
        self.assertEqual(data["first_name"], "Flaunta1")
        self.assertEqual(data["last_name"], "Goddess1")
        self.assertEqual(data["email"], "iflaunta1@gmail.com")
    
    def test_add_user_invalid(self):
        # Adding a new invalid user with missing last_name
        user_data = {
            "first_name": "Flaunta1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        response = self.client.post(reverse("performance:add_user"), json.dumps(user_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        # Adding a new invalid user with duplicate email
        user_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta@gmail.com",
            "password": make_password("1234")
        }
        response = self.client.post(reverse("performance:add_user"), json.dumps(user_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_public_data_from_email_valid(self):
        # Making a new user for fetching data of user1
        user2_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        user2 = User.objects.create(**user2_data)
        
        # Authenticating this user2
        self.client.force_authenticate(user=user2)

        # Fetching public data of user1 with email
        response = self.client.get(reverse("performance:get_public_user_from_email", args=["iflaunta@gmail.com"]))
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["user_id"], 1)
        self.assertEqual(data["first_name"], "Flaunta")
        self.assertEqual(data["last_name"], "Goddess")
        self.assertEqual(data["email"], "iflaunta@gmail.com")
    
    def test_get_user_public_data_from_email_invalid(self):
        # Making a new user for fetching data of user1
        user2_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        user2 = User.objects.create(**user2_data)

        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Fetching public data of user1 with email without any authorized user
        response = self.client.get(reverse("performance:get_public_user_from_email", args=["iflaunta@gmail.com"]))
        self.assertEqual(response.status_code, 401)

        # Authenticating user2
        self.client.force_authenticate(user=user2)

        # Fetching public data of a user with email which does not exist in db
        response = self.client.get(reverse("performance:get_public_user_from_email", args=["goddess@gmail.com"]))
        self.assertEqual(response.status_code, 404)
    
    def test_get_user_public_data_from_user_id_valid(self):
        # Making a new user for fetching data of user1
        user2_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        user2 = User.objects.create(**user2_data)
        
        # Authenticating this user2
        self.client.force_authenticate(user=user2)

        # Fetching public data of user1 with email
        response = self.client.get(reverse("performance:get_public_user_from_user_id", args=[1]))
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["user_id"], 1)
        self.assertEqual(data["first_name"], "Flaunta")
        self.assertEqual(data["last_name"], "Goddess")
        self.assertEqual(data["email"], "iflaunta@gmail.com")
    
    def test_get_user_public_data_from_user_id_invalid(self):
        # Making a new user for fetching data of user1
        user2_data = {
            "first_name": "Flaunta1",
            "last_name": "Goddess1",
            "email": "iflaunta1@gmail.com",
            "password": make_password("1234")
        }
        user2 = User.objects.create(**user2_data)

        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Fetching public data of user1 with user_id without any authorized user
        response = self.client.get(reverse("performance:get_public_user_from_user_id", args=[1]))
        self.assertEqual(response.status_code, 401)

        # Authenticating user2
        self.client.force_authenticate(user=user2)

        # Fetching public data of a user with user_id which does not exist in db
        response = self.client.get(reverse("performance:get_public_user_from_user_id", args=[3]))
        self.assertEqual(response.status_code, 404)
