from math import floor

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from content.models import Header, Section, Fact
from news.models import News


class HomeView(View):

    def get(self, request, *args, **kwargs):
        header_content = Header.objects.all().first()
        sections = Section.objects.all()
        recent_news = News.objects.all()[:6]
        figures = Fact.objects.all().order_by('id')
        if figures.count() > 4:
            figures = figures[:int(4*floor(figures.count()/4.))]
        return render(request, 'index.html', {
            'header': header_content,
            'sections': sections,
            'recent_news': recent_news,
            'figures': figures
        })
