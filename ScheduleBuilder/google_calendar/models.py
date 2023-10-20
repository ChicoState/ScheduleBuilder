from django.db import models
import datetime

# This isn't working yet, I'm trying to allow only certain types of submission type choices
SUB_TYPES = [("f", "File Upload"), ("t", "Text Submission"), ("i", "Image"), ("l", "Link")]

class SubmitType(models.Model):
    submission_type = models.CharField(max_length=15, choices=SUB_TYPES, default="File Upload")
    def __str__(self):
        return self.submission_type

# Model for an event to be added into google calendar
class Event(models.Model):
    event_name = models.CharField(default="Event", verbose_name="Event Title", max_length=60)
    class_name = models.CharField(verbose_name="Assignment's class", max_length=9)
    start_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default=datetime.date.today)
    time_to_spend = models.IntegerField(default=0)
    amount_per_week = models.IntegerField(default=0)
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low'
    )
    progress = models.CharField(
        max_length=20,
        choices=[('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')],
        default='not started'
    )