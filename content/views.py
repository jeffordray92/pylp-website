from math import floor
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import (
    force_bytes,
    force_text
)
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from content.models import Header, Section, Fact, Resource, ResourceListDetail, Account
from content.forms import LogInForm, SignupForm
from content.utils import token_generator
from news.models import News


class HomeView(View):

    def get(self, request, *args, **kwargs):
        header_content = Header.objects.all().first()
        sections = Section.objects.all()
        recent_news = News.objects.filter(is_published=True)[:6]
        figures = Fact.objects.all().order_by('id')
        resources = Resource.objects.all()[:6]
        if figures.count() > 4:
            figures = figures[:int(4*floor(figures.count()/4.))]
        return render(request, 'index.html', {
            'header': header_content,
            'sections': sections,
            'recent_news': recent_news,
            'figures': figures,
            'resources': resources,
        })


class ResourceListView(View):

    def get(self, request, *args, **kwargs):
        details = ResourceListDetail.objects.last()
        resources = Resource.objects.all()
        return render(request, 'resource_list.html', {
            'resources': resources,
            'details': details,
        })


class ResourceView(View):

    def get(self, request, slug, *args, **kwargs):
        try:
            item = Resource.objects.get(slug=slug)
            return HttpResponseRedirect(item.file.url)
        except Exception as e:
            print(e)
            return HttpResponseNotFound('<h1>Resource not found</h1>')


class DirectoryView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            print('query')
        else:
            print('hello')
        return render(request, 'directory.html', {})


class SignupView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {'UserForm': SignupForm})

    def post(self, request, *args, **kwargs):
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            userform = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'])
            userform.set_password(
                user_form.cleaned_data['password1']
            )
            userform.is_active = False
            userform.save()
            email_subject = "PYLP Registration Email Confirmation"
            uidb64 = urlsafe_base64_encode(force_bytes(userform.pk)).decode()
            token = token_generator.make_token(userform)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token})
            activate_url = f'http://{domain}{link}'
            email_body = "Thank you for registering at PYLP Alumni Association, Inc.\n\nTo get started, activate your account by clicking the" \
                " below.\n" + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@pylp.com',
                [user_form.cleaned_data['email']],
            )
            email.send(fail_silently=False)
            signup_instructions = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ut turpis faucibus, pharetra diam quis, ultricies leo. Fusce tortor lectus, ultricies at nisi at, blandit egestas sem. Curabitur porttitor tempus justo vel semper. Vivamus sodales, eros lacinia vulputate rhoncus, tellus metus dapibus turpis, et malesuada massa nisl vitae ex. Nam rutrum congue dui, id bibendum nibh tincidunt et. Curabitur ipsum enim, laoreet vel venenatis sit amet, consectetur ut ipsum. In hac habitasse platea dictumst. Mauris sed vulputate nibh. Vivamus mi tellus, pellentesque ut convallis ut, facilisis vel nunc. Praesent vel dolor dictum, mattis sem in, dictum dui. Nullam ac purus dolor. Mauris libero nisl, vulputate id erat ac, egestas sagittis metus. Donec ipsum leo, gravida sed tellus non, commodo hendrerit elit. Vestibulum quis magna ante. Nullam ullamcorper egestas tincidunt."
            return render(request, 'base2.html', {'header': "How To Activate Your Account",
                                                  'content': signup_instructions})
        else:
            return render(request, 'signup.html', {
                'UserForm': user_form,
            })


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
        messages.success(request, "Account Activated successfully. You may log in now.",
                         extra_tags='register')
        return redirect('login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
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
                        signup_instructions = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam rutrum bibendum diam ac laoreet. Fusce eu urna sit amet elit mattis facilisis. Aenean eu risus scelerisque, dapibus risus id, iaculis dui. Cras et ornare lorem. Ut ultrices ornare diam sed facilisis. Curabitur et augue molestie, tristique magna eu, porta dui. Nulla ut eros metus. Morbi in sodales nisl. Mauris a augue scelerisque, maximus lacus non, ultricies odio. Morbi quam dui, euismod a tincidunt et, hendrerit sit amet ex."
                        return render(request, 'base2.html', {'header': "Your Account Isn't Activated Yet.",
                                                              'content': signup_instructions})
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
