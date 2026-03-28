from django.urls import path, include

urlpatterns = [
    path("health/", include("apps.common.urls")),
    path("users/", include("apps.users.urls")),
    path("resumes/", include("apps.resumes.urls")),
    path("jobs/", include("apps.jobs.urls"))
]