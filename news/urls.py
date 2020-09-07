from django.urls import path
from django.conf.urls import url
from news.views import NewsListView, NewsView, SubmitArticleView, simple_upload

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<str:tag>', NewsListView.as_view(), name='news_list'),
    path('article/<slug:slug>/', NewsView.as_view(), name='news'),
    path('submit-new/', SubmitArticleView.as_view(), name='submit-news'),
    url(r'^upload-image/', simple_upload, name='upload-image'),
]
