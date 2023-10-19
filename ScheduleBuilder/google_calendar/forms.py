from django import forms
from google_calendar.models import SubmitType, Event

# Valid date formats 
DATE_INPUT_FORMATS = ['%Y-%m-%d','%m/%d/%Y','%m/%d/%y']
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M','%m/%d/%Y %H:%M','%m/%d/%y %H:%M']

# form for adding an event model into the database / calendar
class EventForm(forms.ModelForm):
    assignment_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    class_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    # submission_type = forms.ModelChoiceField(queryset=SubmitType.objects.all(), blank=True)
    assigned_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    due_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    time_to_spend = forms.IntegerField(widget=forms.TextInput(attrs={'size': '80'}))
    amount_per_week = forms.IntegerField(widget=forms.TextInput(attrs={'size': '80'}))
    priority = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    friends = forms.ChoiceField(choices=[('assignment', 'Assignment'), ('syllabus', 'Syllabus Parser')],
        widget=forms.RadioSelect) # Change this to add friends
    progress = forms.ChoiceField(choices=[('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')],
        widget=forms.RadioSelect)
    
    class Meta():
        model = Event
        # fields = ('assignment_name' , 'class_name', 'submission_type', 'assigned_date', 'due_date')
        fields = ('assignment_name' , 'class_name', 'assigned_date', 'due_date', 'time_to_spend', 'priority' )