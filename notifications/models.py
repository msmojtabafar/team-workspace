from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('task_assigned', 'تسک جدید'),
        ('task_updated', 'بروزرسانی تسک'),
        ('task_due', 'مهلت تسک'),
        ('task_completed', 'تسک تکمیل شده'),
        ('project_invite', 'دعوت به پروژه'),
        ('message', 'پیام جدید'),
        ('file_uploaded', 'فایل آپلود شده'),
        ('mention', 'اشاره به شما'),
        ('system', 'سیستمی'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'کم'),
        ('medium', 'متوسط'), 
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='کاربر')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='نوع اعلان')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium', verbose_name='اولویت')
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    
    # لینک‌های اختیاری
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, verbose_name='پروژه')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تسک')
    action_url = models.CharField(max_length=500, blank=True, verbose_name='لینک اقدام')
    
    # وضعیت
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_sent = models.BooleanField(default=False, verbose_name='ارسال شده')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ خواندن')
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """علامت‌گذاری به عنوان خوانده شده"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def get_icon(self):
        """آیکون مناسب برای نوع اعلان"""
        icons = {
            'task_assigned': '🎯',
            'task_updated': '✏️',
            'task_due': '⏰',
            'task_completed': '✅',
            'project_invite': '👥',
            'message': '💬',
            'file_uploaded': '📁',
            'mention': '👋',
            'system': '🔔',
        }
        return icons.get(self.notification_type, '🔔')
    
    def get_priority_color(self):
        """رنگ بر اساس اولویت"""
        colors = {
            'low': 'gray',
            'medium': 'blue', 
            'high': 'orange',
            'urgent': 'red',
        }
        return colors.get(self.priority, 'blue')
    
    def get_badge_color(self):
        """رنگ badge بر اساس اولویت"""
        colors = {
            'low': 'bg-gray-100 text-gray-800',
            'medium': 'bg-blue-100 text-blue-800',
            'high': 'bg-orange-100 text-orange-800',
            'urgent': 'bg-red-100 text-red-800',
        }
        return colors.get(self.priority, 'bg-blue-100 text-blue-800')

class NotificationManager:
    """مدیریت اعلان‌ها"""
    
    @staticmethod
    def create_notification(user, notification_type, title, message, priority='medium', 
                          project=None, task=None, action_url=''):
        """ایجاد اعلان جدید"""
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            project=project,
            task=task,
            action_url=action_url
        )
        
        # ارسال real-time notification از طریق WebSocket
        from .consumers import send_notification_to_user
        send_notification_to_user(user.id, notification)
        
        return notification
    
    @staticmethod
    def create_task_assigned_notification(task, assigned_to):
        """اعلان اختصاص تسک جدید"""
        return NotificationManager.create_notification(
            user=assigned_to,
            notification_type='task_assigned',
            title='تسک جدید به شما اختصاص داده شد',
            message=f'تسک "{task.title}" در پروژه "{task.project.title}" به شما اختصاص داده شد.',
            priority='high',
            project=task.project,
            task=task,
            action_url=f'/projects/{task.project.id}/'
        )
    
    @staticmethod
    def create_task_updated_notification(task, updated_by):
        """اعلان بروزرسانی تسک"""
        # برای تمام اعضای پروژه به جز کاربر بروزکننده
        members = task.project.members.exclude(id=updated_by.id)
        notifications = []
        
        for member in members:
            notification = NotificationManager.create_notification(
                user=member,
                notification_type='task_updated',
                title='تسک بروزرسانی شد',
                message=f'تسک "{task.title}" توسط {updated_by.username} بروزرسانی شد.',
                priority='medium',
                project=task.project,
                task=task,
                action_url=f'/projects/{task.project.id}/'
            )
            notifications.append(notification)
        
        return notifications
    
    @staticmethod
    def create_task_due_notification(task):
        """اعلان نزدیک شدن مهلت تسک"""
        if task.assigned_to:
            return NotificationManager.create_notification(
                user=task.assigned_to,
                notification_type='task_due',
                title='مهلت تسک نزدیک است',
                message=f'تسک "{task.title}" تا فردا باید تکمیل شود.',
                priority='high',
                project=task.project,
                task=task,
                action_url=f'/projects/{task.project.id}/'
            )
    
    @staticmethod
    def create_file_uploaded_notification(attachment, uploaded_by):
        """اعلان آپلود فایل جدید"""
        members = attachment.project.members.exclude(id=uploaded_by.id)
        notifications = []
        
        for member in members:
            notification = NotificationManager.create_notification(
                user=member,
                notification_type='file_uploaded',
                title='فایل جدید آپلود شد',
                message=f'فایل "{attachment.file_name}" توسط {uploaded_by.username} در پروژه "{attachment.project.title}" آپلود شد.',
                priority='medium',
                project=attachment.project,
                action_url=f'/projects/{attachment.project.id}/'
            )
            notifications.append(notification)
        
        return notifications
