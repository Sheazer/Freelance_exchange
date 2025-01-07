from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.db.models import Q

from .forms import UserRegistrationForm, TaskCreateForm, UserEditForm, EditPortfolioForm, TaskFilterForm, CommentForm, \
    MessageForm
from .models import CustomUser, Task, ExecutorPortfolio, Comment, Chat, Message
from .decorators import role_required, anonymous_required


@method_decorator(anonymous_required, name='dispatch')
class UserLoginView(LoginView):
    template_name = "mysite/login.html"


# Представление выхода с аккаунта
def logout_view(request):
    logout(request)
    return redirect('mysite:login')


# Регистрация нового пользователя
@anonymous_required  # декоратор где ограничивает залогиненых юзеров
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mysite:home'))
        else:
            form = UserRegistrationForm()
            return render(request, 'mysite/register.html',
                          {'form': form, 'error': 'Wrong registrations!!!', })

    else:
        form = UserRegistrationForm()
        return render(request, 'mysite/register.html', {'form': form})


# обычный View для главной страницы
def home(request):
    users = CustomUser.objects.all()
    user = request.user
    return render(request, 'mysite/home.html', {'users': users, 'user': user})


# Представление создания нового задания
# Ограничения декораторов: залогоненый и только с ролью customer
@login_required
@role_required('customer')
def create_task(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.customer = request.user
            task.save()
            categories = form.cleaned_data.get('categories')
            task.categories.set(categories)
            return redirect(reverse('mysite:list_task'))
        else:
            form = TaskCreateForm()
            return render(request, 'mysite/create_task.html',
                          {'form': form, 'error': 'Wrong Task!!!', })
    else:
        form = TaskCreateForm()
        return render(request, 'mysite/create_task.html', {'form': form})


# Просмотр своих существуещих обьявлений customer
@login_required
@role_required('customer')
def list_task(request):
    tasks = Task.objects.filter(customer=request.user).order_by('-id')[:15]
    return render(request, 'mysite/list_task.html', {'tasks': tasks})


# Просмотр более детального просмотра одного Task
@login_required
def task_detail_view(request, pk, executor_id=None):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()

    if task.status == 'active':
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.task = task
                comment.executor = request.user
                comment.save()
                return redirect('mysite:detail_task', pk=pk)
            else:
                form = CommentForm()
            return render(request, 'mysite/detail_task.html', {'task': task, 'comments': comments, 'form': form,
                                                               'error': 'Wrong comment'})
        if request.user.is_executor():
            if comments.filter(executor=request.user).exists():
                return render(request, 'mysite/detail_task.html', {'task': task, 'comments': comments})
            else:
                form = CommentForm()
                return render(request, 'mysite/detail_task.html', {'task': task, 'comments': comments,
                                                                   'form': form})
        return render(request, 'mysite/detail_task.html', {'task': task, 'comments': comments})
    else:
        return render(request, 'mysite/detail_task.html', {'task': task})


# Нужен для того чтобы поменять статус тасков. Например если в процессе работы завершить
@login_required
def processing_task(request):
    task_id = request.POST.get('task_id')
    executor_id = request.POST.get('executor_id')

    task = Task.objects.get(id=task_id)
    executor = CustomUser.objects.get(id=executor_id)

    if request.user != task.customer:
        return HttpResponse('Вы не можете выбрать исполнителя для этой задачи.', status=403)

    if task.status == 'active':
        task.executor = executor
        task.status = 'in_progress'
        chat = Chat(customer=task.customer, executor=task.executor, task=task)
        chat.save()
        task.save()
    elif task.status == 'in_progress':
        task.status = 'completed'
        task.executor.executor_portfolio.completed_tasks += 1
        task.executor.executor_portfolio.save()
        task.save()

    return redirect('mysite:detail_task', pk=task_id)


# Представление для редакции профиля
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mysite:home')
        else:
            form = UserEditForm(instance=user)
            return render(request, 'mysite/edit_profile.html', {'form': form, 'error': 'Error form!'})
    else:
        form = UserEditForm(instance=user)
        return render(request, 'mysite/edit_profile.html', {'form': form})


# Просмотр профиля любого
def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    executor_profile = None

    if hasattr(user, "executor_portfolio"):
        executor_profile = user.executor_portfolio

    return render(request, 'mysite/profile.html', {'user': user, 'profile': executor_profile})


# Вывод списка фрилансеров
def freelancers_list(request):
    executors = CustomUser.objects.filter(role='executor')
    return render(request, 'mysite/freelancers.html', {'users': executors})


# Редактировать портофолио для Исполнителя и только
@login_required
@role_required('executor')
def edit_portfolio(request):
    if request.method == 'POST':
        form = EditPortfolioForm(request.POST)
        if form.is_valid():
            portfolio, created = ExecutorPortfolio.objects.update_or_create(
                user=request.user,
                defaults={
                    'skills': form.cleaned_data['skills'],
                    'experience': form.cleaned_data['experience'],
                    'portfolio': form.cleaned_data['portfolio'],
                }
            )
            portfolio.categories.set(form.cleaned_data['categories'])
            return redirect(reverse('mysite:profile', kwargs={'username': request.user.username}))
        else:
            form = EditPortfolioForm()
            return render(request, 'mysite/edit_portfolio.html',
                          {'form': form, 'error': 'Wrong Task!!!', })
    else:
        form = EditPortfolioForm()
        return render(request, 'mysite/edit_portfolio.html', {'form': form})


# Страница поиска любого задания на сайте
@login_required
def search_task(request):
    form = TaskFilterForm(request.GET)
    tasks = Task.objects.all()

    if form.is_valid():
        categories = form.cleaned_data.get('categories')
        if categories:
            tasks = tasks.filter(categories__in=categories).distinct()

        key_words = form.cleaned_data.get('key_words')
        if key_words:
            tasks = tasks.filter(key_words__icontains=key_words)

    return render(request, 'mysite/search_task.html', {'form': form, 'tasks': tasks})


# Выводим список переписок пользователя
@login_required
def dialog_list(request):
    chats = Chat.objects.filter(Q(customer=request.user) | Q(executor=request.user))[:20]
    if request.user.role == 'executor':
        role = 'executor'
    else:
        role = 'customer'
    return render(request, 'mysite/dialog_list.html', {'chats': chats, 'role': role})


# Крутая функция, горд собой! Выводит чат с связанным собеседником
@login_required
def dialog_view(request, chat_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = get_object_or_404(Chat, pk=chat_id)
            message.save()
    messages = Message.objects.filter(chat=chat_id).order_by('timestamp')[:20]
    form = MessageForm()
    return render(request, 'mysite/dialog_view.html', {'messages': messages, 'form': form, 'id': chat_id})
