from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('executor', 'Executor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Устанавливаем уникальное имя для связи
        blank=True
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Уникальное имя для связи
        blank=True
    )

    def is_customer(self):
        return self.role == 'customer'

    def is_executor(self):
        return self.role == 'executor'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ExecutorPortfolio(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="executor_portfolio")
    skills = models.CharField(max_length=100, help_text="List of skills", blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="categories_sk")
    experience = models.TextField(help_text="Description of experience or info about you", blank=True)
    portfolio = models.TextField(help_text="Portfolio or projects links", blank=True)
    like = models.IntegerField(help_text="Likes rating", default=0)
    dislike = models.IntegerField(help_text="Likes rating", default=0)
    completed_tasks = models.IntegerField(help_text="Likes rating", default=0)


class CustomerPortfolio(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_portfolio')


class Task(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('inactive', 'Неактивный'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершён'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks_on_work", null=True)
    categories = models.ManyToManyField(Category, default="Not have categories", related_name="task_category")
    key_words = models.CharField(max_length=50, help_text='specialization')
    title = models.CharField(max_length=100, help_text="Name of the task")
    description = models.TextField(help_text="Description of your task")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price")
    deadline = models.DateTimeField(help_text="Your deadline")
    create_at = models.DateTimeField(auto_now_add=True, help_text='Created time')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="status of task"
    )


class Chat(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_chats", help_text="Chat for this task")
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_chats')
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='executor_chats')
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Is the chat open?")

    def __str__(self):
        return f"Chat with {self.customer}(customer) and {self.executor}(executor)"


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Chat to which this message belongs",
    )
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sender",
        help_text="User who sent the message",
    )
    content = models.TextField(help_text="Message content")
    timestamp = models.DateTimeField(help_text="Time when the message was send", auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text="Has the message been read?")

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id}"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=200, help_text="type your text")
    offer = models.IntegerField(default=0, help_text="Your proposal")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['task', 'executor'], name='unique_task_executor_comment')
        ]
