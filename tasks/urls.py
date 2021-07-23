from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('projects/',views.ProjectListView.as_view(), name = 'list_project'),
    path('projects/create',views.ProjectCreateView.as_view(), name = 'create_project'),
    path('projects/<str:pk>/updatename',views.ProjectUpdateView.as_view(), name = 'update_project'),
    path('projects/<str:pk>/delete', views.ProjectDeleteView.as_view(), name = 'delete_project'),
    path('projects/<str:pk>/tasks',views.TaskListView.as_view(), name= 'list_task'),
    path('projects/<str:pk>/tasks/create',views.TaskCreateView.as_view(), name='create_task'),
    path('projects/<str:pk>/tasks/<str:task_pk>/update',views.TaskUpdateView.as_view(), name = 'update_task')
    
    ]