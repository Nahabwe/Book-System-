from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serailizers import UserSerializer

@api_view(['POST'])   
@permission_classes([AllowAny])
def register_user(request):
   serializers=UserSerializer(data=request.data)
   if serializers.is_valid():
      user=User.objects.create_user(
         username=serializers.validated_data['username'],
         email=serializers.validated_data['email'],
         password=serializers.validated_data['password'],
      )
      response={
         'message':'User successfully registered','data':serializers.data
      }
      return Response(response,status=status.HTTP_201_CREATED)
   return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
   username=request.data.get('username')
   password=request.data.get('password')
   user=authenticate(username=username,password=password)
   if user:
      refesh_token=RefreshToken.for_user(user)
      response={
         'refresh':str(refesh_token),
         'access':str(refesh_token.access_token),
         'username':user.username
      }
      return Response(response,status=status.HTTP_200_OK)
   else:
      return Response({'error':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
   try:
      refresh_token=request.data['refresh']
      token=RefreshToken(refresh_token)
      token.blacklist()
      return Response({'message':'Logged out successfuly'},status=status.HTTP_200_OK)
   except KeyError:
      return Response({'error':'Refresh token is requred '},status=status.HTTP_400_BAD_REQUEST)
   except TokenError as e:
      return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

