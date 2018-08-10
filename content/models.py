from django.db import models
from tinymce.models import HTMLField

optional = {
    'null': True,
    'blank': True
}


# Create your models here.
class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'header/')
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
    section_image = models.ImageField(upload_to = 'section/')
    subquote_image = models.ImageField(upload_to = 'section/')

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
