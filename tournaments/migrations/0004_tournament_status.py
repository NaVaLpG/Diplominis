# Generated by Django 5.1.6 on 2025-02-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('u', 'Upcoming'), ('o', 'Ongoing'), ('c', 'Completed')], default='u', max_length=1),
        ),
    ]
