from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task
from datetime import datetime, timedelta

class ProjectStats:
    """کلاس برای محاسبه آمار پروژه"""
    
    def __init__(self, user):
        self.user = user
    
    def get_user_projects(self):
        return Project.objects.filter(members=self.user)
    
    def get_total_projects(self):
        return self.get_user_projects().count()
    
    def get_active_projects(self):
        return self.get_user_projects().filter(status='active').count()
    
    def get_completed_projects(self):
        return self.get_user_projects().filter(status='completed').count()
    
    def get_total_tasks(self):
        projects = self.get_user_projects()
        return Task.objects.filter(project__in=projects).count()
    
    def get_task_stats(self):
        projects = self.get_user_projects()
        tasks = Task.objects.filter(project__in=projects)
        
        return {
            'todo': tasks.filter(status='todo').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'done': tasks.filter(status='done').count(),
        }
    
    def get_recent_activity(self):
        """فعالیت‌های اخیر"""
        projects = self.get_user_projects()
        recent_tasks = Task.objects.filter(
            project__in=projects
        ).order_by('-created_at')[:10]
        
        return recent_tasks
    
    def get_priority_stats(self):
        projects = self.get_user_projects()
        tasks = Task.objects.filter(project__in=projects)
        
        return {
            'high': tasks.filter(priority='high').count(),
            'medium': tasks.filter(priority='medium').count(),
            'low': tasks.filter(priority='low').count(),
        }
