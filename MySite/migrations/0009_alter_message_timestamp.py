# Generated by Django 5.1.4 on 2024-12-26 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0008_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, help_text='Time when the message was send'),
        ),
    ]
