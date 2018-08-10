from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'header/')
    video = models.URLField(max_length=200, default="")


class Section(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    section_image = models.ImageField(upload_to = 'section/')
    subquote_image = models.ImageField(upload_to = 'section/')

class Fact(models.Model):
    title = models.CharField(max_length=20)
    value = models.PositiveIntegerField()

class SocialMedia(models.Model):
    facebook = models.URLField(max_length=200, default="")
    twitter = models.URLField(max_length=200, default="")
    instagram = models.URLField(max_length=200, default="")
    linkedin = models.URLField(max_length=200, default="")
    telephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, default="")
