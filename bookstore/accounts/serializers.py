from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.gis.geos import Point


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type', 'longitude', 'latitude']

    def create(self, validated_data):
        lon = validated_data.pop('longitude')
        lat = validated_data.pop('latitude')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            location=Point(lon, lat),
            **validated_data
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
