# Generated by Django 5.0.2 on 2024-09-11 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureapp', '0003_document_delete_documentupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
