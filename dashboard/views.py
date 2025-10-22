from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProjectStats

@login_required
def dashboard(request):
    stats = ProjectStats(request.user)
    
    context = {
        'total_projects': stats.get_total_projects(),
        'active_projects': stats.get_active_projects(),
        'completed_projects': stats.get_completed_projects(),
        'total_tasks': stats.get_total_tasks(),
        'task_stats': stats.get_task_stats(),
        'recent_activity': stats.get_recent_activity(),
        'priority_stats': stats.get_priority_stats(),
    }
    
    return render(request, 'dashboard/dashboard.html', context)
