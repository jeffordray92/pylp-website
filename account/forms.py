from django import forms
from account.models import (
    CommunityActivity,
    current_year,
    EducationalBackground,
    EDUCATIONAL_TYPE,
    GENDER_CHOICES,
    MembershipOrganization,
    Profile,
    School,
    year_choices,)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class PersonalInformationForm(forms.ModelForm):
    birth_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    pylp_year = forms.ChoiceField(
        choices=year_choices, initial=current_year)
    contact_number = PhoneNumberField(region="PH")
    telephone_number = PhoneNumberField(region="PH")

    class Meta:
        model = Profile
        fields = '__all__'
        required = '__all__'
        exclude = ('user', 'is_verified', 'user_name', 'photo', 'electronic_signature',
                   'email', 'cluster', 'committees')

    def save(self, user, commit=True):
        profile = super(PersonalInformationForm, self).save(commit=False)
        profile.user = user
        profile.email = user.email
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
        widgets = {
            'school': autocomplete.ModelSelect2(url='school-autocomplete')
        }

    def save(self, commit=True, profile=None):
        education = super(EducationalBackgroundForm, self).save(commit=False)
        education.profile = profile
        if commit:
            education.save()
        return education


class MembershipOrganizationForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = MembershipOrganization
        fields = '__all__'
        required = '__all__'
        exclude = ('profile',)
        widgets = {
            'organization': autocomplete.ModelSelect2(url='organization-autocomplete')
        }

    def save(self, commit=True, profile=None):
        membership = super(MembershipOrganizationForm, self).save(commit=False)
        membership.profile = profile
        if commit:
            membership.save()
        return membership


class CommunityActivityForm(forms.ModelForm):
    inclusive_date = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = CommunityActivity
        fields = '__all__'
        required = '__all__'
        exclude = ('profile',)
        widgets = {
            'sponsor_organization': autocomplete.ModelSelect2(url='organization-autocomplete')
        }

    def save(self, commit=True, profile=None):
        activity = super(CommunityActivityForm, self).save(commit=False)
        activity.profile = profile
        if commit:
            activity.save()
        return activity


class LogInForm(forms.Form):
    user_name = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class PhotoSignatureForm(forms.Form):
    photo = forms.ImageField(required=False, label="2x2 with white background is encouraged.",
                             widget=forms.FileInput(attrs={'accept': ".png, .jpg", 'id': "photo_img"}))
    e_sig = forms.ImageField(required=False, label="Please sign it in a blank white paper using black marker.",
                             widget=forms.FileInput(attrs={'accept': ".png, .jpg", 'id': "esig_img"}))
