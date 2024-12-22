from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, TaskCreateForm, UserEditForm
from .models import CustomUser, Task, ExecutorPortfolio


# User = get_user_model()


# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             # Аутентификация пользователя
#             user = authenticate(request, username=form['username'], password=form['password'])
#             if user is not None:
#                 # Сохранение пользователя в сессии
#                 login(request, user)
#                 return redirect('home')  # Перенаправляем на домашнюю страницу
#             else:
#                 form = UserLoginForm
#                 return render(request, '/mysite/login.html', {'form': form, 'error': 'Неверные данные для входа'})
#     form = UserLoginForm()
#     return render(request, 'mysite/login.html', {'form': form})
#

def logout_view(request):
    logout(request)
    return redirect('mysite:login')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mysite:home'))
        else:
            form = UserRegistrationForm()
            return render(request, 'mysite/register.html',
                          {'form': form, 'error': 'Wrong registrations!!!', })

    else:
        form = UserRegistrationForm()
        return render(request, 'mysite/register.html', {'form': form})


def home(request):
    users = CustomUser.objects.all()
    user = request.user
    return render(request, 'mysite/home.html', {'users': users, 'user': user})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.customer = request.user
            task.save()
            return redirect(reverse('mysite:list_task'))
        else:
            form = TaskCreateForm()
            return render(request, 'mysite/create_task.html',
                          {'form': form, 'error': 'Wrong Task!!!', })
    else:
        form = TaskCreateForm()
        return render(request, 'mysite/create_task.html', {'form': form})


@login_required
def list_task(request):
    tasks = Task.objects.filter(customer=request.user).order_by('-id')[:15]
    return render(request, 'mysite/list_task.html', {'tasks': tasks})


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'mysite/detail_task.html', {'task': task})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mysite:home')
        else:
            form = UserEditForm(instance=user)
            return render(request, 'mysite/edit_profile.html', {'form': form, 'error': 'Error form!'})
    else:
        form = UserEditForm(instance=user)
        return render(request, 'mysite/edit_profile.html', {'form': form})


def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'mysite/profile.html', {'user': user})


def freelancers_list(request):
    executors = CustomUser.objects.filter(role='executor')
    return render(request, 'mysite/freelancers.html', {'users': executors})



# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('customer', 'Customer'),
#         ('executor', 'Executor'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
#
#     def __str__(self):
#         return f"{self.username} ({self.get_role_display()})"
#
# class Customer(CustomUser):
#     class Meta:
#         proxy = True
#
#     def get_active_orders(self):
#         # Пример: логика получения активных заказов
#         return "Active orders for customer"
#
#
# class Executor(CustomUser):
#     class Meta:
#         proxy = True
#
#     def get_completed_tasks(self):
#         # Пример: логика получения выполненных задач
#         return "Completed tasks for executor"

# # Получить всех заказчиков
# customers = Customer.objects.filter(role='customer')
# for customer in customers:
#     print(customer.get_active_orders())
#
# # Получить всех исполнителей
# executors = Executor.objects.filter(role='executor')
# for executor in executors:
#     print(executor.get_completed_tasks())
