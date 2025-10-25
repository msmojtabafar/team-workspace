from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CalendarEvent

@login_required
def calendar_view(request):
    """صفحه اصلی تقویم"""
    return render(request, 'calendar/calendar.html')

@login_required
def calendar_events(request):
    """API برای گرفتن رویدادهای تقویم"""
    calendar = CalendarEvent(request.user)
    events = calendar.get_user_tasks_as_events()
    return JsonResponse(events, safe=False)

@login_required
def upcoming_tasks(request):
    """تسک‌های آینده"""
    calendar = CalendarEvent(request.user)
    days = request.GET.get('days', 7)
    tasks = calendar.get_upcoming_tasks(int(days))
    
    context = {
        'tasks': tasks,
        'days': days,
    }
    return render(request, 'calendar/upcoming_tasks.html', context)

@login_required
def today_tasks(request):
    """تسک‌های امروز"""
    calendar = CalendarEvent(request.user)
    tasks = calendar.get_today_tasks()
    
    context = {
        'tasks': tasks,
    }
    return render(request, 'calendar/today_tasks.html', context)
