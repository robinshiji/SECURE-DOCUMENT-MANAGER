# Generated by Django 5.0.2 on 2024-09-14 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureapp', '0006_imageupload_delete_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageupload',
            name='description',
        ),
        migrations.AddField(
            model_name='imageupload',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
