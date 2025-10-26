from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('project/<int:project_id>/upload/', views.upload_project_attachment, name='upload_project_attachment'),
    path('task/<int:task_id>/upload/', views.upload_task_attachment, name='upload_task_attachment'),
    path('<int:attachment_id>/delete/', views.delete_attachment, name='delete_attachment'),
    path('<int:attachment_id>/download/', views.download_attachment, name='download_attachment'),
]

# اضافه کردن مسیر media برای توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
