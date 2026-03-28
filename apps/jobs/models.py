from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Job posted by recruiter
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    required_skills = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title