from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

EDUCATIONAL_TYPE = (
    ('E', 'Elementary'),
    ('H', 'High School'),
    ('C', 'College'),
    ('P', 'Post Graduate'),
)


def year_choices():
    return [(r, r) for r in range(2004, datetime.now().date().year+1)]


def current_year():
    return datetime.now().date().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    is_verified = models.BooleanField(default=False)
    user_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    full_name = models.CharField(max_length=100, null=True)
    birth_date = models.DateTimeField(null=True)
    birth_place = models.CharField(max_length=100, null=True)
    civil_status = models.CharField(max_length=100, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M")
    pylp_batch = models.IntegerField(null=True)
    pylp_year = models.IntegerField(
        null=True, validators=[MinValueValidator(1984), max_value_current_year])
    host_family = models.CharField(max_length=100, null=True)
    present_address = models.CharField(max_length=150, null=True)
    permanent_address = models.CharField(max_length=150, null=True)
    current_work_affiliation = models.CharField(
        max_length=100, null=True)
    name_address_office_school = models.CharField(
        max_length=150, null=True)
    ethnicity = models.CharField(max_length=80, null=True)
    religion = models.CharField(max_length=80, null=True)
    facebook_account = models.CharField(max_length=80, null=True)
    contact_number = PhoneNumberField(null=True)
    telephone_number = PhoneNumberField(null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.is_active = self.is_verified
        self.user.save()
        super(Profile, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.user.is_active = self.is_verified
        self.user.save()
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Profiles"


class EducationalBackground(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    education_type = models.CharField(
        max_length=1, choices=EDUCATIONAL_TYPE, default="C")
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateTimeField(null=True)
    level_attained = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Educational Background"


class MembershipOrganization(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateTimeField(null=True)
    position_held = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Membership in Youth Organizations"


class CommunityActivity(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False, null=True)
    activity_name = models.CharField(max_length=150, null=True)
    activity_description = models.CharField(max_length=150, null=True)
    sponsor_organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Involvement in Youth/Community Related Activities"


class School(models.Model):
    school_name = models.CharField(max_length=150, null=True)
    school_address = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.school_name


class Organization(models.Model):
    organization_name = models.CharField(max_length=150, null=True)
    organization_address = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.organization_name
