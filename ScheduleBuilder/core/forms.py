# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='Max. 5 MB',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf, .txt'}),
    )
    option = forms.ChoiceField(
        choices=[('assignment', 'Assignment'), ('syllabus', 'Syllabus Parser')],
        widget=forms.RadioSelect,
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

