# Generated by Django 4.2.5 on 2023-10-11 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=60, verbose_name='Assignment Title')),
                ('class_name', models.CharField(max_length=9, verbose_name="Assignment's class")),
                ('assigned_date', models.DateField(default=datetime.date.today)),
                ('due_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='SubmitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_type', models.CharField(choices=[('f', 'File Upload'), ('t', 'Text Submission'), ('i', 'Image'), ('l', 'Link')], default='File Upload', max_length=15)),
            ],
        ),
    ]
