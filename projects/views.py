from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from tasks.models import Task

@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, members=request.user)
    tasks = project.tasks.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Task.objects.create(
                title=title,
                description=description,
                project=project,
                created_by=request.user
            )
            return redirect('project_detail', project_id=project_id)
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks
    })
