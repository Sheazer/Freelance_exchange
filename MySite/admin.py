from django.contrib import admin

from .models import CustomUser, Customer, Executor

admin.site.register(CustomUser)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
