# Generated by Django 4.2.5 on 2023-11-01 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('google_calendar', '0002_event_user_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
