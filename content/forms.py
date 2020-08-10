from django import forms
from content.models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user_account = Account(
                user=user,
                user_name=user.username,
                email=user.email,
                is_verified=False
            )
            user_account.save()
        return user