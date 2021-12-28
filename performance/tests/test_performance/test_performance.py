import os
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from django.core.files import File
from moviepy.editor import ColorClip
from django.conf import settings
from unittest.mock import patch

from performance.serializers import *
from performance.analyze_video.analyze_video import AnalyzeVideo

MEDIA_ROOT = settings.MEDIA_ROOT

class PerformanceModelViewTest(APITestCase):
    def setUp(self):
        user1_data = {
            "first_name": "Flaunta",
            "last_name": "Goddess",
            "email": "iflaunta@gmail.com",
            "password": make_password("1234")
        }
        user1 = User.objects.create(**user1_data)
        question_data = {
            "title": "Introduction",
            "description": "Please introduce yourself.",
            "keywords": "introduce", # Comma Separated words
            "question_grade": 10,   # Any weightage
            "tags": "personality"   # Comma Separated words
        }
        question1 = Question.objects.create(**question_data)

        performance_data = {
            "user": user1,
            "question": question1, 
            "concentration": int(0.6*70+0.4*60),
            "eyecontact": 60, 
            "clarity": int(0.9*70),
            "understanding": int(0.2*60+0.8*70), 
            "confidence": int(0.9*70+0.1*60)
        }

        Performance.objects.create(**performance_data)

        # Authorizing user1 for login
        self.client.force_authenticate(user1)
    
    def test_get_performance_valid(self):
        # Getting a valid performance with performance_id=1 with an authorized user
        response = self.client.get(reverse("performance:performance", args=[1]))
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["performance_id"], 1)
        self.assertEqual(data["user"], 1)
        self.assertEqual(data["concentration"], 66)
    
    def test_get_performance_invalid(self):
        # Getting a valid performance with performance_id=2 which does not exist
        response = self.client.get(reverse("performance:performance", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_get_performance_with_unauthenticated_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Getting a valid performance with performance_id=1 with an unauthneticated user
        response = self.client.get(reverse("performance:performance", args=[1]))
        self.assertEqual(response.status_code, 401)
