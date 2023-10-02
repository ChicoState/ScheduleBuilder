# core/views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from PyPDF2 import PdfReader
import os
import tempfile
from .assignment_parser import assignment_parser

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PdfReader(pdf_file)
    for page in pdf.pages:
        text += page.extract_text()
    return text

def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            option = form.cleaned_data['option']
            temp_file_path = None
            
            if uploaded_file and option == 'assignment':
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                        temp_file.write(extract_text_from_pdf(uploaded_file).encode('utf-8'))
                        temp_file_path = temp_file.name

                    parser = assignment_parser(temp_file_path, uploaded_file.name)
                    parser.process_assignment()
                    parsed_contents = parser.get_parsed_contents()

                    return render(request, 'core/assignment_result.html', {'parsed_contents': parsed_contents})
                finally:
                    if temp_file_path:
                        os.remove(temp_file_path)
            
                return render(request, 'core/assignment_result.html', {'parsed_contents': parsed_contents})

            elif uploaded_file and option == 'syllabus':
                syllabus_contents = extract_text_from_pdf(uploaded_file)
                return render(request, 'core/syllabus_result.html', {'Important_Syllabus_Info': syllabus_contents})

    else:
        form = UploadFileForm()

    return render(request, 'core/home.html', {'form': form})