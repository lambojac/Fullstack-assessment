from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer

class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # If admin, list all projects; if user, list only their projects
        if request.user.is_staff:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(assigned_to=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only admins can create projects
        if request.user.is_staff:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == project.assigned_to:
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff:
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff:
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
