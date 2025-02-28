# Generated by Django 5.1.4 on 2024-12-24 19:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0006_remove_executorportfolio_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_active',
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks_on_work', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('active', 'Активный'), ('inactive', 'Неактивный'), ('in_progress', 'В работе'), ('completed', 'Завершён')], default='active', help_text='status of task', max_length=20),
        ),
    ]
