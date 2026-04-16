from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tovar, Zakaz, ZakazItem

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'FIO', 'Number', 'Address', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'FIO': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ФИО'}),
            'Number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'Address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'FIO', 'Number', 'Address', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'FIO': forms.TextInput(attrs={'class': 'form-control'}),
            'Number': forms.NumberInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class TovarForm(forms.ModelForm):
    class Meta:
        model = Tovar
        fields = ['Vid_tovara', 'Nomer_tovara', 'Prace', 'category', 'description']
        widgets = {
            'Vid_tovara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название товара'}),
            'Nomer_tovara': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите артикул'}),
            'Prace': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание товара'}),
        }

class ZakazForm(forms.ModelForm):
    class Meta:
        model = Zakaz
        fields = ['user', 'Sposob_oplati', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'Sposob_oplati': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }