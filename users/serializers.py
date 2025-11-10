from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import Serializer


class RegisterSerializer(Serializer):
    name = CharField(max_length=128, required=True)
    email = EmailField(max_length=128, required=True)
    password = CharField(max_length=64, write_only=True, required=True)

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'],
        )


class LoginSerializer(Serializer):
    email = EmailField(max_length=128, required=True)
    password = CharField(max_length=64, required=True)
