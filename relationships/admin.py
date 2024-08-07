from django.contrib import admin
from .models import Relationship, Goal, Milestone

admin.site.register(Relationship)
admin.site.register(Goal)
admin.site.register(Milestone)