from django.contrib import admin
from django.contrib.auth.models import Group
from news.models import News, NewsList, Category, Attachment


class AttachmentInLine(admin.StackedInline):
    model = Attachment
    extra = 1
    max_num = 5


class NewsAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    readonly_fields = ('date_published',)
    filter_horizontal = ['categories']
    list_display = ['title', 'get_author', 'is_published']
    ordering = ['is_published']
    inlines = [AttachmentInLine, ]

    def get_author(self, obj):
        return obj.author.get_full_name()
    get_author.short_description = 'Author'

    # def add_view(self, request, form_url='', extra_context=None):
    #     data = request.GET.copy()
    #     data['author'] = request.user
    #     request.GET = data
    #     return super(NewsAdmin, self).add_view(request, form_url)

    # def get_form(self, request, obj=None, **kwargs):
    #     user_group = Group.objects.get(name="PYLP Member")
    #     if user_group in request.user.groups.all():
    #         self.exclude = ("is_published", "author", "slug", "date_uploaded")
    #     form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
    #     return form

    # def get_queryset(self, request):
    #     user_group = Group.objects.get(name="PYLP Member")
    #     qs = super(NewsAdmin, self).get_queryset(request)
    #     if user_group in request.user.groups.all():
    #         return qs.filter(author=request.user)
    #     else:
    #         return qs


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(News, NewsAdmin)
admin.site.register(NewsList)
admin.site.register(Category)
