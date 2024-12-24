from django.urls import path
from django.contrib.auth import views

from .views import register, home, create_task, list_task, logout_view, task_detail_view, edit_profile, user_profile, freelancers_list
from .views import UserLoginView, edit_portfolio, search_task

app_name = "mysite"
urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path('project/create/', create_task, name='create_task'),
    path('project/list/', list_task, name='list_task'),
    path('project/view/<int:pk>/', task_detail_view, name='detail_task'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('freelancers/', freelancers_list, name='freelancers'),
    path('edit/portfolio/', edit_portfolio, name='edit_portfolio'),
    path('project/search/', search_task, name='project_search'),
    path('<str:username>/', user_profile, name='profile'),
]
