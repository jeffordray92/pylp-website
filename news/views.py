from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.html import format_html
from news.models import Attachment, Category, News, NewsList, CkeditorMedia
from news.forms import NewsForm


class NewsListView(View):

    def get(self, request, *args, **kwargs):

        tag = kwargs.get("tag")

        if tag:
            tag_category = Category.objects.get(slug=tag)
            articles = tag_category.articles.filter(is_published=True)
        else:
            tag_category = []
            articles = News.objects.filter(
                is_published=True).order_by('-date_published')
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
                attachments = list(Attachment.objects.filter(news=article))
                content = format_html(article.content)
                return render(request, 'news.html', {
                    'article': article,
                    'attachments': attachments,
                    'content': content
                })
            else:
                return HttpResponseNotFound('<h1>Article not found</h1>')
        except Exception:
            return HttpResponseNotFound('<h1>Article not found</h1>')


class SubmitArticleView(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_authenticated == False):
            return redirect('index')
        return render(request, 'submit_article.html', {'NewsForm': NewsForm})

    def post(self, request, *args, **kwargs):
        news_form = NewsForm(request.POST, request.FILES)
        if news_form.is_valid():
            files = request.FILES.getlist('attachments')
            news = news_form
            try:
                if(request.user.profile != None):
                    news = news_form.save(author=request.user.profile)
                else:
                    news = news_form.save()
            except:
                pass
            for f in files:
                attachment = Attachment(
                    news=news,
                    file=f
                )
                attachment.save()

            messages.success(
                request, "Your article has been submitted and is waiting to be reviewed by the admin.")
            return redirect('news_list')
        else:
            return render(request, 'submit_article.html', {'NewsForm': news_form})


@csrf_exempt
def simple_upload(request):
    if request.method == 'POST':
        image = CkeditorMedia(
            image=request.FILES['upload']
        )
        image.save()
        base_url = request.get_host()
        image_url = f'http://{base_url}{image.image.url}'
        return JsonResponse({'url': image_url})
