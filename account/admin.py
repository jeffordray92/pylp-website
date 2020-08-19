from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from account.models import (
    Committee,
    CommunityActivity,
    Cluster,
    EducationalBackground,
    MembershipOrganization,
    Organization,
    Profile,
    School,
)
# Register your models here.


class EducationalBackgroundInLine(admin.TabularInline):
    model = EducationalBackground
    extra = 1


class MembershipOrganizationInLine(admin.TabularInline):
    model = MembershipOrganization
    extra = 1


class CommunityActivityInLine(admin.TabularInline):
    model = CommunityActivity
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    readonly_fields = ('user',)
    actions = ['verify_selected', ]
    list_display = ['email', 'get_username',
                    'get_name', 'is_verified', 'get_userstaff']
    list_filter = ['is_verified', 'cluster', 'committees', 'pylp_batch',
                   'educationalbackground__school', 'membershiporganization__organization']
    filter_horizontal = ('committees',)
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

    def has_add_permission(self, request, obj=None):
        return False


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    min_num = 1
    can_delete = False


class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(School)
admin.site.register(Organization)
admin.site.register(Cluster)
admin.site.register(Committee)
