# Generated by Django 4.2.5 on 2023-09-27 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_calendar', '0003_alter_event_submission_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='submission_type',
        ),
    ]