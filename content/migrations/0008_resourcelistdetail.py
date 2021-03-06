# Generated by Django 2.1 on 2018-09-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_resource'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceListDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('subtitle', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='resource_header/')),
            ],
            options={
                'verbose_name': 'Resource List Detail',
                'verbose_name_plural': 'Resource List Details',
            },
        ),
    ]
