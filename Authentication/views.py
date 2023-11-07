from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.db.models import Q
fake = Faker()


class CustomUserRegistration(APIView):
    def post(self, request):
        username = request.data.get('username')

        if CustomUser.objects.filter(username=username).exists():
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': 'Username address already in use.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate and save the secret phrases
            user.secret_phrase_1 = fake.word()
            user.secret_phrase_2 = fake.word()
            user.secret_phrase_3 = fake.word()
            user.secret_phrase_4 = fake.word()
            user.secret_phrase_5 = fake.word()
            user.secret_phrase_6 = fake.word()
            user.secret_phrase_7 = fake.word()
            user.secret_phrase_8 = fake.word()
            user.secret_phrase_9 = fake.word()
            user.secret_phrase_10 = fake.word()
            user.secret_phrase_11 = fake.word()
            user.secret_phrase_12 = fake.word()
            user.save()

            # Include the secret phrases in the response
            secret_phrases = [
                user.secret_phrase_1,
                user.secret_phrase_2,
                user.secret_phrase_3,
                user.secret_phrase_4,
                user.secret_phrase_5,
                user.secret_phrase_6,
                user.secret_phrase_7,
                user.secret_phrase_8,
                user.secret_phrase_9,
                user.secret_phrase_10,
                user.secret_phrase_11,
                user.secret_phrase_12,
            ]

            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'message': 'Welcome, your account is successfully registered.',
                'secret_phrases': secret_phrases,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class SecretPhrasesList(APIView):
    def get(self, request, username):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        secret_phrases = [
            user.secret_phrase_1,
            user.secret_phrase_2,
            user.secret_phrase_3,
            user.secret_phrase_4,
            user.secret_phrase_5,
            user.secret_phrase_6,
            user.secret_phrase_7,
            user.secret_phrase_8,
            user.secret_phrase_9,
            user.secret_phrase_10,
            user.secret_phrase_11,
            user.secret_phrase_12,
        ]

        return Response({'secret_phrases': secret_phrases}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        secret_phrases = request.data.get('secret_phrases', [])

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        elif secret_phrases:
            # Build a query for matching secret phrases
            query = Q()
            for secret in secret_phrases:
                query &= Q(secret_phrase_1=secret) | Q(secret_phrase_2=secret) | Q(secret_phrase_3=secret) | Q(secret_phrase_4=secret) | Q(secret_phrase_5=secret) | Q(secret_phrase_6=secret) | Q(secret_phrase_7=secret) | Q(secret_phrase_8=secret) | Q(secret_phrase_9=secret) | Q(secret_phrase_10=secret) | Q(secret_phrase_11=secret) | Q(secret_phrase_12=secret)

            found_user = CustomUser.objects.filter(query).first()

            if found_user:
                # You can perform actions for secret phrase login here
                return Response({'message': 'Secret phrases matched', 'username': found_user.username, 'custom_id': found_user.custom_id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Secret phrases do not match any user'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if username and new_password:
            try:
                user = CustomUser.objects.get(username=username)
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)