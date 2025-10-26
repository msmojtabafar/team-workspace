from django.contrib import admin
from .models import Attachment

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_type', 'file_size', 'project', 'task', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at', 'project']
    search_fields = ['file_name', 'description']
    readonly_fields = ['file_size', 'file_type', 'uploaded_at']
    
    def get_file_size_display(self, obj):
        return obj.get_file_size_display()
    get_file_size_display.short_description = 'حجم فایل'
