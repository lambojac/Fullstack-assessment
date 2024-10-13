from django.test import TestCase
from .models import Project
from django.contrib.auth.models import User

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        Project.objects.create(
            name="Test Project",
            description="A test project",
            status="in_progress",
            priority="mid",
            created_by=self.user
        )

    def test_project_creation(self):
        project = Project.objects.get(name="Test Project")
        self.assertEqual(project.description, "A test project")
