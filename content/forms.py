from django import forms
from content.models import Account, Resource
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.forms import formset_factory
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
    gender = forms.CharField(required=True, max_length=50, label='Gender')
    batch_and_year = forms.CharField(
        required=True, max_length=50, label='PYLP Batch & Year')
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


class EducationalBackgroundForm(forms.Form):
    pass


class OrganizationMembershipForm(forms.Form):
    name = forms.CharField(
        required=True, max_length=50, label='Organization Name')


OrganizationMembershipFormset = formset_factory(
    OrganizationMembershipForm, extra=3)


class InvolvementForm(forms.Form):
    pass


class LogInForm(forms.Form):
    user_name = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class ResourceForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    image = forms.ImageField()
    attachments = forms.FileField(required=False,
                                  widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'attachment_tag'}))
