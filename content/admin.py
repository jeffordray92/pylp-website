from django.contrib import admin
from content.models import (
    Account,
    Attachment,
    CommunityActivity,
    Directory,
    EducationalBackground,
    Fact,
    Header,
    Location,
    MembershipOrganization,
    Organization,
    Resource,
    ResourceListDetail,
    Section,
    SocialMedia,
    School,
    SignUpInstructions)
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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


class EducationalBackgroundInLine(admin.TabularInline):
    model = EducationalBackground
    extra = 1


class MembershipOrganizationInLine(admin.TabularInline):
    model = MembershipOrganization
    extra = 1


class CommunityActivityInLine(admin.TabularInline):
    model = CommunityActivity
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    model = Account
    readonly_fields = ('user', 'get_name')
    actions = ['verify_selected', ]
    list_display = ['email', 'get_username',
                    'get_name', 'is_verified', 'get_userstaff']
    list_filter = ['is_verified']
    inlines = [EducationalBackgroundInLine,
               MembershipOrganizationInLine, CommunityActivityInLine]

    def get_name(self, obj):
        return obj.user.first_name
    get_name.admin_order_field = 'user__first_name'
    get_name.short_description = 'first Name'

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'username'

    def get_userstaff(self, obj):
        return obj.user.is_staff
    get_userstaff.admin_order_field = 'user__is_staff'
    get_userstaff.short_description = 'staff'

    def verify_selected(self, request, queryset):
        queryset.update(is_verified=True)
        for q in queryset:
            q.user.is_active = True
            q.user.save()
    verify_selected.short_description = "Mark selected users as verified"


class ResourceAdmin(admin.ModelAdmin):
    inlines = [AttachmentInLine, ]
    exclude = ['slug', ]


    # admin.site.unregister(User)
admin.site.register(Account, AccountAdmin)
#admin.site.register(User, UserAdmin)
admin.site.register(SignUpInstructions)
admin.site.register(Header)
admin.site.register(Section)
admin.site.register(Fact)
admin.site.register(SocialMedia)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceListDetail)
admin.site.register(Location)
admin.site.register(Directory)
admin.site.register(School)
admin.site.register(Organization)
