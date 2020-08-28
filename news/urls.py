from django.urls import path

from news.views import NewsListView, NewsView, SubmitArticleView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<str:tag>', NewsListView.as_view(), name='news_list'),
    path('article/<slug:slug>/', NewsView.as_view(), name='news'),
    path('submit-new/', SubmitArticleView.as_view(), name='submit-news')
]
