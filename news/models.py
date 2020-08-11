import os
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

optional = {
    'null': True,
    'blank': True
}


def get_image_path(instance, filename):
    return os.path.join('news', str(datetime.now().date()), filename)


def validate_file_size(value):
    filesize = value.size

    if filesize > 26214400:
        raise ValidationError(
            "The maximum file size that can be uploaded is 25MB")
    else:
        return value
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, **optional)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_image_path)
    date_uploaded = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField(default="", **optional)
    categories = models.ManyToManyField(
        'news.Category', related_name="articles")
    tags = models.CharField(null=True, max_length=100, blank=True)
    caption = models.TextField(max_length=250, **optional)
    share_on_facebook = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False, verbose_name="Published")
    date_published = models.DateTimeField(
        null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published:
            self.date_published = datetime.now()
        if not self.is_published:
            self.date_published = None
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def add_attachment(self, attachment):
        if self.attachment_set.count() >= 5:
            raise Exception("Too many attachments on this News")
        self.attachment_set.add(attachment)

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(**optional)
    slug = models.SlugField(default="", **optional)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Attachment(models.Model):
    news = models.ForeignKey(
        "News", on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_image_path,
                            validators=[validate_file_size, ])

    def __str__(self):
        return self.file.name
