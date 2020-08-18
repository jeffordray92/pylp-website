from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import formset_factory
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import (
    force_bytes,
    force_text
)
from django.urls import reverse
from account.models import (
    Profile,
    EducationalBackground,
    School
)
from django.views import View
from content.models import SignUpInstructions
from account.forms import (
    CommunityActivityForm,
    EducationalBackgroundForm,
    LogInForm,
    MembershipOrganizationForm,
    PersonalInformationForm,
    SignupForm
)
from account.utils import token_generator
from dal import autocomplete


class SignupView(View):

    EducationalBackgroundFormSet = formset_factory(
        EducationalBackgroundForm, extra=1, max_num=4)

    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('index')

        education_formset = self.EducationalBackgroundFormSet(
            prefix='education')
        return render(request, 'signup.html',
                      {'UserForm': SignupForm,
                       'InformationForm': PersonalInformationForm,
                       'EducationForm': education_formset,
                       'MembershipForm': MembershipOrganizationForm,
                       'CommunityForm': CommunityActivityForm})

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(request.POST)
        personal_information_form = PersonalInformationForm(request.POST)
        education_formset = self.EducationalBackgroundFormSet(
            request.POST, prefix='education')
        #membership_form = MembershipOrganizationForm(request.POST)
        #community_form = CommunityActivityForm(request.POST)
        if user_form.is_valid() and personal_information_form.is_valid() and education_formset.is_valid():
            userform = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                first_name=personal_information_form.cleaned_data['first_name'],
                last_name=personal_information_form.cleaned_data['last_name'],
                email=user_form.cleaned_data['email'])
            userform.set_password(
                user_form.cleaned_data['password1']
            )
            userform.is_active = False
            userform.save()
            profile = personal_information_form.save(user=userform)
            for educ_form in education_formset:
                educ_form.save(profile=profile)

            email_subject = "PYLP Registration Email Confirmation"
            uidb64 = urlsafe_base64_encode(force_bytes(userform.pk))
            token = token_generator.make_token(userform)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token})
            activate_url = f'http://{domain}{link}'
            instruction = SignUpInstructions.objects.last()
            email_body = "Thank you for registering at PYLP Alumni Association, Inc.\n\nTo get started, activate your account by clicking the" \
                " below.\n" + activate_url
            email = EmailMessage(
                email_subject,
                email_body+instruction.content,
                'noreply@pylp.com',
                [user_form.cleaned_data['email']],
            )
            email.send(fail_silently=False)
            return render(request, 'activate_account.html', {'header': "How To Activate Your Account",
                                                             'content': instruction})
        else:
            return render(request, 'signup.html', {
                'UserForm': user_form,
                'InformationForm': personal_information_form,
                'EducationForm': education_formset})


class VerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uidb64 = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uidb64)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            account = Profile.objects.get(user_name=user.username)
            account.is_verified = True
            account.save()

        messages.success(request, "Account Activated successfully. You may log in now.",
                         extra_tags='register')
        return redirect('login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('index')
        return render(request, 'login.html', {'loginForm': LogInForm})

    def post(self, request, *args, **kwargs):
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['user_name'],
                password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                not_active = User.objects.filter(
                    username=login_form.cleaned_data['user_name']).first()
                if(not_active):
                    if(not_active.is_active == False):
                        instruction = SignUpInstructions.objects.last()
                        return render(request, 'activate_account.html', {'header': "Your Account Isn't Activated Yet.",
                                                                         'content': instruction})
                    else:
                        messages.error(request, "Incorrect credentials.")
                        return render(request, 'login.html', {
                            'loginForm': login_form,
                        })
                else:
                    messages.error(request, "Incorrect credentials.")
                    return render(request, 'login.html', {
                        'loginForm': login_form,
                    })
        else:
            return render(request, 'login.html', {
                'loginForm': login_form,
            })
