from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from performance.models import User, Question
from performance.serializers import UserSerializer, QuestionSerializer

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
