from rest_framework import serializers
from performance.models import User, Question, PastPerformance, PastPerformanceVideo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'is_staff']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_id', 'title', 'description', 'keywords', 'question_grade', 'tags']

class PastPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastPerformance
        fields = ['user_id', 'performance_id', 'question_id', 'concentration', 'eyecontact', 'clarity', 'understanding', 'confidence', 'performance_datetime']

class PastPerformanceVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastPerformanceVideo
        fields = ['video_id', 'performance_id', 'file']
