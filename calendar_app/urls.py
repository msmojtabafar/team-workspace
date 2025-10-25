from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events/', views.calendar_events, name='calendar_events'),
    path('upcoming/', views.upcoming_tasks, name='upcoming_tasks'),
    path('today/', views.today_tasks, name='today_tasks'),
]
