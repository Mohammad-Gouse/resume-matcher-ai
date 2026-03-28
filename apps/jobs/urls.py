from django.urls import path
from .views import JobCreateView, MatchResumeJobView

urlpatterns = [
    path("create/", JobCreateView.as_view()),
    path("match/", MatchResumeJobView.as_view()),
]