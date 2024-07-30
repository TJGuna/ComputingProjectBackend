from django.contrib import admin

from project.models import Task, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)