# guides/admin.py
from django.contrib import admin
from .models import Guide

class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at', 'author')

admin.site.register(Guide, GuideAdmin)