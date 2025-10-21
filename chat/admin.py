from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'message', 'timestamp']
    list_filter = ['timestamp', 'project']
    search_fields = ['message', 'user__username']
