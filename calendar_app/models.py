from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task

class CalendarEvent:
    """کلاس برای مدیریت رویدادهای تقویم"""
    
    def __init__(self, user):
        self.user = user
    
    def get_user_tasks_as_events(self):
        """گرفتن تمام تسک‌های کاربر به عنوان رویداد"""
        projects = Project.objects.filter(members=self.user)
        tasks = Task.objects.filter(project__in=projects)
        
        events = []
        for task in tasks:
            if task.due_date:
                event = {
                    'id': task.id,
                    'title': task.title,
                    'start': task.due_date.isoformat(),
                    'end': task.due_date.isoformat(),
                    'color': self.get_task_color(task),
                    'project': task.project.title,
                    'status': task.status,
                    'priority': task.priority,
                    'url': f'/projects/{task.project.id}/',
                }
                events.append(event)
        return events
    
    def get_task_color(self, task):
        """تعیین رنگ بر اساس وضعیت و اولویت تسک"""
        if task.status == 'done':
            return '#10B981'  # سبز
        elif task.is_overdue():
            return '#EF4444'  # قرمز
        elif task.priority == 'high':
            return '#DC2626'  # قرمز تیره
        elif task.priority == 'medium':
            return '#F59E0B'  # نارنجی
        else:
            return '#3B82F6'  # آبی
    
    def get_upcoming_tasks(self, days=7):
        """تسک‌های آینده در روزهای مشخص"""
        from django.utils import timezone
        from datetime import timedelta
        
        projects = Project.objects.filter(members=self.user)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=days)
        
        return Task.objects.filter(
            project__in=projects,
            due_date__range=[start_date, end_date]
        ).order_by('due_date')
    
    def get_today_tasks(self):
        """تسک‌های امروز"""
        from django.utils import timezone
        from datetime import datetime, time
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        projects = Project.objects.filter(members=self.user)
        return Task.objects.filter(
            project__in=projects,
            due_date__range=[today_start, today_end]
        ).order_by('due_date')
