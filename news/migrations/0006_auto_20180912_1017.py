# Generated by Django 2.1 on 2018-09-12 10:17

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20180810_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
