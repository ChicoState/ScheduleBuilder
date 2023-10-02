from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadSyllabusForm
from .ScheduleParser import parse_keywords, parse_tables, parse_schedule, extract_grade_breakdown
from PyPDF2 import PdfReader
import pdfplumber
import re
import pandas as pd
# for when we implement login features
from django.contrib.auth import authenticate, login, logout

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PdfReader(pdf_file)
    for page in pdf.pages:
        page_text = page.extract_text()
        # Remove excess whitespace and normalize the text
        page_text = ' '.join(page_text.split())
        text += page_text + "\n"
    return text

def main(request):
    if request.method == 'POST':
        form = UploadSyllabusForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded syllabus here
            syllabus_file = form.cleaned_data['syllabus_file']
            if syllabus_file:
               # Extract tables from the uploaded PDF using PDFPlumber
               with pdfplumber.open(syllabus_file) as pdf:
                   tables_parsed = []
                   for page in pdf.pages:
                       for table in page.extract_tables():
                           if parse_tables(table):
                               tables_parsed.append(table)
               syllabus_contents = extract_text_from_pdf(syllabus_file) 
               print(syllabus_contents)
               text_schedule = parse_schedule(syllabus_contents)
               grade_breakdown = extract_grade_breakdown(syllabus_contents)
               course = re.findall(r"[A-Z][A-Za-z\s-]{1,5}\d{3}", syllabus_contents)
               if course:
                   course = course[0]
               keyword_occurrences = parse_keywords(syllabus_contents)
               return render(request, 'core/syllabus_result.html', {'Important_Syllabus_Info': syllabus_contents, 'Course': course,'keywords': keyword_occurrences, 'tables_parsed': tables_parsed, 'schedule': text_schedule, 'grade_breakdown': grade_breakdown})
    else:
        form = UploadSyllabusForm()

    return render(request, 'core/home.html', {'form': form})