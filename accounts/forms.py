from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': False}))
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] == cd['password_2']:
            return cd['password']
        return forms.ValidationError('Password Mismatch')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
