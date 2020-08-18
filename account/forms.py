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


class PersonalInformationForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, label='First Name')
    last_name = forms.CharField(
        required=True, max_length=50, label='Last Name')
    nickname = forms.CharField(required=True, max_length=50, label='Nickname')
    birth_date = forms.DateField(required=True, label='Date of Birth', widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    birth_place = forms.CharField(
        required=True, max_length=50, label='Place of Birth')
    civil_status = forms.CharField(
        required=True, max_length=50, label='Civil Status')
    gender = forms.ChoiceField(
        required=True, choices=GENDER_CHOICES, label='Gender')
    pylp_batch = forms.IntegerField(
        required=True,  min_value=0, label='PYLP Batch')
    pylp_year = forms.ChoiceField(
        choices=year_choices, initial=current_year, label='PYLP Year')
    host_family = forms.CharField(
        required=True, max_length=50, label='Host Family')
    present_address = forms.CharField(
        required=True, max_length=150, label='Present Address')
    permanent_address = forms.CharField(required=True,
                                        max_length=150, label='Permanent Address')
    current_work_affiliation = forms.CharField(required=True,
                                               max_length=50, label='Current Work Affiliation')
    name_address_office_school = forms.CharField(required=True,
                                                 max_length=150, label='Name and Address of Office/School')
    ethnicity = forms.CharField(
        required=True, max_length=50, label='Ethnicity')
    religion = forms.CharField(required=True, max_length=50, label='Religion')
    facebook_account = forms.CharField(required=True, max_length=150)
    contact_number = PhoneNumberField(region="PH")
    telephone_number = PhoneNumberField(region="PH")


class EducationalBackgroundForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = EducationalBackground
        fields = '__all__'
        required = '__all__'
        exclude = ('account',)


class MembershipOrganizationForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = MembershipOrganization
        fields = '__all__'
        required = '__all__'
        exclude = ('account',)


class CommunityActivityForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = CommunityActivity
        fields = '__all__'
        required = '__all__'
        exclude = ('account',)


class LogInForm(forms.Form):
    user_name = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
