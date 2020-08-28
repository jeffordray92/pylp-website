import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from gdstorage.storage import GoogleDriveStorage
from functools import partial
from django.conf import settings
from dirtyfields import DirtyFieldsMixin

gd_storage = GoogleDriveStorage()


def validate_image_size(value):
    filesize = value.size

    if int(filesize) > 10485760:
        raise ValidationError(
            "The maximum image size that can be uploaded is 10MB")
    else:
        return value


def _update_filename(instance, filename, path, type):
    path = path
    ext = filename.split('.')[-1]
    filename = f"{instance.last_name.upper()}-{instance.pylp_batch}-{instance.pylp_year}-{type.upper()}.{ext}"
    return os.path.join(path, filename)


def upload_to(path, type):
    return partial(_update_filename, path=path, type=type)


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

EDUCATIONAL_TYPE = (
    ('E', 'Elementary'),
    ('H', 'High School'),
    ('C', 'College'),
    ('P', 'Post Graduate'),
)

CIVIL_OPTIONS = (
    ('M', 'Married'),
    ('S', 'Single'),
    ('D', 'Divorced'),
    ('W', 'Widowed')
)


def year_choices():
    return [(r, r) for r in range(2004, datetime.now().date().year+1)]


def current_year():
    return datetime.now().date().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Profile(DirtyFieldsMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    cluster = models.ForeignKey(
        "Cluster", on_delete=models.CASCADE, null=True, blank=True, verbose_name=u"Cluster")
    committees = models.ManyToManyField(
        'Committee', blank=True, verbose_name=u"Committees")
    is_verified = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=upload_to(
        "photos", type="PHOTOS"), blank=True, null=True, verbose_name=u"Profile Picture", storage=gd_storage, validators=[validate_image_size, ])
    electronic_signature = models.ImageField(upload_to=upload_to(
        "e_signature", type="SIGNATURES"), blank=True, null=True, verbose_name=u"Electronic Signature", storage=gd_storage, validators=[validate_image_size, ])
    email = models.EmailField(null=True)
    first_name = models.CharField(
        max_length=100, null=True, verbose_name=u"First Name")
    last_name = models.CharField(
        max_length=100, null=True, verbose_name=u"Last Name")
    birth_date = models.DateField(null=True, verbose_name=u"Date of Birth")
    birth_place = models.CharField(
        max_length=100, null=True, verbose_name=u"Place of Birth")
    civil_status = models.CharField(null=True, default="S",
                                    max_length=100, choices=CIVIL_OPTIONS, verbose_name=u"Civil Status")
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M")
    pylp_batch = models.PositiveIntegerField(
        null=True, verbose_name=u"PYLP Batch")
    pylp_year = models.IntegerField(
        null=True, validators=[MinValueValidator(1984), max_value_current_year], verbose_name=u"PYLP Year", choices=year_choices())
    host_family = models.CharField(
        max_length=100, null=True, verbose_name=u"Host Family")
    present_address = models.CharField(
        max_length=150, null=True, verbose_name=u"Present Address")
    permanent_address = models.CharField(
        max_length=150, null=True, verbose_name=u"Permanent Address")
    current_work_affiliation = models.CharField(
        max_length=100, null=True, verbose_name=u"Current Work Affiliation")
    name_address_office_school = models.CharField(
        max_length=150, null=True, verbose_name=u"Name and Address of Office")
    ethnicity = models.CharField(max_length=80, null=True)
    religion = models.CharField(max_length=80, null=True)
    facebook_account = models.CharField(
        max_length=80, null=True, verbose_name=u"Facebook Account")
    contact_number = PhoneNumberField(
        null=True, verbose_name=u"Contact Number", region="PH")
    telephone_number = PhoneNumberField(
        null=True, verbose_name=u"Telephone Number", region="PH")

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        self.user.is_active = self.is_verified
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
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
        "Profile", on_delete=models.CASCADE, editable=False)
    education_type = models.CharField(
        max_length=1, choices=EDUCATIONAL_TYPE, default="C")
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, verbose_name=u"School")
    inclusive_date = models.DateField()
    level_attained = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Educational Background"


class MembershipOrganization(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False)
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, verbose_name=u"Organization")
    inclusive_date = models.DateField()
    position_held = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Membership in Youth Organizations"


class CommunityActivity(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, editable=False)
    activity_name = models.CharField(max_length=150)
    activity_description = models.CharField(max_length=150)
    sponsor_organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE)
    inclusive_date = models.DateField()

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


class Cluster(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Profile)
def my_post_delete_callback(sender, **kwargs):
    try:
        if kwargs['instance'].user:
            kwargs['instance'].user.delete()
    except:
        pass
