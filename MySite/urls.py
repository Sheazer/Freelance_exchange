from django.urls import path

from .views import register, home

app_name = "mysite"
urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
]
