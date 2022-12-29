from django.contrib import admin

from apps.todo.models import Expectation, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Expectation)
class ExpectationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "issue",
        "created_at",
        "expected_at",
        "done_at",
    )
