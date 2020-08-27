import os
from datetime import datetime
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from djrichtextfield.models import RichTextField
from gdstorage.storage import GoogleDriveStorage

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


def validate_file_size(value):
    filesize = value.size

    if int(filesize) > 26214400:
        raise ValidationError(
            "The maximum file size that can be uploaded is 25MB")
    else:
        return value


def validate_image_size(value):
    filesize = value.size

    if int(filesize) > 10485760:
        raise ValidationError(
            "The maximum image size that can be uploaded is 10MB")
    else:
        return value


def get_image_path(instance, filename):
    return os.path.join('resource-image', str(datetime.now().date()), filename)


class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='header/', validators=[validate_image_size, ])
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
    section_image = models.ImageField(
        upload_to='section/', validators=[validate_image_size, ])
    subquote_image = models.ImageField(
        upload_to='section/', validators=[validate_image_size, ])

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
    image = models.ImageField(upload_to=get_image_path,
                              **optional, validators=[validate_image_size, ])
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
    image = models.ImageField(
        upload_to="resource_header/", validators=[validate_image_size, ])

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
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Signing Up Instruction"
        verbose_name_plural = "Signing Up Instructions"


class ContactUsEmail(models.Model):
    email = models.EmailField(null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Contact Email"
