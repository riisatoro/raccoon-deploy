from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Expectation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    issue = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expected_at = models.DateTimeField(null=False, blank=False)
    done_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}#{self.project}: {self.issue}"
