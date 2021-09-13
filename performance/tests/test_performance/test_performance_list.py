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

class PerformanceListModelViewTest(APITestCase):
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
    
    def test_get_performance_list_valid(self):
        # Getting valid performance list with an authneticated user
        response = self.client.get(reverse("performance:performance_list"))
        self.assertEqual(response.status_code, 200)

        data = response.data
        # Response will contain 1 performance
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["performance_id"], 1)
        self.assertEqual(data[0]["user"], 1)
        self.assertEqual(data[0]["concentration"], 66)

    def test_get_performance_list_with_unauthenticated_user_invalid(self):
        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Getting valid performance list with an unauthneticated user
        response = self.client.get(reverse("performance:performance_list"))
        self.assertEqual(response.status_code, 401)
    
    @patch.object(AnalyzeVideo, 'analyze_audio')
    def test_post_performance_list_without_saving_video_valid(self, mock_post):
        # Posting valid performance with an authneticated user without saving the video
        print()
        print("For this test, an empty video is being used with no sound. So an ignored warning/error is expected for generating audio.")

        # Confirming that there is no entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 0)

        # Making an empty video file 
        location = r"performance\tests\test_performance\test_video.mp4"
        size = (200, 100)
        duration = 5
        fps = 25 
        color = (0,0,0)
        ColorClip(size, color, duration=duration).write_videofile(location, fps=fps)  
        
        with open(location, "rb") as t:
            f = File(t, "test_video.mp4")
            data = {
                "question_id": 1,
                "file": f
            }
            response = self.client.post(reverse("performance:performance_list"), data=data)
            self.assertEqual(response.status_code, 201)
        # Confirming that there is no entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 0)
        os.remove(location)

    @patch.object(AnalyzeVideo, 'analyze_audio')
    def test_post_performance_list_with_saving_video_valid(self, mock_post):
        # Posting valid performance with an authneticated user with saving the video
        print()
        print("For this test, an empty video is being used with no sound. So an ignored warning/error is expected for generating audio.")

        # Confirming that there is no entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 0)

        # Updating the user1 to save video
        user1 = User.objects.get(user_id=1)
        user1.save_video = True
        user1.save()

        # Authorizing user1 for login
        self.client.force_authenticate(user1)

        location = r"performance\tests\test_performance\test_video.mp4"
        size = (200, 100)
        duration = 5
        fps = 25 
        color = (0,0,0)
        ColorClip(size, color, duration=duration).write_videofile(location, fps=fps)  
        
        with open(location, "rb") as t:
            f = File(t, "test_video.mp4")
            data = {
                "question_id": 1,
                "file": f
            }
            response = self.client.post(reverse("performance:performance_list"), data=data)
            self.assertEqual(response.status_code, 201)
        
        # Confirming that there is an entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 1)

        self.assertEqual(PerformanceVideo.objects.all()[0].file.name, "user_1/test_video.mp4")
        os.remove(os.path.join(MEDIA_ROOT, "user_1/test_video.mp4"))
        os.remove(location)
    
    @patch.object(AnalyzeVideo, 'analyze_audio')
    def test_post_performance_list_with_unauthenticated_user_valid(self, mock_post):
        # Posting valid performance with an authneticated user without saving the video
        print()
        print("For this test, an empty video is being used with no sound. So an ignored warning/error is expected for generating audio.")

        # First removing the authenticated user
        self.client.force_authenticate(user=None)

        # Confirming that there is no entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 0)

        # Making an empty video file 
        location = r"performance\tests\test_performance\test_video.mp4"
        size = (200, 100)
        duration = 5
        fps = 25 
        color = (0,0,0)
        ColorClip(size, color, duration=duration).write_videofile(location, fps=fps)  
        
        with open(location, "rb") as t:
            f = File(t, "test_video.mp4")
            data = {
                "question_id": 1,
                "file": f
            }
            response = self.client.post(reverse("performance:performance_list"), data=data)
            self.assertEqual(response.status_code, 401)
        # Confirming that there is no entry of the video
        self.assertEqual(PerformanceVideo.objects.count(), 0)
        os.remove(location)

