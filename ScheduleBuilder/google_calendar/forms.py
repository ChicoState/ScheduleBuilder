from django import forms
from google_calendar.models import SubmitType, Event

class EventForm(forms.ModelForm):
    assignment_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    class_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    submission_type = forms.ModelChoiceField(queryset=SubmitType.objects.all())
    assigned_date = forms.DateField()
    due_date = forms.DateTimeField()
    
    class Meta():
        model = Event
        fields = ('assignment_name' , 'class_name', 'submission_type', 'assigned_date', 'due_date')