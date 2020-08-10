from math import floor
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from content.models import Header, Section, Fact, Resource, ResourceListDetail, Account
from content.forms import SignupForm
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


class LoginView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})


class SignupView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {'UserForm': SignupForm})
         
    def post(self, request, *args, **kwargs):
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'{username} is created! Log in now.')
            return redirect('signup')
        else:
            return render(request, 'signup.html', {
                'UserForm': user_form,
            })
