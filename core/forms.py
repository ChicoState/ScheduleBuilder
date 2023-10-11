# core/forms.py
from django import forms

class UploadSyllabusForm(forms.Form):
    syllabus_file = forms.FileField(
        label='Select a syllabus file',
        help_text='Max. 5 MB',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}),  
    )