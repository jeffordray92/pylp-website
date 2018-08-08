from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'header/')


class Section(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    section_image = models.ImageField(upload_to = 'section/')
    subquote = models.CharField(max_length=200)
    subquote_image = models.ImageField(upload_to = 'section/')

