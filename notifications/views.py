from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notification

@login_required
def notification_list(request):
    """لیست اعلان‌های کاربر"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    # علامت‌گذاری اعلان‌ها به عنوان ارسال شده
    Notification.objects.filter(user=request.user, is_sent=False).update(is_sent=True)
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    })

@login_required
@require_http_methods(["POST"])
def mark_as_read(request, notification_id):
    """علامت‌گذاری اعلان به عنوان خوانده شده"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["POST"])
def mark_all_as_read(request):
    """علامت‌گذاری تمام اعلان‌ها به عنوان خوانده شده"""
    Notification.objects.filter(user=request.user, is_read=False).update(
        is_read=True, 
        read_at=timezone.now()
    )
    
    return JsonResponse({'success': True})

@login_required
def get_unread_count(request):
    """گرفتن تعداد اعلان‌های خوانده نشده"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

@login_required
def notification_dropdown(request):
    """دریافت اعلان‌ها برای dropdown"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'icon': notification.get_icon(),
            'priority': notification.priority,
            'priority_color': notification.get_priority_color(),
            'badge_color': notification.get_badge_color(),
            'created_at': notification.created_at.strftime('%H:%M'),
            'is_read': notification.is_read,
            'action_url': notification.action_url or '#',
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    })
