from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views import View

from content.models import Header, Section


class HomeView(View):

    def get(self, request, *args, **kwargs):
        header_content = Header.objects.all().first()
        sections = Section.objects.all()
        return render(request, 'index.html', {
            'header': header_content,
            'sections': sections,
        })
