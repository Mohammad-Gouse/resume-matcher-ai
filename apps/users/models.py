from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Resume Matcher.
    """

    email = models.EmailField(unique=True)

    USER_TYPE_CHOICES = (
        ("candidate", "Candidate"),
        ("recruiter", "Recruiter"),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="candidate",
    )

    # Use email instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email