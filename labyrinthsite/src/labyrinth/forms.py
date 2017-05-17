from django import forms
from django.contrib.auth.models import User
from labyrinth.models import MyUser
import re

CHOICES = (('male', 'Мужской'), ('female', 'Женский'))

class RegistrationForm(forms.Form):
    username = forms.CharField(
        required=True, label='Логин: ', widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    email = forms.EmailField(
        required=True, max_length=100, label="E-mail: ", widget=forms.TextInput(attrs={'placeholder': 'Введите E-mail'}))
    first_name = forms.CharField(
        required=True, max_length=30, label='Имя: ', widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(), 
        required=True, max_length=30, label="Пароль: ")
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30)),
        label="Повторите: ")
    phone = forms.CharField(
        required=True, label='Телефон: ', 
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}))
    age = forms.IntegerField(
        required=True, label='Возраст: ', 
        widget=forms.NumberInput(attrs={'placeholder': 'Введите количество полных лет'}))
    gender = forms.ChoiceField(required=True, label="Пол: ", widget=forms.RadioSelect, choices=CHOICES)
    

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('Этот логин занят')

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError('Этот e-mail занят')

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data
