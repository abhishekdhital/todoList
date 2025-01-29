from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Task

class TaskList(ListView):
   model = Task
   context_object_name = 'tasks'     # OBJECT NAME IN HTML FILE IS NOW WRITTEN AS tasks
   template_name = 'task_list.html'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
