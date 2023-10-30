# core/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from PyPDF2 import PdfReader
import os
import tempfile
from .assignment_parser import assignment_parser
from .ScheduleParser import parse_keywords, parse_tables, parse_schedule, extract_grade_breakdown
import pdfplumber
import re
import pandas as pd
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PdfReader(pdf_file)
    for page in pdf.pages:
        page_text = page.extract_text()
        # Remove excess whitespace and normalize the text
        page_text = ' '.join(page_text.split())
        text += page_text + "\n"
    return text

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def icalendar(request):
    if request.method == 'POST':
        # Get the iCalendar URL from the form submission
        icalendar_url = request.POST.get('ical_url')

        # Store the URL in session for later use
        request.session['ical_url'] = icalendar_url

        # Redirect to the /calendar page
        return redirect('icalendar-add')
    return render(request, 'parser/icalendar.html')

@login_required
def parser(request):
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
               # Extract tables from the uploaded PDF using PDFPlumber
               with pdfplumber.open(uploaded_file) as pdf:
                   tables_parsed = []
                   for page in pdf.pages:
                       for table in page.extract_tables():
                           if parse_tables(table):
                               tables_parsed.append(table)
               syllabus_contents = extract_text_from_pdf(uploaded_file) 
               text_schedule = parse_schedule(syllabus_contents)
               grade_breakdown = extract_grade_breakdown(syllabus_contents)
               course = re.findall(r"[A-Z][A-Za-z\s-]{1,5}\d{3}", syllabus_contents)
               if course:
                   course = course[0]
               keyword_occurrences = parse_keywords(syllabus_contents)
               return render(request, 'core/syllabus_result.html', {'Important_Syllabus_Info': syllabus_contents, 'Course': course,'keywords': keyword_occurrences, 'tables_parsed': tables_parsed, 'schedule': text_schedule, 'grade_breakdown': grade_breakdown})
    else:
        form = UploadFileForm()

    return render(request, 'parser/parser.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

