from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin  
# anywehre you put LoginRequiredMixin below we require to be loggedIn to access that data

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 

from .models import Task

class CustomLoginView(LoginView):
   template_name = 'base/login.html'
   fields = '__all__'
   redirect_authenticated_user = True

   def get_success_url(self):
       return reverse_lazy('tasks')

class RegisterPage(FormView):
   template_name = 'base/register.html'
   form_class = UserCreationForm
   redirect_authenticated_users= True
   success_url = reverse_lazy('tasks')

   def form_valid(self, form):
    user = form.save()
    if user is not None:
        login(self.request, user)
    return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
   model = Task
   context_object_name = 'tasks'     # OBJECT NAME IN HTML FILE IS NOW WRITTEN AS tasks

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['tasks'] = context['tasks'].filter(user=self.request.user)   # Filtering tasks by logged-in user
       context['count'] = context['tasks'].filter(complete=False).count()    # Count incomplete tasks
       return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task         # The model to be used for form creation
    fields = ['title', 'description', 'complete']   # Fields to be included in the form
    success_url= reverse_lazy('tasks')   # Redirects to 'tasks' after successful submission

    def form_valid(self, form):
       form.instance.user = self.request.user        # Assign the logged-in user to the task
       return super(TaskCreate, self).form_valid(form)    # Call the parent method to save the task


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task    
    fields = ['title', 'description', 'complete']   # Fields to be included in the form
    success_url= reverse_lazy('tasks')
     

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task    
    context_object_name = 'task'
    success_url= reverse_lazy('tasks')     
