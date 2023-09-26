from django.db import models
import datetime

SUB_TYPES = [("f", "File Upload"), ("t", "Text Submission"), ("i", "Image"), ("l", "Link")]

class SubmitType(models.Model):
    submission_type = models.CharField(max_length=15, choices=SUB_TYPES, default="File Upload")
    def __str__(self):
        return self.submission_type
    
class Event(models.Model):
    assignment_name = models.CharField(verbose_name="Assignment Title", max_length=60)
    class_name = models.CharField(verbose_name="Assignment's class", max_length=9)
    # professor = models.CharField(verbose_name="Professor who assigned", max_length=60)
    submission_type = models.ForeignKey(SubmitType, on_delete=models.CASCADE)
    assigned_date = models.DateField(default=datetime.date.today)
    due_date = models.DateTimeField(default=datetime.datetime.today)