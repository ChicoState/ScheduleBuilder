from django import forms
from google_calendar.models import SubmitType, Event, Calendar

# Valid date formats 
DATE_INPUT_FORMATS = ['%Y-%m-%d','%m/%d/%Y','%m/%d/%y']
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M','%m/%d/%Y %H:%M','%m/%d/%y %H:%M']

class CalendarForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'80'}))
    class Meta:
        model = Calendar
        fields = ('name',)
# form for adding an event model into the database / calendar
class EventForm(forms.ModelForm):
    assignment_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    class_name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    # submission_type = forms.ModelChoiceField(queryset=SubmitType.objects.all(), blank=True)
    assigned_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    due_date = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    
    class Meta():
        model = Event
        # fields = ('assignment_name' , 'class_name', 'submission_type', 'assigned_date', 'due_date')
        fields = ('assignment_name' , 'class_name', 'assigned_date', 'due_date')