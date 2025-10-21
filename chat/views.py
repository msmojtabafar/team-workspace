from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project

@login_required
def chat_room(request, project_id):
    project = get_object_or_404(Project, id=project_id, members=request.user)
    return render(request, 'chat/chat_room.html', {'project': project})
