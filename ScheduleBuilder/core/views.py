from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadSyllabusForm
from PyPDF2 import PdfReader
import pandas as pd
# for when we implement login features
from django.contrib.auth import authenticate, login, logout

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PdfReader(pdf_file)
    for page in pdf.pages:
        text += page.extract_text()
    return text

def main(request):
    if request.method == 'POST':
        form = UploadSyllabusForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded syllabus here
            syllabus_file = form.cleaned_data['syllabus_file']
            if syllabus_file:
                syllabus_contents = extract_text_from_pdf(syllabus_file)
                return render(request, 'core/syllabus_result.html', {'Important_Syllabus_Info': syllabus_contents})



    else:
        form = UploadSyllabusForm()

    return render(request, 'core/home.html', {'form': form})