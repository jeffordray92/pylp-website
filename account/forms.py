from django import forms
from account.models import (
    Profile,
    current_year,
    EducationalBackground,
    EDUCATIONAL_TYPE,
    GENDER_CHOICES,
    MembershipOrganization,
    CommunityActivity,
    year_choices,)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class PersonalInformationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50, label='First Name')
    last_name = forms.CharField(
        required=True, max_length=50, label='Last Name')
    birth_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    pylp_year = forms.ChoiceField(
        choices=year_choices, initial=current_year)
    contact_number = PhoneNumberField(region="PH")
    telephone_number = PhoneNumberField(region="PH")

    class Meta:
        model = Profile
        fields = ('first_name',
                  'last_name',
                  'birth_date',
                  'birth_place',
                  'civil_status',
                  'gender',
                  'pylp_batch',
                  'pylp_year',
                  'host_family',
                  'present_address',
                  'permanent_address',
                  'current_work_affiliation',
                  'name_address_office_school',
                  'ethnicity',
                  'religion',
                  'facebook_account',
                  'contact_number',
                  'telephone_number',)
        required = '__all__'
        exclude = ('user', 'is_verified', 'user_name', 'email', 'full_name')

    def save(self, commit=True, user=None):
        profile = super(PersonalInformationForm, self).save(commit=False)
        profile.user = user
        profile.email = user.email
        profile.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            profile.save()
        return profile


class EducationalBackgroundForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = EducationalBackground
        fields = '__all__'
        required = '__all__'
        exclude = ('profile',)


class MembershipOrganizationForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = MembershipOrganization
        fields = '__all__'
        required = '__all__'
        exclude = ('profile',)


class CommunityActivityForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = CommunityActivity
        fields = '__all__'
        required = '__all__'
        exclude = ('profile',)


class LogInForm(forms.Form):
    user_name = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
