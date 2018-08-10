from django.urls import path

from news.views import NewsListView, NewsView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', NewsView.as_view(), name='news')
]
