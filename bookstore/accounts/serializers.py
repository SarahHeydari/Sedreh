from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'balance']
        read_only_fields = ['user_type', 'balance']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        available_books = Book.objects.filter(available=True).values('id', 'title', 'price')

        data.update({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
                "balance": user.balance
            },
            "books": list(available_books),
            "redirect_to": "/accounts/profile/"
        })
        return data
