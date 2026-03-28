from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Job
from .serializers import JobSerializer

from apps.resumes.models import Resume
from .services import calculate_match_score


class JobCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchResumeJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        resume = Resume.objects.get(id=resume_id, user=request.user)
        job = Job.objects.get(id=job_id)

        result = calculate_match_score(
            resume.parsed_data,
            job.required_skills,
        )

        return Response({
            "resume_id": resume.id,
            "job_id": job.id,
            **result
        })