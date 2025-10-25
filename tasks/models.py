from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'برای انجام'),
        ('in_progress', 'در حال انجام'),
        ('review', 'در حال بررسی'),
        ('done', 'انجام شده'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    
    # فیلدهای جدید برای تقویم
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'done':
            return timezone.now() > self.due_date
        return False
    
    def days_until_due(self):
        from django.utils import timezone
        if self.due_date:
            delta = self.due_date - timezone.now()
            return delta.days
        return None
    
    class Meta:
        ordering = ['-created_at']
