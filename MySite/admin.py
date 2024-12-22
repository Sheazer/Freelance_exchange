from django.contrib import admin

from .models import CustomUser, ExecutorPortfolio, Category, Task

admin.site.register(CustomUser)

admin.site.register(Category)
admin.site.register(Task)


@admin.register(ExecutorPortfolio)
class Profile(admin.ModelAdmin):
    list_display = ['user', 'rating']
