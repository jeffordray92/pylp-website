from math import floor
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from content.models import (
    Attachment,
    ContactUsEmail,
    Fact,
    Header,
    Resource,
    ResourceListDetail,
    Section,
    SignUpInstructions)

from content.forms import (
    ContactUsForm,
    ResourceForm,
)
from news.models import News


class HomeView(View):

    def get(self, request, *args, **kwargs):
        header_content = Header.objects.all().first()
        sections = Section.objects.all()
        recent_news = News.objects.filter(
            is_published=True).order_by('-date_published')[:6]
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
        if(request.user.is_authenticated == False):
            return redirect('index')
        details = ResourceListDetail.objects.last()
        resources = Resource.objects.all()
        return render(request, 'resource_list.html', {
            'resources': resources,
            'details': details,
        })


class ResourceView(View):

    def get(self, request, slug, *args, **kwargs):
        if(request.user.is_authenticated == False):
            return redirect('index')
        try:
            details = ResourceListDetail.objects.last()
            resource = Resource.objects.get(slug=slug)
            attachments = list(Attachment.objects.filter(resource=resource))
            return render(request, 'resource.html', {
                'resource': resource,
                'attachments': attachments,
                'details': details,
            })
        except Exception as e:
            print(e)
            return HttpResponseNotFound('<h1>Resource not found</h1>')


class SubmitResourceView(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_staff == False):
            return redirect('index')
        details = ResourceListDetail.objects.last()
        return render(request, 'submit_resource.html', {'ResourceForm': ResourceForm, 'details': details})

    def post(self, request, *args, **kwargs):
        resource_form = ResourceForm(request.POST, request.FILES)
        if resource_form.is_valid():
            files = request.FILES.getlist('attachments')
            resource = Resource(
                title=resource_form.cleaned_data['title'],
                description=resource_form.cleaned_data['description'],
                image=request.FILES['image'])
            resource.save()
            for f in files:
                attachment = Attachment(
                    resource=resource,
                    file=f
                )
                attachment.save()

            return redirect('resource_list')
        else:
            return render(request, 'submit_resource.html', {'ResourceForm': resource_form})


class DirectoryView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            print('query')
        else:
            print('hello')
        return render(request, 'directory.html', {})


class ContactUsView(View):

    def get(self, request, *args, **kwargs):
        name = ""
        email = ""
        try:
            name = request.user.first_name
            email = request.user.email
        except:
            pass

        contact_form = ContactUsForm(
            initial={
                'name': name,
                'email': email
            }
        )
        return render(request, 'contact_us.html', {'contactForm': contact_form})

    def post(self, request, *args, **kwargs):
        contact_email = ""
        try:
            contact_email = ContactUsEmail.objects.first().email
        except:
            contact_email = ""
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            email_subject = contact_form.cleaned_data['subject']
            email_body = contact_form.cleaned_data['message']
            email_sender = f"Sender Name: {name}\n\n Sender Email: {email}\n\n Email Body:\n\n"
            email = EmailMessage(
                email_subject,
                email_sender+email_body,
                email,
                [contact_email],
            )
            email.send(fail_silently=False)
            messages.success(request, "Message sent successfully.",
                             extra_tags='contact_us')
            return redirect('contact-us')
        else:
            return render(request, 'contact_us.html', {'contactForm': contact_form})
