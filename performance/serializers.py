from rest_framework import serializers
from performance.models import User, Question, Performance, PerformanceVideo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'save_video']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_id', 'title', 'description', 'keywords', 'question_grade', 'tags']

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['user', 'performance_id', 'question', 'concentration', 'eyecontact', 'clarity', 'understanding', 'confidence', 'performance_datetime']

class PerformanceVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceVideo
        fields = ['video_id', 'performance', 'file']
