# Generated by Django 5.1.6 on 2025-02-19 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
    ]
