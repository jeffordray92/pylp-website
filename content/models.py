import os
from datetime import datetime
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from djrichtextfield.models import RichTextField
from gdstorage.storage import GoogleDriveStorage
from phonenumber_field.modelfields import PhoneNumberField

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

optional = {
    'null': True,
    'blank': True
}

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

GROUP_CHOICES = (
    ('Y', 'Youth'),
    ('A', 'Adult'),
)

EDUCATIONAL_TYPE = (
    ('E', 'Elementary'),
    ('H', 'High School'),
    ('C', 'College'),
    ('P', 'Post Graduate'),
)


def validate_file_size(value):
    filesize = value.size

    if int(filesize) > 26214400:
        raise ValidationError(
            "The maximum file size that can be uploaded is 25MB")
    else:
        return value


def get_image_path(instance, filename):
    return os.path.join('resource-image', str(datetime.now().date()), filename)


def year_choices():
    return [(r, r) for r in range(2004, datetime.now().date().year+1)]


def current_year():
    return datetime.now().date().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)
# Create your models here.


class Account(models.Model):
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
        super(Account, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.user.is_active = self.is_verified
        self.user.save()
        super(Account, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Accounts"


class EducationalBackground(models.Model):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, editable=False, null=True)
    education_type = models.CharField(
        max_length=1, choices=EDUCATIONAL_TYPE, default="C")
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateTimeField(null=True)
    level_attained = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Educational Background"


class MembershipOrganization(models.Model):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, editable=False, null=True)
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True)
    inclusive_date = models.DateTimeField(null=True)
    position_held = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Membership in Youth Organizations"


class CommunityActivity(models.Model):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, editable=False, null=True)
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


class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='header/')
    video = models.URLField(max_length=200, default="")
    details = models.TextField(**optional)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Header Details"
        verbose_name_plural = "Header Details"


class Section(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    section_image = models.ImageField(upload_to='section/')
    subquote_image = models.ImageField(upload_to='section/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"


class Fact(models.Model):
    title = models.CharField(max_length=20)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Facts and Figures"
        verbose_name_plural = "Facts and Figures"


class SocialMedia(models.Model):
    facebook = models.URLField(max_length=200, **optional)
    twitter = models.URLField(max_length=200, **optional)
    instagram = models.URLField(max_length=200, **optional)
    linkedin = models.URLField(max_length=200, **optional)
    telephone = models.CharField(max_length=20, **optional)
    email = models.EmailField(max_length=100, **optional)

    class Meta:
        verbose_name = "Social Media Accounts"
        verbose_name_plural = "Social Media Accounts"


class Resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(**optional)
    image = models.ImageField(upload_to=get_image_path, **optional)
    slug = models.SlugField(default="", **optional)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(Resource, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"


class Attachment(models.Model):
    resource = models.ForeignKey(
        "Resource", on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources', max_length=200,
                            validators=[validate_file_size, ], storage=gd_storage)

    def __str__(self):
        return self.file.name


class ResourceListDetail(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to="resource_header/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Resource List Detail"
        verbose_name_plural = "Resource List Details"


class Location(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Directory(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="M")
    age_group = models.CharField(
        max_length=1, choices=GROUP_CHOICES, default="Y")
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="members", **optional)

    class Meta:
        verbose_name = "Directory Entry"
        verbose_name_plural = "Directory Entries"


class SignUpInstructions(models.Model):
    title = models.CharField(max_length=20)
    content = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Signing Up Instruction"
        verbose_name_plural = "Signing Up Instructions"
