from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from projects.models import Project
from tasks.models import Task
from .models import Attachment
from .forms import ProjectAttachmentForm, TaskAttachmentForm

@login_required
def upload_project_attachment(request, project_id):
    """آپلود فایل برای پروژه"""
    project = get_object_or_404(Project, id=project_id, members=request.user)
    
    if request.method == 'POST':
        form = ProjectAttachmentForm(request.POST, request.FILES, request=request, project=project)
        if form.is_valid():
            attachment = form.save()
            messages.success(request, f'فایل "{attachment.file_name}" با موفقیت آپلود شد.')
            return redirect('project_detail', project_id=project_id)
    else:
        form = ProjectAttachmentForm(request=request, project=project)
    
    return render(request, 'attachments/upload_attachment.html', {
        'form': form,
        'project': project,
        'title': f'آپلود فایل برای پروژه: {project.title}'
    })

@login_required
def upload_task_attachment(request, task_id):
    """آپلود فایل برای تسک"""
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    
    # بررسی دسترسی کاربر به پروژه
    if not project.members.filter(id=request.user.id).exists():
        messages.error(request, 'شما دسترسی به این پروژه را ندارید.')
        return redirect('project_list')
    
    if request.method == 'POST':
        form = TaskAttachmentForm(request.POST, request.FILES, request=request, task=task)
        if form.is_valid():
            attachment = form.save()
            messages.success(request, f'فایل "{attachment.file_name}" با موفقیت آپلود شد.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskAttachmentForm(request=request, task=task)
    
    return render(request, 'attachments/upload_attachment.html', {
        'form': form,
        'task': task,
        'project': project,
        'title': f'آپلود فایل برای تسک: {task.title}'
    })

@login_required
def delete_attachment(request, attachment_id):
    """حذف فایل آپلود شده"""
    attachment = get_object_or_404(Attachment, id=attachment_id)
    
    # بررسی مالکیت یا دسترسی
    if attachment.uploaded_by != request.user and not request.user.is_staff:
        messages.error(request, 'شما اجازه حذف این فایل را ندارید.')
        return redirect('project_list')
    
    project_id = None
    if attachment.project:
        project_id = attachment.project.id
    elif attachment.task:
        project_id = attachment.task.project.id
    
    if request.method == 'POST':
        file_name = attachment.file_name
        attachment.delete()
        messages.success(request, f'فایل "{file_name}" با موفقیت حذف شد.')
        
        if project_id:
            return redirect('project_detail', project_id=project_id)
        else:
            return redirect('project_list')
    
    return render(request, 'attachments/delete_attachment.html', {
        'attachment': attachment
    })

@login_required
def download_attachment(request, attachment_id):
    """دانلود فایل"""
    attachment = get_object_or_404(Attachment, id=attachment_id)
    
    # بررسی دسترسی کاربر
    if attachment.project and not attachment.project.members.filter(id=request.user.id).exists():
        messages.error(request, 'شما دسترسی به این فایل را ندارید.')
        return redirect('project_list')
    
    if attachment.task and not attachment.task.project.members.filter(id=request.user.id).exists():
        messages.error(request, 'شما دسترسی به این فایل را ندارید.')
        return redirect('project_list')
    
    response = FileResponse(attachment.file.open(), as_attachment=True, filename=attachment.file_name)
    return response
