import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password

from performance.serializers import *

class QuestionModelViewTest(APITestCase):
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

        question_data = {
            "title": "Introduction",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        Question.objects.create(**question_data)
    
    def test_get_question_valid(self):
        # Getting a valid question with quetion_id=1 with an authneticated user
        response = self.client.get(reverse("performance:question", args=[1]))
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["question_id"], 1)
        self.assertEqual(data["title"], "Introduction")
    
    def test_get_question_invalid(self):
        # Getting a valid question with quetion_id=2 which does not exist
        response = self.client.get(reverse("performance:question", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_get_question_with_unauthenticated_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Getting a valid question with quetion_id=1 with an unauthneticated user
        response = self.client.get(reverse("performance:question", args=[1]))
        self.assertEqual(response.status_code, 401)

class QuestionListModelViewTest(APITestCase):
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

        question_data = {
            "question_id": 1,
            "title": "Introduction",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        Question.objects.create(**question_data)
    
    def test_get_question_list_valid(self):
        # Getting valid question list with an authneticated user
        response = self.client.get(reverse("performance:question_list"))
        self.assertEqual(response.status_code, 200)

        data = response.data
        # Response will contain 1 question
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["question_id"], 1)
        self.assertEqual(data[0]["title"], "Introduction")

    def test_get_question_list_with_unauthenticated_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Getting valid question list with an unauthneticated user
        response = self.client.get(reverse("performance:question_list"))
        self.assertEqual(response.status_code, 401)
    
    def test_post_question_list_valid(self):
        # Making the user a staff
        user1 = User.objects.get(user_id=1)
        user1.is_staff = True
        user1.save()

        # Confirming the user1 is a staff
        user1 = User.objects.get(user_id=1)
        self.assertTrue(user1.is_staff)

        # Authorizing user1 for login
        self.client.force_authenticate(user1)

        question_data = {
            "title": "Introduction1",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        # Posting valid question with an authneticated user
        response = self.client.post(reverse("performance:question_list"), json.dumps(question_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        data = response.data
        self.assertEqual(data["question_id"], 2)
        self.assertEqual(data["title"], "Introduction1")
    
    def test_post_question_list_with_non_staff_invalid(self):
        question_data = {
            "title": "Introduction1",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        # Posting valid question with an authneticated user
        response = self.client.post(reverse("performance:question_list"), json.dumps(question_data), content_type="application/json")
        self.assertEqual(response.status_code, 401)

        data = response.data
        self.assertEqual(data["error"], "Not Authorised")
    
    def test_post_question_list_with_unautneticated_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)
        question_data = {
            "title": "Introduction1",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        # Posting valid question with an authneticated user
        response = self.client.post(reverse("performance:question_list"), json.dumps(question_data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
