from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from content.models import (
    Attachment,
    ContactUsEmail,
    Directory,
    Fact,
    Header,
    Location,
    Resource,
    ResourceListDetail,
    Section,
    SocialMedia,
    SignUpInstructions)
from content.forms import SignUpInstructionsForm


# class UserAdmin(BaseUserAdmin):
#     list_filter = []
#     search_fields = []

#     def get_form(self, request, obj=None, **kwargs):
#         user_group = Group.objects.get(name="PYLP Member")
#         if user_group in request.user.groups.all():
#             print(self.list_filter)
#             # self.exclude = (
#             #     "date_joined",
#             #     "groups",
#             #     "is_active",
#             #     "is_superuser",
#             #     "last_login",
#             #     "user_permissions",
#             # )
#             # # self.exclude = ("email",)
#             # print(self.exclude)
#         form = super(UserAdmin, self).get_form(request, obj, **kwargs)
#         return form

#     def get_queryset(self, request):
#         user_group = Group.objects.get(name="PYLP Member")
#         qs = super(UserAdmin, self).get_queryset(request)
#         if user_group in request.user.groups.all():
#             return qs.filter(id=request.user.id)
#         else:
#             return qs
class AttachmentInLine(admin.StackedInline):
    model = Attachment
    extra = 1
    max_num = 5


class ResourceAdmin(admin.ModelAdmin):
    inlines = [AttachmentInLine, ]
    exclude = ['slug', ]


class SignUpInstructionsAdmin(admin.ModelAdmin):
    form = SignUpInstructionsForm


admin.site.register(SignUpInstructions, SignUpInstructionsAdmin)
admin.site.register(Header)
admin.site.register(Section)
admin.site.register(Fact)
admin.site.register(SocialMedia)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceListDetail)
admin.site.register(Location)
admin.site.register(Directory)
admin.site.register(ContactUsEmail)
