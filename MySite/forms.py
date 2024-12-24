from django import forms
from .models import CustomUser, Task, Category, ExecutorPortfolio
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']


class TaskCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    deadline = forms.DateField(
        widget=forms.SelectDateWidget(),  # Виджет для выбора даты
        required=True
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Введите цену', 'step': '0.01', 'min': '0', 'style': 'text-align:right;'}),
        required=True
    )

    class Meta:
        model = Task
        fields = ['categories', 'key_words', 'title', 'description', 'price', 'deadline']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email' ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditPortfolioForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Все категории из базы данных
        widget=forms.CheckboxSelectMultiple,  # Виджет для множественного выбора
        required=False  # Поле не обязательно
    )

    class Meta:
        model = ExecutorPortfolio
        fields = ['categories', 'skills', 'experience', 'portfolio']


class TaskFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    key_words = forms.CharField(max_length=100, required=False)
