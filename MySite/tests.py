from django.test import TestCase
from datetime import datetime

from MySite.models import Task, CustomUser


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create(username='TestUser')
        self.assertEqual(user.username, 'TestUser')


class TaskModelTest(TestCase):
    def test_create_task(self):
        user = CustomUser.objects.create(username='TestUser')
        task = Task.objects.create(customer=user, title='Test title1', description='Description test', price=100, deadline=datetime.now())
        self.assertEqual(task.title, 'Test title1')
        self.assertEqual(Task.objects.count(), 1)


class
