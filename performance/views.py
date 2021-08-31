from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny

from performance.models import User
from performance.serializers import UserSerializer

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
            print(type(user))
            data = serializer.data
            remove_password(data)    # Removing hashed password
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data={"error": "Please enter valid data :("}, status=status.HTTP_400_BAD_REQUEST)
    
class getUserFromEmail(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={"error": "User does not exist :("}, status=status.HTTP_404_NOT_FOUND)
        
        data = UserSerializer(user).data
        remove_password(data)    # Removing hashed password        
        return Response(data=data, status=status.HTTP_200_OK)
    
class getUserFromUserId(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(data={"error": "User does not exist :("}, status=status.HTTP_404_NOT_FOUND)
        
        data = UserSerializer(user).data
        remove_password(data)    # Removing hashed password
        return Response(data=data, status=status.HTTP_200_OK)


        
