from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserRegistrationForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mysite:home'))
        else:
            form = UserRegistrationForm()
            return render(request,'mysite/register.html',
                          {'form': form, 'error': 'Wrong registrations!!!', })

    else:
        form = UserRegistrationForm()
        return render(request,'mysite/register.html', {'form': form})


def home(request):
    users = CustomUser.objects.all()
    return render(request, 'mysite/home.html', {'users': users, })



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