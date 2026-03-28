from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Resume
from .serializers import ResumeUploadSerializer
from .services import parse_resume


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
            status="processing",  #  update
        )

        try:
            parsed_data = parse_resume(resume.file.path, resume.file_type)

            resume.parsed_data = parsed_data
            resume.status = "parsed"
            resume.save()

        except Exception as e:
            resume.status = "failed"
            resume.save()

        return Response(
            {
                "id": resume.id,
                "status": resume.status,
                "parsed_data": resume.parsed_data,
            },
            status=status.HTTP_201_CREATED,
        )