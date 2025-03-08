from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
