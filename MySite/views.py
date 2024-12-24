from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm, TaskCreateForm, UserEditForm, EditPortfolioForm, TaskFilterForm
from .models import CustomUser, Task, ExecutorPortfolio
from .decorators import role_required, anonymous_required


@method_decorator(anonymous_required, name='dispatch')
class UserLoginView(LoginView):
    template_name = "mysite/login.html"


def logout_view(request):
    logout(request)
    return redirect('mysite:login')


@anonymous_required
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


def home(request):
    users = CustomUser.objects.all()
    user = request.user
    return render(request, 'mysite/home.html', {'users': users, 'user': user})


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


@login_required
@role_required('customer')
def list_task(request):
    tasks = Task.objects.filter(customer=request.user).order_by('-id')[:15]
    return render(request, 'mysite/list_task.html', {'tasks': tasks})


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'mysite/detail_task.html', {'task': task})


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


def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    executor_profile = None

    if hasattr(user, "executor_portfolio"):
        executor_profile = user.executor_portfolio

    return render(request, 'mysite/profile.html', {'user': user, 'profile': executor_profile})


def freelancers_list(request):
    executors = CustomUser.objects.filter(role='executor')
    return render(request, 'mysite/freelancers.html', {'users': executors})


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
