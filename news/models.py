import os

from datetime import datetime
from djrichtextfield.models import RichTextField
# from tinymce.models import HTMLField
# from tinymce.widgets import TinyMCE

from django.db import models
from django.template.defaultfilters import slugify


optional = {
    'null': True,
    'blank': True
}

def get_image_path(instance, filename):
    return os.path.join('news', str(datetime.now().date()), filename)


# Create your models here.

class NewsList(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to="news_header/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News List Detail"
        verbose_name_plural = "News List Details"


class News(models.Model):
    title = models.CharField(max_length=100)
    # content = HTMLField()
    content = RichTextField()
    image = models.ImageField(upload_to=get_image_path)
    date_uploaded = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField(default="", **optional)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
