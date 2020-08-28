# Generated by Django 3.1 on 2020-08-18 11:40

import account.models
import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200818_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_name',
        ),
        migrations.AlterField(
            model_name='profile',
            name='civil_status',
            field=models.CharField(max_length=100, null=True, verbose_name='Civil Status'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='current_work_affiliation',
            field=models.CharField(max_length=100, null=True, verbose_name='Current Work Affiliation'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook_account',
            field=models.CharField(max_length=80, null=True, verbose_name='Facebook Account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='host_family',
            field=models.CharField(max_length=100, null=True, verbose_name='Host Family'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name_address_office_school',
            field=models.CharField(max_length=150, null=True, verbose_name='Name and Address of Office'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='permanent_address',
            field=models.CharField(max_length=150, null=True, verbose_name='Permanent Address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='present_address',
            field=models.CharField(max_length=150, null=True, verbose_name='Present Address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pylp_batch',
            field=models.PositiveIntegerField(null=True, verbose_name='PYLP Batch'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pylp_year',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1984), account.models.max_value_current_year], verbose_name='PYLP Year'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Telephone Number'),
        ),
    ]
