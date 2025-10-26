from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task
import os
from uuid import uuid4

def attachment_upload_path(instance, filename):
    """تعیین مسیر ذخیره‌سازی فایل‌ها"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    
    if instance.task:
        return f'attachments/tasks/{instance.task.id}/{filename}'
    elif instance.project:
        return f'attachments/projects/{instance.project.id}/{filename}'
    else:
        return f'attachments/general/{filename}'

class Attachment(models.Model):
    FILE_TYPES = [
        ('document', 'سند'),
        ('image', 'تصویر'),
        ('archive', 'آرشیو'),
        ('code', 'کد'),
        ('other', 'سایر'),
    ]
    
    file = models.FileField(upload_to=attachment_upload_path, verbose_name='فایل')
    file_name = models.CharField(max_length=255, verbose_name='نام فایل')
    file_size = models.BigIntegerField(verbose_name='حجم فایل')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, verbose_name='نوع فایل')
    
    # ارتباط با پروژه یا تسک (یکی از این دو باید پر شود)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='attachments', verbose_name='پروژه')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='attachments', verbose_name='تسک')
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='آپلود شده توسط')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپلود')
    
    def save(self, *args, **kwargs):
        """ذخیره اطلاعات فایل قبل از ذخیره مدل"""
        if self.file:
            if not self.file_name:
                self.file_name = os.path.basename(self.file.name)
            self.file_size = self.file.size
            
            # تشخیص نوع فایل
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
                self.file_type = 'document'
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
                self.file_type = 'image'
            elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                self.file_type = 'archive'
            elif ext in ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']:
                self.file_type = 'code'
            else:
                self.file_type = 'other'
        
        super().save(*args, **kwargs)
    
    def get_file_icon(self):
        """آیکون مناسب برای نوع فایل"""
        icons = {
            'document': '📄',
            'image': '🖼️',
            'archive': '📦',
            'code': '💻',
            'other': '📎',
        }
        return icons.get(self.file_type, '📎')
    
    def get_file_size_display(self):
        """نمایش خوانا از حجم فایل"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        elif self.file_size < 1024 * 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.file_size / (1024 * 1024 * 1024):.1f} GB"
    
    def __str__(self):
        return self.file_name
    
    class Meta:
        verbose_name = 'ضمیمه'
        verbose_name_plural = 'ضمیمه‌ها'
        ordering = ['-uploaded_at']
