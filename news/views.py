from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponseNotFound
from news.models import News, NewsList, Category


class NewsListView(View):

    def get(self, request, *args, **kwargs):

        tag = kwargs.get("tag")

        if tag:
            tag_category = Category.objects.get(slug=tag)
            articles = tag_category.articles.filter(is_published=True)
        else:
            tag_category = []
            articles = News.objects.filter(is_published=True)
        header = NewsList.objects.first()
        categories = Category.objects.all()
        return render(request, 'newslist.html', {
            'articles': articles,
            'header': header,
            'categories': categories,
            'tag_category': tag_category,
        })


class NewsView(View):

    def get(self, request, *args, **kwargs):
        try:
            article = News.objects.get(slug=kwargs.get('slug'))
            if article.is_published:
                return render(request, 'news.html', {
                    'article': article
                })
            else:
                return HttpResponseNotFound('<h1>Article not found</h1>')
        except Exception:
            return HttpResponseNotFound('<h1>Article not found</h1>')
