from django.urls import path
from .views import RegisterView, LoginView, MeView, UserViewSet, PasswordChangeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("change-password/", PasswordChangeView.as_view()),
]

urlpatterns += router.urls