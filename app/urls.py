from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (signup_successful, signup, dashboard, redirect_after_login, 
                    CreateTaskView, DeleteTaskView, UpdateTaskView, TaskDetailView)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('redirect', redirect_after_login, name='redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sucess', signup_successful, name='signup_successful'),
    path('dashboard/<int:account_id>/', dashboard, name='dashboard'),
    path('dashboard/<int:account_id>/task_detail/<int:pk>', TaskDetailView, name='task_detail'),
    path('dashboard/<int:account_id>/add_task/', CreateTaskView, name='add_task'),
    path('dashboard/<int:account_id>/delete_task/<int:pk>', DeleteTaskView, name='delete_task'),
    path('dashboard/<int:account_id>/update_task/<int:pk>', UpdateTaskView, name='update_task'),

]