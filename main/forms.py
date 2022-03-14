from django.contrib.auth.forms import UserCreationForm
from django import forms

from main.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agreement_checked = forms.BooleanField(
        label='Я принимаю условия соглашения',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CreateVotingForm(forms.Form):
    title = forms.CharField(
        label='Название голосования',
        required=True
    )
    description = forms.CharField(
        label='Описание голосования',
        required=True
    )
    type = forms.IntegerField(
        label='Тип голосования',
        min_value=1,
        max_value=3,
        required=True
    )


class EditVotingForm(forms.Form):
    title = forms.CharField(
        label='Название голосования',
        required=True
    )
    description = forms.CharField(
        label='Описание голосования',
        required=True
    )


class EditProfileForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        required=True
    )
    email = forms.CharField(
        label='Email',
        required=True
    )