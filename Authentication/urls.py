
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CustomUserRegistration.as_view(), name='user-registration'),
    path('api/secret-phrases/<str:username>/', SecretPhrasesList.as_view(), name='secret-phrases-list'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]