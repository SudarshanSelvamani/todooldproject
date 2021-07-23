from django.db.models.base import Model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, View
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.urls import reverse

# Create your views here.

class ProjectListView(ListView):
    template_name = 'tasks/project_list_view.html'
    model = Project
    context_object_name = 'projects'


class ProjectCreateView(View):
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_project')
        return render(request, 'tasks/create_project_view.html', {'form': form})

    def get(self, request):
        form = ProjectForm()
        return render(request, 'tasks/create_project_view.html', {'form': form})


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('name', )
    template_name = 'tasks/edit_project_view.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'project'

    def form_valid(self, form):
        project = form.save()
        return redirect('tasks:list_project',)


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('tasks:list_project')
    template_name = 'tasks/delete_project_view.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'project'


class TaskListView(ListView):
    template_name = 'tasks/tasks_list_view.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(project = self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return context

class TaskCreateView(View):
    def post(self, request, pk):
        self.project = get_object_or_404(Project, pk = pk)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = self.project
            task.save()
            return redirect(reverse('tasks:list_task',kwargs={'pk':self.project.pk}))
        return render(request, 'tasks/create_task_view.html', {'form': form, 'project_pk':pk})

    def get(self, request,pk):
        form = TaskForm()
        return render(request, 'tasks/create_task_view.html', {'form': form, 'project_pk':pk})

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task_view.html'
    pk_url_kwarg = 'task_pk'
    context_object_name = 'task'

    def form_valid(self, form):
        task = form.save()
        return redirect(reverse('tasks:list_task',kwargs={'pk': task.project.pk}))


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete_task_view.html'
    pk_url_kwarg = 'task_pk'
    context_object_name = 'task'

    def get_success_url(self, **kwargs):
        return reverse_lazy('tasks:list_task',kwargs={'pk':self.object.project.pk,})