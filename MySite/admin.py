from django.contrib import admin

from .models import CustomUser, ExecutorPortfolio, Category, Task

admin.site.register(CustomUser)

admin.site.register(Category)


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ['title', 'create_at']


@admin.register(ExecutorPortfolio)
class Profile(admin.ModelAdmin):
    list_display = ['user', 'completed_tasks']
