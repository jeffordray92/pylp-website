# Generated by Django 3.1 on 2020-08-27 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_auto_20200827_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalbackground',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.school', verbose_name='School'),
        ),
        migrations.AlterField(
            model_name='membershiporganization',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cluster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.cluster', verbose_name='Cluster'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='committees',
            field=models.ManyToManyField(blank=True, to='account.Committee', verbose_name='Committees'),
        ),
    ]
