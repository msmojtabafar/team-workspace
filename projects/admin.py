from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
