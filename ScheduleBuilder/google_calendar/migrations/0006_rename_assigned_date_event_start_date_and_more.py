# Generated by Django 4.2.6 on 2023-10-30 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_calendar', '0005_alter_event_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='assigned_date',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='assignment_name',
        ),
        migrations.AddField(
            model_name='event',
            name='amount_per_week',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='Event', max_length=60, verbose_name='Event Title'),
        ),
        migrations.AddField(
            model_name='event',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=10),
        ),
        migrations.AddField(
            model_name='event',
            name='progress',
            field=models.CharField(choices=[('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')], default='not started', max_length=20),
        ),
        migrations.AddField(
            model_name='event',
            name='time_to_spend',
            field=models.IntegerField(default=0),
        ),
    ]