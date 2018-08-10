from django.contrib import admin
from news.models import News, NewsList


class NewsAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(News, NewsAdmin)
admin.site.register(NewsList)
