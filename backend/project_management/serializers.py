from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Project

# Define a UserSerializer to convert User objects to JSON-friendly format
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password']  # Add fields you want to expose

# Modify your ProjectSerializer
class ProjectSerializer(serializers.ModelSerializer):
    # Use the UserSerializer for the 'created_by' field
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
