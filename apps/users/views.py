from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import RegisterSerializer, UserSerializer
from apps.users.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


def get_token_response(user):
    refresh = RefreshToken.for_user(user)

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type,
        },
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "access_expires_in": int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
        "refresh_expires_in": int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
    }



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            get_token_response(user),
            status=status.HTTP_201_CREATED,
        )



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        if not username_or_email or not password:
            return Response(
                {"error": "Username/email and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if input is email
        user_obj = User.objects.filter(email=username_or_email).first()

        if user_obj:
            username = user_obj.username
        else:
            username = username_or_email

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(get_token_response(user), status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
