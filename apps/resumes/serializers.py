from rest_framework import serializers
from .models import Resume


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "file")

    def validate_file(self, value):
        # ✅ File size limit (e.g. 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File too large (max 5MB)")

        # ✅ Allowed types
        allowed_types = ["application/pdf",
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF and DOCX allowed")

        return value