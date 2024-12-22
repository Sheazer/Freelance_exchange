from django.urls import path
from django.contrib.auth import views

from .views import register, home, create_task, list_task, logout_view, task_detail_view, edit_profile, user_profile, freelancers_list

app_name = "mysite"
urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', views.LoginView.as_view(template_name="mysite/login.html"), name="login"),
    path('logout/', logout_view, name='logout'),
    path('project/create/', create_task, name='create_task'),
    path('project/list/', list_task, name='list_task'),
    path('project/view/<int:pk>/', task_detail_view, name='detail_task'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('freelancers/', freelancers_list, name='freelancers'),

    path('<str:username>/', user_profile, name='profile')
]
