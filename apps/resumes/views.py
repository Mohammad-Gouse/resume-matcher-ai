from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Resume
from .serializers import ResumeUploadSerializer


class ResumeUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        resume = Resume.objects.create(
            user=request.user,
            file=file,
            original_filename=file.name,
            file_size=file.size,
            file_type=file.content_type,
        )

        return Response(
            {
                "id": resume.id,
                "message": "Resume uploaded successfully",
                "status": resume.status,
            },
            status=status.HTTP_201_CREATED,
        )