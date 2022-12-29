from django.contrib.auth.models import User
from rest_framework import serializers

from apps.todo.models import Expectation, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("name",)


class ExpectationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Expectation
        fields = (
            "user",
            "project",
            "issue",
            "created_at",
            "expected_at",
            "done_at",
        )
