from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, PasswordChangeSerializer, UserUpdateSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import get_user_model

User = get_user_model()


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
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            get_token_response(user),
            status=status.HTTP_200_OK,
        )

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 🔥 Admin sees all, user sees only self
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
