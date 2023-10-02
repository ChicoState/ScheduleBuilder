# core/forms.py
from django import forms

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