# Generated by Django 5.1.4 on 2024-12-23 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0005_task_create_at_task_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='executorportfolio',
            name='rating',
        ),
        migrations.AddField(
            model_name='executorportfolio',
            name='completed_tasks',
            field=models.IntegerField(default=0, help_text='Likes rating'),
        ),
        migrations.AddField(
            model_name='executorportfolio',
            name='dislike',
            field=models.IntegerField(default=0, help_text='Likes rating'),
        ),
        migrations.AddField(
            model_name='executorportfolio',
            name='like',
            field=models.IntegerField(default=0, help_text='Likes rating'),
        ),
        migrations.AlterField(
            model_name='task',
            name='categories',
            field=models.ManyToManyField(default='Not have categories', related_name='task_category', to='MySite.category'),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Is the task done?'),
        ),
    ]