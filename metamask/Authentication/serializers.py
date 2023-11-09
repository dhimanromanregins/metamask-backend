from rest_framework import serializers
from .models import *
from django.core.validators import MinLengthValidator,MaxLengthValidator, MaxValueValidator, MinValueValidator, validate_email
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8, message="Password must be at least 8 characters long."),
        ]
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8, message="Confirm Password must be at least 8 characters long."),
        ]
    )

    class Meta:
        model = CustomUser
        fields = ("id",'username', 'password', 'confirm_password','secret_phrase_1')

        extra_kwargs = {
            'username': {'required': True, 'validators': [MinLengthValidator(4), MaxLengthValidator(150)]},
        }

    def validate(self, data):
        # Check if password and confirm_password match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Password and confirm_password do not match.")
        return data

    def create(self, validated_data):
        # Remove confirm_password from the validated_data
        validated_data.pop('confirm_password', None)
        # Create a new user with a hashed password
        user = CustomUser.objects.create_user(**validated_data)
        return user