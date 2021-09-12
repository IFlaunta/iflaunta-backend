from requests import api
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import Performance, User, Question, PerformanceVideo
from .serializers import PerformanceSerializer, PerformanceVideoSerializer, UserSerializer, QuestionSerializer
from .analyze_video.analyze_video import AnalyzeVideo

ANALYSIS_VIDEOS_DIR = settings.ANALYSIS_VIDEOS_DIR

def remove_password(data):
    if(isinstance(data, dict)):
        data.pop("password", "Doesn't contain password")
    return

class addUser(APIView):

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if(serializer.is_valid()):
            user = serializer.save(password=make_password(data["password"]))
            data = serializer.data
            remove_password(data)    # Removing hashed password
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data={"error": "Please enter valid data :("}, status=status.HTTP_400_BAD_REQUEST)
    
def userPublicData(user):
    '''
    Function to get the public data of a user
    
    Currently, it is giving all the present data
    '''
    if(user):
        data = UserSerializer(user).data
        remove_password(data)
        return data
    return {}

class getUser(APIView):
    '''
    View for getting all the data (private+public) of an authenticated user 
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            data = UserSerializer(user).data
            remove_password(data)    # Removing hashed password
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getUserPublicDataFromEmail(APIView):
    '''
    View for getting all public data of a user with email

    This view can be accessed by an authenticated user
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={"error": "User does not exist :("}, status=status.HTTP_404_NOT_FOUND)
        
        data = userPublicData(user)
        return Response(data=data, status=status.HTTP_200_OK)
    
class getUserPublicDataFromUserId(APIView):
    '''
    View for getting all public data of a user with user_id

    This view can be accessed by an authenticated user
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(data={"error": "User does not exist :("}, status=status.HTTP_404_NOT_FOUND)
        
        data = userPublicData(user)
        return Response(data=data, status=status.HTTP_200_OK)

class questionList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        questions = Question.objects.all()
        serializers = QuestionSerializer(questions, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        if(user==None or (not user.is_staff)):
            return Response({"error": "Not AUthorised"}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        serializer = QuestionSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

class question(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, question_id):
        try:
            question = Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            return Response(data={"error": "Question does not exist :("}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class userLogOut(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if(refresh_token):
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={"message": "logged out!"}, status=status.HTTP_200_OK)
        return Response(data={"error": "Please send refresh token."}, status=status.HTTP_400_BAD_REQUEST)

class performanceList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            performances = user.userPerformance.all()
            serializers = PerformanceSerializer(performances, many=True)
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        user = request.user
        question_id = request.data.get("question_id")
        file = request.FILES.get("file")

        try:
            # Storing video response for analysis
            fs = FileSystemStorage(location=ANALYSIS_VIDEOS_DIR)
            file_name = fs.save(file.name, file)
            file_path = fs.path(file_name)

            # Analysing the video response
            vid = AnalyzeVideo(file_path)
            vid.analyze()
            confidence = vid.confidence
            video_score = vid.video_score
            # Clearing the files 
            vid.clear()

            # Calculating performance factors and saving performance
            performance_data = {
                "user": user.user_id,
                "question": question_id, 
                "concentration": int(0.6*confidence+0.4*video_score),
                "eyecontact": video_score, 
                "clarity": int(0.9*confidence),
                "understanding": int(0.2*video_score+0.8*confidence), 
                "confidence": int(0.9*confidence+0.1*video_score)
            }
            serializer = PerformanceSerializer(data=performance_data)
            if(serializer.is_valid()):
                serializer.save()
                performance_data = serializer.data
                performance_id = performance_data["performance_id"]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            # Checking whether response video has to be stored or not
            if(not self.check_save_response(user.user_id)):
                # If not, just return the current performance
                return Response(data=performance_data, status=status.HTTP_201_CREATED)

            # saving video response
            video_data = {
                "performance": performance_id, 
                "file": file
            }
            serializer = PerformanceVideoSerializer(data=video_data)
            if(serializer.is_valid()):
                serializer.save()
            return Response(data=performance_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def check_save_response(self, user_id):
        # Check if the user is granted the facility to store video
        # ...
        # For now, videos are not being stored
        return False

class performance(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, performance_id):
        try:
            performance = Performance.objects.get(performance_id=performance_id)
        except Performance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if(performance.user_id!=user.user_id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PerformanceSerializer(performance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class performanceVideo(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, performance_id):
        try:
            performance = Performance.objects.get(performance_id=performance_id)
        except Performance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if(performance.user_id!=user.user_id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            performance_video = performance.performanceVideo
        except Exception as e:
            return Response(data={"error": "No video exists for this performance"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PerformanceVideoSerializer(performance_video)
        return Response(data=serializer.data, status=status.HTTP_200_OK)    
    