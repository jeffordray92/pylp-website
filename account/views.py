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
from django.utils.html import format_html
from account.models import (
    Profile,
    EducationalBackground,
    School
)
from django.views import View
from content.models import ContactUsEmail, SignUpInstructions
from account.forms import (
    CommunityActivityForm,
    EducationalBackgroundForm,
    LogInForm,
    MembershipOrganizationForm,
    PersonalInformationForm,
    PhotoSignatureForm,
    SignupForm
)
from account.utils import token_generator
from dal import autocomplete
from django.db.models.signals import post_save
from django.dispatch import receiver


class SignupView(View):

    EducationalBackgroundFormSet = formset_factory(
        EducationalBackgroundForm, extra=1, max_num=4
    )
    MembershipOrganizationFormSet = formset_factory(
        MembershipOrganizationForm, extra=1, max_num=3
    )
    CommunityActivityFormSet = formset_factory(
        CommunityActivityForm, extra=1, max_num=3
    )

    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('index')

        education_formset = self.EducationalBackgroundFormSet(
            prefix='education'
        )
        membership_formset = self.MembershipOrganizationFormSet(
            prefix='membership'
        )
        activity_formset = self.CommunityActivityFormSet(
            prefix='activity'
        )
        return render(request, 'signup.html',
                      {'UserForm': SignupForm,
                       'InformationForm': PersonalInformationForm,
                       'EducationForm': education_formset,
                       'MembershipForm': membership_formset,
                       'CommunityForm': activity_formset})

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(request.POST)
        personal_information_form = PersonalInformationForm(request.POST)
        education_formset = self.EducationalBackgroundFormSet(
            request.POST, prefix='education')
        membership_formset = self.MembershipOrganizationFormSet(
            request.POST, prefix='membership')
        activity_formset = self.CommunityActivityFormSet(
            request.POST, prefix='activity')
        if user_form.is_valid() and personal_information_form.is_valid():
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
            for education_form in education_formset:
                education_form.save(profile=profile)
            for membership_form in membership_formset:
                membership_form.save(profile=profile)
            for activity_form in activity_formset:
                activity_form.save(profile=profile)

            email_subject = "PYLP Registration Email Confirmation"
            uidb64 = urlsafe_base64_encode(force_bytes(userform.pk))
            token = token_generator.make_token(userform)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token})
            activate_url = f'http://{domain}{link}'
            instruction = SignUpInstructions.objects.last()
            content = format_html(instruction.content)
            email_body = "Thank you for registering at PYLP Alumni Association, Inc.\n\nTo get started, activate your account by clicking the" \
                " below.\n" + activate_url
            email = EmailMessage(
                email_subject,
                email_body+content,
                'noreply@pylp.com',
                [user_form.cleaned_data['email']],
            )
            email.send(fail_silently=False)
            profile_pk = urlsafe_base64_encode(force_bytes(profile.pk))
            return redirect(reverse('photo-sig', kwargs={'pk': profile_pk}))
        else:
            return render(request, 'signup.html', {
                'UserForm': user_form,
                'InformationForm': personal_information_form,
                'EducationForm': education_formset,
                'MembershipForm': membership_formset,
                'CommunityForm': activity_formset})


class PhotoSignatureView(View):
    def get(self, request, pk, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('index')
        try:
            pk = force_text(urlsafe_base64_decode(pk))
            Profile.objects.get(pk=pk)
            return render(request, 'submit_photo_signature.html', {'photoSignatureForm': PhotoSignatureForm})
        except:
            return redirect('index')

    def post(self, request, pk, *args, **kwargs):
        photo_sig_form = PhotoSignatureForm(request.POST, request.FILES)
        if photo_sig_form.is_valid():
            pk = force_text(urlsafe_base64_decode(pk))
            profile = Profile.objects.get(pk=pk)
            if photo_sig_form.cleaned_data['photo']:
                profile.photo = photo_sig_form.cleaned_data['photo']
            if photo_sig_form.cleaned_data['e_sig']:
                profile.electronic_signature = photo_sig_form.cleaned_data['e_sig']
            profile.save()
        instruction = SignUpInstructions.objects.last()
        content = format_html(instruction.content)
        return render(request, 'activate_account.html', {'header': "How To Activate Your Account", 'instruction_content': content})


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
                        content = format_html(instruction.content)
                        return render(request, 'activate_account.html', {'header': "Your Account Isn't Activated Yet.",
                                                                         'instruction': instruction,
                                                                         'instruction_content': content})
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


def send_email(photo=None, e_sig=None):
    subject = ""
    body = ""
    contact_email = ""
    try:
        contact_email = ContactUsEmail.objects.first().email
    except:
        contact_email = ""
    if photo and e_sig:
        subject = "[Photo & E-Signature Update]"
        body = f"Updated Photo: {photo} \n\n Updated E-Signature: {e_sig}"
    elif photo:
        subject = "[Photo Update]"
        body = f"Updated Photo: {photo}"
    elif e_sig:
        subject = "[E-Signature Update]"
        body = f"Updated E-Signature: {e_sig}"

    email = EmailMessage(
        subject,
        body,
        'noreply@pylp.com',
        [contact_email],
    )
    email.send(fail_silently=False)


@receiver(post_save, sender=Profile)
def email_handler(sender, instance, **kwargs):
    if instance.is_dirty():
        dirty = instance.get_dirty_fields()
        try:
            if 'photo' in dirty and 'electronic_signature' in dirty:
                photo = "User removed photo"
                e_sig = "User removed photo"
                if instance.photo:
                    photo = instance.photo.url
                if instance.electronic_signature:
                    e_sig = instance.electronic_signature.url
                send_email(photo=photo, e_sig=e_sig)
            elif 'photo' in dirty:
                photo = "User removed photo"
                if instance.photo:
                    photo = instance.photo.url
                send_email(photo=photo)
            elif 'electronic_signature' in dirty:
                e_sig = "User removed photo"
                if instance.electronic_signature:
                    e_sig = instance.electronic_signature.url
                send_email(e_sig=e_sig)
        except:
            pass
