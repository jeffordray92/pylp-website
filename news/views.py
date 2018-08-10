from django.shortcuts import render

# Create your views here.
from django.views import View

from news.models import News, NewsList


class NewsListView(View):

    def get(self, request, *args, **kwargs):
        articles = News.objects.all()
        header = NewsList.objects.first()
        return render(request, 'newslist.html', {
            'articles': articles,
            'header': header,
        })


class NewsView(View):

    def get(self, request, *args, **kwargs):
        article = News.objects.get(slug=kwargs.get('slug'))
        return render(request, 'news.html', {
            'article': article
        })
