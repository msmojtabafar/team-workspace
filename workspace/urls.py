from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('chat/', include('chat.urls')),
    path('attachments/', include('attachments.urls')),
    path('notifications/', include('notifications.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/dashboard/')),
]

# اضافه کردن مسیر media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
