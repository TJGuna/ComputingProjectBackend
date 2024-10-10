# important_dates/admin.py
from django.contrib import admin
from .models import ImportantDate

@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('date', 'user')