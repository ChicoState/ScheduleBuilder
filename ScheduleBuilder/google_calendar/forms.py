from django import forms
from google_calendar.models import SubmitType, Event

# Valid date formats 
DATE_INPUT_FORMATS = ['%Y-%m-%d','%m/%d/%Y','%m/%d/%y']
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M','%m/%d/%Y %H:%M','%m/%d/%y %H:%M']
RECURRING_OPTIONS = [
    ('weekly', 'Weekly'),
    ('daily', 'Daily'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]

# form for adding an event model into the database / calendar
class EventForm(forms.ModelForm):
    event_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=True)
    class_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    # submission_type = forms.ModelChoiceField(queryset=SubmitType.objects.all(), blank=True)
    start_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD', 
                'size': '80'
            }
        )
    )
    due_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',  
                'size': '80'
            }
        )
    )
    time_to_spend = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to spend (input number)', 'size': '80'}), required=True)
    amount_per_week = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Days per week (input number)', 'size': '80'}), required=True)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        widget=forms.RadioSelect, required=True)
    # friends = forms.ChoiceField(choices=[('assignment', 'Assignment'), ('syllabus', 'Syllabus Parser')],
        # widget=forms.RadioSelect, required=False) # Change this to add friends
    progress = forms.ChoiceField(choices=[('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')],
        widget=forms.RadioSelect, required=True)
    repeat = forms.ChoiceField(
        label='Recurrence Option',
        widget=forms.RadioSelect,
        choices=RECURRING_OPTIONS,
        required=False
    )
    repeat_until = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',  
                'size': '80'
            }
        )
    )
    
    class Meta():
        model = Event
        # fields = ('assignment_name' , 'class_name', 'submission_type', 'assigned_date', 'due_date')
        fields = ('event_name' , 'class_name', 'start_date', 'due_date', 'time_to_spend', 'priority', 'progress', 'repeat', 'repeat_until' )
        
class EditEventForm(forms.ModelForm):
    event_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=True)
    start_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD', 
                'size': '50'
            }
        )
    )
    due_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',  
                'size': '50'
            }
        )
    )
    class Meta:
        model = Event
        fields = ('event_name' , 'start_date', 'due_date')
    
class DeleteEventForm(forms.ModelForm):
    event_title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=True)
    start_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD', 
                'size': '50'
            }
        )
    )
    due_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',  
                'size': '50'
            }
        )
    )
    
    class Meta:
        model = Event
        fields = ('event_title' , 'start_date', 'due_date')