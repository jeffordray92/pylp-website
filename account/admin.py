from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
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


class UserVerifiedListFilter(admin.SimpleListFilter):
    title = 'User Verification'

    parameter_name = 'verified'

    def lookups(self, request, model_admin):
        return (
            ('verified', 'verified'),
            ('not verified', 'not verified'),
        )

    def queryset(self, request, queryset):
        if self.value() == "verified":
            return queryset.filter(is_verified=True)
        elif self.value() == "not verified":
            return queryset.exclude(is_verified=True)


class EducationalBackgroundInLine(admin.TabularInline):
    model = EducationalBackground
    extra = 1


class MembershipOrganizationInLine(admin.TabularInline):
    model = MembershipOrganization
    extra = 1


class CommunityActivityInLine(admin.TabularInline):
    model = CommunityActivity
    extra = 1


class ImageListFilter(admin.SimpleListFilter):

    title = _('Profile Photo')

    parameter_name = 'has_photo'

    def lookups(self, request, model_admin):

        return (
            ('yes', _('has photo')),
            ('no',  _('no photo')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'yes':
            return queryset.filter(photo__isnull=False).exclude(photo='')

        if self.value() == 'no':
            return queryset.filter(Q(photo__isnull=True) | Q(photo__exact=''))


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    readonly_fields = ('user',)
    actions = ['verify_selected', ]
    list_display = ['email', 'get_username',
                    'get_name', 'is_verified', 'get_userstaff']
    list_filter = [UserVerifiedListFilter, 'cluster', 'pylp_batch', 'educationalbackground__school',
                   'membershiporganization__organization', 'committees', ImageListFilter]
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
        for q in queryset:
            q.user.is_active = True
            q.user.save()
        queryset.update(is_verified=True)
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
