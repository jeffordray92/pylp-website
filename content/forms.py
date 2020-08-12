from django import forms
from content.models import Account, Resource
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "password1", "password2")


class LogInForm(forms.Form):
    user_name = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class ResourceForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    image = forms.ImageField()
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'attachment_tag'}))
