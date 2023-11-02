from django.db import models
from django.contrib.auth.models import User
import datetime

# This isn't working yet, I'm trying to allow only certain types of submission type choices
SUB_TYPES = [("f", "File Upload"), ("t", "Text Submission"), ("i", "Image"), ("l", "Link")]

class SubmitType(models.Model):
    submission_type = models.CharField(max_length=15, choices=SUB_TYPES, default="File Upload")
    def __str__(self):
        return self.submission_type

class Calendar(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE,)
    
    calendar_name = models.CharField(verbose_name="Calendar Title", max_length=30)

# Model for an event to be added into google calendar
class Event(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE,)
    
    assignment_name = models.CharField(verbose_name="Assignment Title", max_length=60)
    class_name = models.CharField(verbose_name="Assignment's class", max_length=9)
    # professor = models.CharField(verbose_name="Professor who assigned", max_length=60)
    # submission_type = models.ForeignKey(SubmitType, on_delete=models.CASCADE, blank=True, null=True)
    assigned_date = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default=datetime.date.today)