# Generated by Django 3.1 on 2020-08-20 10:20

import account.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_auto_20200820_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='electronic_signature',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(account.models._update_filename, *(), **{'path': 'e_signature', 'type': 'SIGNATURES'}), verbose_name='Electronic Signature'),
        ),
    ]
