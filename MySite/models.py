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


class ExecutorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    skills = models.TextField(help_text="List of skills", blank=True)
    experience = models.TextField(help_text="Description of experience or info about you", blank=True)
    portfolio = models.TextField(help_text="Portfolio or projects links", blank=True)
    rating = models.FloatField(help_text="Average rating", default=0)


class Executor(CustomUser):
    class Meta:
        proxy = True

    def __str__(self):
        return f"Freelancer name: {self.username}"


class Customer(CustomUser):
    class Meta:
        proxy = True

    def __str__(self):
        return f"Customer name: {self.username}"


class Tasks(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100, help_text="Name of the task")
    description = models.TextField(help_text="Description of your task")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price")
    deadline = models.DateTimeField(help_text="Your deadline")

    def save(self, *args, **kwargs):
        if not isinstance(self.customer, Customer):
            raise ValueError("Only customers can create tasks.")
        super().save(*args, **kwargs)


class Chat(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="chats", help_text="Chat for this task")
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_chats')
    executor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='executor_chats')
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False, help_text="Is the chat open?")

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
    content = models.TextField(help_text="Message content"),
    timestamp = models.DateTimeField(help_text="Time when the message was send", default=now)
    is_read = models.BooleanField(default=False, help_text="Has the message been read?")

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id}"
